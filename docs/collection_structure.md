# ARCHE Archival Structure

## Collection Hierarchy

The dataset is structured as a five-level hierarchy following ARCHE's OAIS-based model:

```
id:dhd-conferences-factgrid   [acdh:TopCollection]
│   hasTitle: "DHd Conferences as an Evolving Constellation (FactGrid)"
│   hasLicense: CC BY 4.0
│   hasCoverageStartDate: 2014
|   hasCoverageEndDate: 2025
│   hasDepositor: Tinghui Duan (https://orcid.org/0000-0002-3324-0938)
│
├── id:.../conferences         [acdh:Collection]
│   │   hasTitle: "DHd Annual Conferences"
│   └── id:.../conferences/conferences.csv     [acdh:Resource]
│           hasFormat: text/csv
│           hasDescription: "Export via 01_conferences.rq"
│
├── id:.../publications        [acdh:Collection]
│   │   hasTitle: "DHd Conference Publications / Abstracts"
│   └── id:.../publications/publications.csv   [acdh:Resource]
│           hasFormat: text/csv
│
├── id:.../authors             [acdh:Collection]
│   │   hasTitle: "DHd Conference Authors"
│   ├── id:.../authors/authors.csv             [acdh:Resource]
│   └── id:.../authors/author_leaderboard.csv  [acdh:Resource]
│
├── id:.../affiliations        [acdh:Collection]
│   │   hasTitle: "Author Institutional Affiliations"
│   └── id:.../affiliations/affiliations.csv   [acdh:Resource]
│
└── id:.../gender              [acdh:Collection]
    │   hasTitle: "Gender Distribution at DHd Conferences"
    └── id:.../gender/gender_distribution.csv  [acdh:Resource]
```

## Rationale

The thematic sub-collections map directly to the six SPARQL queries defined on the FactGrid project page, ensuring a 1:1 traceability between the archived data and its source. Each collection is self-contained (can be cited independently) and linked via `acdh:isPartOf` to the TopCollection.

## File Naming Convention

| Pattern                     | Example                    |
| --------------------------- | -------------------------- |
| `{topic}.csv`             | `conferences.csv`        |
| `{topic}_{qualifier}.csv` | `author_leaderboard.csv` |

All filenames: lowercase, underscores as separators, no special characters, UTF-8 encoded.

## Formats

All data is stored as **CSV (text/csv, UTF-8)** — an open, non-proprietary format listed as recommended for long-term preservation in ARCHE's format policy. The metadata is additionally provided as **Turtle/RDF (.ttl)**, the native serialisation of ARCHE's metadata schema.
