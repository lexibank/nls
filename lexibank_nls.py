import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec
from lingpy import Wordlist


@attr.s
class CustomLanguage(Language):
    Location = attr.ib(default=None)
    Subgroup = attr.ib(default=None)
    Latitudex = attr.ib(default=None)
    Longitudex = attr.ib(default=None)
    File = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "nls"
    language_class = CustomLanguage
    form_spec = FormSpec(separators="~;,/", missing_data=["∅"], first_form_only=True)

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="number",
        )
 
        # add language
        languages = args.writer.add_languages(lookup_factory="Name")
        args.log.info("added languages")

        wl = Wordlist(self.raw_dir.joinpath("first-pass.tsv").as_posix())
        errors = set()
        missing = set()
        for idx in wl:
            if wl[idx, 'dataset'] in ["Athpahariya", "Bantawa", "Chamling",
                                      "Belhare", "Chintang", "Dhimal", "Chulung"]:
                if wl[idx, "concept"].strip(".") in concepts:
                    args.writer.add_form(
                            Language_ID=languages[wl[idx, 'doculect']],
                            Parameter_ID=concepts[wl[idx, "concept"].strip(".")],
                            Value=wl[idx, 'value'],
                            Form=wl[idx, 'form'].replace(" ", "_^").replace("-", "_^"),
                            Source='')
                else:
                    errors.add((wl[idx, "dataset"], wl[idx, "concept"]))
            else:
                missing.add(wl[idx, 'dataset'])
        for a, b in errors:
            args.log.info("Missing Concept Number: " + a + " " + b)
        for m in missing:
            args.log.info("Missing Dataset: " + m)


