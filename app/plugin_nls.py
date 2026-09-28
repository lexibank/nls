from datasette import hookimpl

@hookimpl
def extra_template_vars():
    return {
            "CustomTables": {
                "Languages": {
                    "columns": {
                        "ID": "ID",
                        "CLDF_ID": "CLDF_ID", 
                        "Name": "Name",
                        "Subgroup": "Subgroup",
                        "cldf_glottocode": "Glottolog",
                        "Latitude": "Latitude",
                        "Longitude": "Longitude",
                        "Family": "Family",
                        "Forms": "Forms"
                        },
                    "title": "Languages",
                    },
                "Forms": {
                    "columns": {
                        "ID": "ID",
                        "CLDF_ID": "CLDF_ID",
                        "Concept_ID": "Concept_ID",
                        "Concept": "Concept",
                        "Language_ID": "Language_ID",
                        "Language": "Language",
                        "Value": "Value",
                        "Form": "Form",
                        "cldf_segments": "Segments",
                        "Borrowing": "Borrowing",
                        },
                    "title": "Forms",
                    },
                "Concepts": {
                    "columns": {
                        "ID": "ID",
                        "CLDF_ID": "CLDF_ID",
                        "Name": "Name",
                        "Chinese": "Chinese",
                        "cldf_concepticonReference": "Concepticon",
                        "Forms": "Forms",
                        
                        },
                    "title": "Concepts"
                    },
                "ParameterTable": {
                    "columns": {
                        "cldf_id": "ID", 
                        "cldf_name": "Name",
                        "cldf_concepticonReference": "Concepticon",
                        "Dataset": "Dataset",
                        # "Forms": "Forms",
                        # "Varieties": "Varieties",
                        # "Languages": "Languages",
                        # "Families": "Families",
                        },
                    "title": "Concepts",
                    },
                "FormTable": {
                    "columns": {
                        "cldf_id": "ID",
                        "cldf_languageReference": "Language",
                        "cldf_parameterReference": "Concept",
                        "cldf_value": "Value",
                        "cldf_form": "Form",
                        "cldf_segments": "Segments",
                        "Borrowing": "Borrowing",
                        "cldf_sourceReference": "Source",
                    },
                    "title": "Forms",
                },
                "ContributionTable": {
                    "columns": {
                        "cldf_id": "Name",
                        "cldf_contributor": "Creator",
                        "cldf_citation": "Citation",
                        "DOI": "DOI",
                        "Editor": "CLDF_Editor",
                        "Version": "Version",
                        },
                    "title": "Datasets",
                    },
                "MorphemeTable": {
                        "columns": {
                            "ID": "ID",
                            "Language_ID": "Language_ID",
                            "Language": "Language",
                            "Concept_ID": "Concept_ID",
                            "Concept": "Concept",
                            "cldf_segments": "Segments",
                            "Morpheme": "Morpheme",
                            "Position": "Position",
                            },
                        "title": "MorphemeTable",
                        },
                "Morphemes": {
                        "columns": {
                            "ID": "ID",
                            "Language_ID": "Language_ID",
                            "Language": "Language",
                            "Morpheme": "Morpheme",
                            "Frequency": "Frequency",
                            },
                        "title": "Morphemes",
                        },
                "Sounds": {
                        "columns": {
                            "ID": "ID",
                            "Language_ID": "Language_ID",
                            "Language": "Language",
                            "Sound": "Sound",
                            "Frequency": "Frequency",
                            },
                        "title": "Sounds",
                        },
                "SoundsTable": {
                        "columns": {
                            "ID": "ID",
                            "Language_ID": "Language_ID",
                            "Language": "Language",
                            "Concept_ID": "Concept_ID",
                            "Concept": "Concept",
                            "cldf_segments": "Segments",
                            "Sound": "Sound",
                            "Position": "Position",
                            },
                        "title": "SoundTable",
                        },
                "SourceTable": {
                        "columns": {
                            "id": "Name",
                            "author": "Author",
                            "title": "Title",
                            "year": "Year"
                            },
                        "title": "Sources"
                        }
            }
    }

