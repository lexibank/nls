from datasette import hookimpl

@hookimpl
def extra_template_vars():
    return {
            "CustomTables": {
                "LanguageTable": {
                    "columns": {
                        "cldf_id": "ID", 
                        "cldf_name": "Name",
                        "cldf_glottocode": "Glottolog",
                        "cldf_latitude": "Latitude",
                        "cldf_longitude": "Longitude",
                        "Macroarea": "Macroarea",
                        "Family": "Family",
                        },
                    "title": "Languages",
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

