# SQL Statements for Querying the Data

```
SQLite-3.54 NLS.sqlite-> select language, borrowing, count(borrowing) from forms where borrowing != '' group by language, borrowing;
╭──────────────────────────┬───────────┬──────────────────╮
│         Language         │ Borrowing │ count(borrowing) │
╞══════════════════════════╪═══════════╪══════════════════╡
│ Aaptar                   │ Nepali    │               14 │
│ Balamta                  │ Nepali    │               10 │
│ Barbhanjyang             │ Nepali    │                9 │
│ Bartole                  │ Nepali    │               35 │
│ Bastim                   │ Nepali    │               25 │
│ Belhara                  │ Nepali    │               32 │
│ Chambak                  │ Nepali    │               37 │
│ Chaudhari Tole           │ Nepali    │               34 │
│ Chaukibari               │ Nepali    │               29 │
│ Dandatole                │ Nepali    │               35 │
│ Dhimal East              │ Nepali    │               29 │
│ Dhimal West              │ Nepali    │               28 │
│ Gairi                    │ Nepali    │                8 │
│ Hadunge                  │ Nepali    │               10 │
│ Halesi                   │ Nepali    │               10 │
│ Hatiya /Dhan kuta Bazaar │ Nepali    │               27 │
│ Khalde                   │ English   │                1 │
│ Khalde                   │ Nepali    │               27 │
│ Khoku, Dhankuta          │ Nepali    │               29 │
│ Lungin (Hatuwa)          │ Nepali    │               29 │
│ Mangthana                │ Nepali    │               37 │
│ Mulgaun                  │ Nepali    │               36 │
│ Nangchhuwa               │ Nepali    │               37 │
│ Okhre, Khena             │ Nepali    │               29 │
│ Pakha                    │ Nepali    │                8 │
│ Piple                    │ Nepali    │               30 │
│ Pokla                    │ Nepali    │                8 │
│ Ratanchha                │ Nepali    │                9 │
│ Rudra bari               │ Nepali    │               35 │
│ Santang                  │ Nepali    │               26 │
│ Suke-ahal                │ Nepali    │                8 │
│ Tekunala                 │ English   │                1 │
│ Tekunala                 │ Nepali    │               24 │
│ Tharpu                   │ Nepali    │               42 │
│ Thidingkha, (Amchok)     │ Nepali    │               33 │
│ Timma, Rimchim           │ Nepali    │               33 │
╰──────────────────────────┴───────────┴──────────────────╯
```
