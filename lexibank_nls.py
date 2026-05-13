import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language, Lexeme
from pylexibank import FormSpec
from lingpy import Wordlist


def coord(ipt):
    tuples = []
    for char in ipt:
        if char.isnumeric() or char == '.':
            if len(tuples) == 0:
                tuples += ['']
            tuples[-1] += char
        else:
            tuples += ['']
    triple = [t for t in tuples if t.strip()]
    if len(triple) == 3:
        return int(triple[0]) + float(triple[1]) / 60 + float(triple[2]) / 3600
    else:
        print(ipt)
        return ''


@attr.s
class CustomLexeme(Lexeme):
    Dataset = attr.ib(default=None)
    Gloss_in_Source = attr.ib(default=None)
    Borrowing = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Location = attr.ib(default=None)
    Subgroup = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Dataset = attr.ib(default=None)




class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nls"
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    
    form_spec = FormSpec(separators="~;,/", missing_data=["∅"], first_form_only=True)

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concept_lookup = {}
        for concept in self.conceptlists[0].concepts.values():
            concept_lookup[concept.number] = concept.english
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="number",
        )

        # load borrowings
        borrowings = {(
            row["Language"], row["Concept"], row["Value"]
            ): row["Borrowing"]
                      for row in self.raw_dir.read_csv("borrowings.tsv", delimiter="\t",
                                           dicts=True)
                      }

 
        # add language
        languages = {}
        for language in self.languages:
            lat = coord(language["Latitudex"])
            lon = coord(language["Longitudex"])
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Latitude=lat, #coord(language["Latitudex"]),
                    Longitude=lon, #coord(language["Longitudex"]),
                    Glottocode=language["Glottocode"],
                    Location=language["Location"],
                    Dataset=language["File"]
                    )
            languages[language["Name"]] = language["ID"]

        #languages = args.writer.add_languages(lookup_factory="Name")
        args.log.info("added languages")

        wl = Wordlist(self.raw_dir.joinpath("first-pass.tsv").as_posix())
        errors = set()
        missing = set()
        for idx in wl:
            if wl[idx, 'dataset'] in ["Athpahariya", "Bantawa", "Chamling",
                                      "Belhare", "Chintang", "Dhimal",
                                      "Chulung", "Dulung", "Ghale-Gurung"]:
                if wl[idx, "concept"].strip(".") in concepts:
                    language = languages[wl[idx, "doculect"]]
                    concept = concept_lookup[wl[idx, "concept"].strip('.')]
                    value = wl[idx, "value"]
                    bor = borrowings.get((language, concept, value), "")
                    args.writer.add_form(
                            Language_ID=languages[wl[idx, 'doculect']],
                            Parameter_ID=concepts[wl[idx, "concept"].strip(".")],
                            Value=wl[idx, 'value'],
                            Form=wl[idx, 'form'].replace(" ", "_^").replace("-", "_^"),
                            Borrowing=bor,
                            Source=''
                            )
                else:
                    errors.add((wl[idx, "dataset"], wl[idx, "concept"]))
            else:
                missing.add(wl[idx, 'dataset'])
        for a, b in errors:
            args.log.info("Missing Concept Number: " + a + " " + b)
        for m in missing:
            args.log.info("Missing Dataset: " + m)


