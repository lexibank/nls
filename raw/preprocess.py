import odf.opendocument 
import collections
from odf.table import Table, TableRow, TableCell
from odf.text import P
from lingpy import Wordlist, ipa2tokens
from lingpy.sequence.sound_classes import token2class
import re

# Copyright 2011 Marco Conti

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Thanks to grt for the fixes

import odf.opendocument
from odf.table import Table, TableRow, TableCell
from odf.text import P

# http://stackoverflow.com/a/4544699/1846474
class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)

class ODSReader:

    # loads the file
    def __init__(self, file, clonespannedcolumns=None):
        self.clonespannedcolumns = clonespannedcolumns
        self.doc = odf.opendocument.load(file)
        self.SHEETS = {}
        for sheet in self.doc.spreadsheet.getElementsByType(Table):
            self.readSheet(sheet)

    # reads a sheet in the sheet dictionary, storing each sheet as an
    # array (rows) of arrays (columns)
    def readSheet(self, sheet):
        name = sheet.getAttribute("name")
        rows = sheet.getElementsByType(TableRow)
        arrRows = []

        # for each row
        for row in rows:
            row_comment = ""
            arrCells = GrowingList()
            cells = row.getElementsByType(TableCell)

            # for each cell
            count = 0
            for cell in cells:
                # repeated value?
                repeat = cell.getAttribute("numbercolumnsrepeated")
                if(not repeat):
                    repeat = 1
                    spanned = int(cell.getAttribute('numbercolumnsspanned') or 0)
                    # clone spanned cells
                    if self.clonespannedcolumns is not None and spanned > 1:
                        repeat = spanned

                ps = cell.getElementsByType(P)
                textContent = ""

                # for each text/text:span node
                for p in ps:
                    for n in p.childNodes:
                        if (n.nodeType == 1 and
                                ((n.tagName == "text:span") or (n.tagName == "text:a"))):
                            for c in n.childNodes:
                                if (c.nodeType == 3):
                                    textContent = u'{}{}'.format(textContent, c.data)

                        if (n.nodeType == 3):
                            textContent = u'{}{}'.format(textContent, n.data)

                if(textContent):
                    if(textContent[0] != "#"):  # ignore comments cells
                        for rr in range(int(repeat)):  # repeated?
                            arrCells[count]=textContent
                            count+=1
                    else:
                        row_comment = row_comment + textContent + " "
                else:
                    for rr in range(int(repeat)):
                        count+=1

            # if row contained something
            if(len(arrCells)):
                arrRows.append(arrCells)

            #else:
            #    print ("Empty or commented row (", row_comment, ")")

        self.SHEETS[name] = arrRows

    # returns a sheet as an array (rows) of arrays (columns)
    def getSheet(self, name):
        return self.SHEETS[name]



def clusters(word):
    
    cons = []
    prec = ("^", "^")
    for i, (snd, scl) in enumerate([(w, token2class(w, 'cv')) for w in word]):
        if scl == 'C':
            if prec[1] == 'C':
                cons[-1] += [snd]
            else:
                cons += [[prec[0], snd]]
        #else:
        #    if prec == 'C':
        prec = (snd, scl)
    return cons
        


doc = ODSReader("data.ods")

sheets = {
        "Athpahariya": "", 
        "Bantawa": "", 
        "Belhare": "", 
        "Chamling": "",
        "Chintang": "",
        "Chulung": "",
        "Dhimal": "",
        "Dulung": "",
        "Ghale-Gurung": "",
        "Gurung": "",
        "Jirel": "",
        }

languages = doc.getSheet("languages")
concepts = doc.getSheet("concepts")

for sheet in list(sheets):
    sheets[sheet] = doc.getSheet(sheet)

wl = {0: ["doculect", "dataset", "concept", "concept_in_source",
          "concept_id", 
          "value",
          "form", "tokens", "pages"]}

language_lookup = {}
for row in languages[1:]:
    language_lookup[row[1].strip()] = row[0].strip()
concept_lookup = {}
for row in concepts[1:]:
    concept_lookup[row[0].strip(".")] = (row[0], row[1])
    concept_lookup[row[1].strip().lower()] = (row[0], row[1])

concept_lookup["burn"] = concept_lookup["to burn"]
concept_lookup["we"] = concept_lookup["we (inclusive)"]
concept_lookup["to speak"] = concept_lookup["to speak/speak"]
concept_lookup["to run"] = concept_lookup["to run/run"]
concept_lookup["to go"] = concept_lookup["to go/go"]
concept_lookup["to listen"] = concept_lookup["to hear/hear/listen"]
concept_lookup["to look"] = concept_lookup["to look/look"]
concept_lookup["rice"] = concept_lookup["rice (husked)"]


all_toks = collections.defaultdict(lambda : collections.defaultdict(list))
idx = 1
current_page = ""
for sheet in sheets:
    print(f'processing sheet {sheet}')
    header = sheets[sheet][0]
    for row in sheets[sheet][1:]:
        data = dict(zip(header, row))
        if "Number" in data:
            concept, number = concept_lookup[data["Number"].strip(".")]
        else:
            try:
                concept, number = concept_lookup[data["English"].lower().strip()]
            except KeyError:
                print("key error {0} / {1}".format(data["English"], data["Nepali"]))
                concept, number = "", ""
        if concept and number:
            cis = data["English"]
            page = data.get("Page", "").strip()
            if not page:
                page = current_page
            else:
                current_page = page
            for language in header[3:][:-1]:
                value = data[language.strip()]
                if value.strip() and not value.strip() == "-":
                    for form in re.split("[,;/]", value):
                        try:
                            tks = ipa2tokens(form.strip().replace(" ",
                                                                  "+").replace("-",
                                                                               "+"),
                                             semi_diacritics="shz–")
                        except:
                            tks = list(form.replace(" ", "+"))
                        wl[idx] = [
                                language,
                                sheet,
                                concept,
                                cis, number,
                                value,
                                form.strip(), tks, page]
                        idx += 1
                        for i, tk in enumerate(tks):
                            if i == 0:
                                all_toks[sheet]['^' + tk] += [(form.strip(),
                                                               language)
                                                            ]
                            elif i == len(tk) - 1:
                                all_toks[sheet][tk + '$'] += [(form.strip(),
                                                               language)
                                                            ]

                            else:
                                all_toks[sheet][tk] += [(form.strip(), language)]


wl = Wordlist(wl)
wl.output("tsv", filename="first-pass", ignore="all", prettify=False)

# obtain consonant clusters
clrs = collections.defaultdict(lambda : collections.defaultdict(list))
for idx, lng, ds, tokens in wl.iter_rows("doculect", "dataset", "tokens"):
    cons = clusters(tokens)
    for clr in cons:
        if clr[0] == "^":
            clrs[ds][" ".join(clr)] += [idx]
        else:
            clrs[ds][" ".join(clr[1:])] += [idx]

for sheet in all_toks:
    with open(f"orthography-{sheet}.tsv", "w") as f:
        f.write("Grapheme\tIPA\tFrequency\tExamples\tLanguages\n")
        visited = set()
        for k, v in sorted(all_toks[sheet].items(), key=lambda x: len(x[1]), reverse=True):
           
            if k[0] == '^':
                t = k[1:]
            elif k[-1] == '$':
                t = k[:-1]
            else:
                if token2class(k, 'dolgo') in 'V1':
                    t = k
                else:
                    t = "+ " + k
            f.write(f'{k}\t{t}\t{len(v)}\t{"//".join([x[0] for x in v][:2])}')
            f.write(f'\t{"/".join(list(set([x[1] for x in v])))}\n')
            visited.add(k)
        for clr, idxs in clrs[sheet].items():
            if clr.replace(" ", "") not in visited:
                f.write(f'{clr.replace(" ", "")}\t{clr}\t{len(idxs)}\t')
                f.write(f'{"//".join([" ".join(wl[idx, "tokens"]) for idx in idxs[:2]])}\t\n')
