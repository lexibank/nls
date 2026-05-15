-- Basic Merged View for Calculation
DROP VIEW IF EXISTS form_table_view;
CREATE VIEW form_table_view AS
SELECT 
  ROW_NUMBER() OVER (ORDER BY f.cldf_id) as ID,
  f.cldf_id as CLDF_ID,
  l.cldf_id as Language_ID,
  l.cldf_name as Language,
  l.cldf_glottocode,
  l.cldf_latitude as Latitude,
  l.cldf_longitude as Longitude,
  l.subgroup as Subgroup,
  l.family as Family,
  c.cldf_id as Concept_ID,
  c.cldf_name as Concept,
  c.cldf_concepticonReference,
  c.Concepticon_Gloss as Concepticon_Gloss,
  f.cldf_value as Value,
  f.cldf_form as Form,
  f.cldf_segments as Segments,
  f.graphemes as Graphemes,
  f.borrowing as Borrowing,
  f.dataset as Dataset
FROM FormTable as f, ParameterTable as c, LanguageTable as l
WHERE 
  l.cldf_id = f.cldf_languageReference AND
  c.cldf_id = f.cldf_parameterReference
;



-- Language Table
DROP TABLE IF EXISTS Languages;
CREATE TABLE Languages (
  ID TEXT PRIMARY KEY,
  CLDF_ID,
  Variety text,
  Subgroup text,
  cldf_glottocode text,
  Family text,
  Latitude integer,
  Longitude integer,
  Forms integer,
  FOREIGN KEY(CLDF_ID) REFERENCES LanguageTable(CLDF_ID)

);

INSERT INTO Languages 
  SELECT 
    ROW_NUMBER() OVER (ORDER BY Language_ID),
    Language_ID,
    Language,
    Subgroup,
    cldf_glottocode,
    Family,
    Latitude,
    Longitude,
    COUNT (Language_ID)
  FROM form_table_view
  GROUP BY Language_ID
;

-- Concept Table
DROP TABLE IF EXISTS Concepts;
CREATE TABLE Concepts (
  ID INTEGER PRIMARY KEY,
  CLDF_ID,
  Name text,
  cldf_concepticonReference integer,
  Concepticon_Gloss text,
  Forms INTEGER,
  FOREIGN KEY(CLDF_ID) REFERENCES ParameterTable(CLDF_ID)
);

INSERT INTO Concepts
SELECT 
    ROW_NUMBER() OVER (ORDER BY Concept_ID),
    Concept_ID,
    Concept,
    cldf_concepticonReference,
    Concepticon_Gloss,
    COUNT (Concept_ID)
  FROM form_table_view
  GROUP BY Concept_ID
;
    

-- Form Table
DROP TABLE IF EXISTS Forms;
CREATE TABLE Forms (
  ID INTEGER PRIMARY KEY,
  CLDF_ID text,
  Language_ID text,
  Language INTEGER,
  Subgroup text,
  Concept_ID INTEGER,
  Concept text,
  Value text,
  Form text,
  cldf_segments text,
  Borrowing text,
  Dataset,
  FOREIGN KEY(Language_ID) REFERENCES Languages(ID),
  FOREIGN KEY(Concept_ID) REFERENCES Concepts(ID),
  FOREIGN KEY(CLDF_ID) REFERENCES FormTable(CLDF_ID)
);

INSERT INTO FORMS
SELECT 
  ft.ID,
  ft.CLDF_ID,
  l.ID,
  ft.Language,
  ft.Subgroup,
  c.ID,
  ft.Concept,
  ft.Value,
  ft.Form,
  ft.Segments,
  ft.Borrowing,
  ft.Dataset
FROM form_table_view as ft, Languages as l, Concepts as c
WHERE ft.language_id = l.cldf_id AND ft.concept_id = c.cldf_id
;
 

