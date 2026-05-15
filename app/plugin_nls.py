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

