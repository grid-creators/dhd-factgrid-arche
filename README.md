# DHd Conferences as an Evolving Constellation – ARCHE SIP (demo)

**Contact:** Tinghui Duan · [FactGrid Project Page](https://database.factgrid.de/wiki/FactGrid:The_DHd_conferences_as_an_evolving_constellation)

This repository contains the **Submission Information Package (SIP)** for archiving the FactGrid dataset on DHd (Digital Humanities im deutschsprachigen Raum) annual conferences in [ARCHE](https://arche.acdh.oeaw.ac.at/) (A Resource Centre for the HumanitiEs), operated by the Austrian Centre for Digital Humanities (ACDH).

---

## Dataset Overview

The dataset captures structured data about DHd annual conferences (2014–2025) as modelled in [FactGrid](https://database.factgrid.de), a Wikibase instance for historical and humanities research. It covers:

| Topic                  | SPARQL Query                  | Description                                        |
| ---------------------- | ----------------------------- | -------------------------------------------------- |
| **Conferences**  | `01_conferences.rq`         | Dates, locations, websites for each DHd conference |
| **Publications** | `02_publications.rq`        | Abstracts with authors                             |
| **Authors**      | `03_authors.rq`             | Person entities with ORCID identifiers             |
| **Affiliations** | `04_affiliations.rq`        | Contributing institutional affiliations per year   |
| **Gender**       | `05_gender_distribution.rq` | Aggregated gender distribution per conference year |
| **Leaderboard**  | `06_author_leaderboard.rq`  | Authors ranked by publication count                |

---

## Repository Structure

```
dhd-factgrid-arche/
│
├── sparql/                          # SPARQL queries for FactGrid endpoint
│   ├── 01_conferences.rq
│   ├── 02_publications.rq
│   ├── 03_authors.rq
│   ├── 04_affiliations.rq
│   ├── 05_gender_distribution.rq
│   └── 06_author_leaderboard.rq
│
├── scripts/
│   ├── fetch_data.py                # Fetch data from FactGrid → CSV
│   └── map_to_arche.py              # Map CSV data → ARCHE metadata TTL
│
├── data/
│   └── sample/                      # Sample data (10 rows each, for illustration)
│       ├── conferences.csv
│       ├── publications.csv
│       └── authors.csv
│
├── metadata/
│   ├── arche_metadata.ttl           # ARCHE-compliant metadata (Turtle/RDF)
│   └── arche_metadata_mapping.csv   # FactGrid → ARCHE property mapping table
│
├── docs/
│   └── collection_structure.md      # Archival structure diagram
│
└── README.md
```

---

## Quickstart: Reproduce the Full Dataset

### 1. Install dependencies

```bash
pip install requests pandas rdflib
```

### 2. Fetch data from FactGrid

```bash
python scripts/fetch_data.py --output-dir data/
```

Runs all six SPARQL queries against `https://database.factgrid.de/sparql` and saves results as CSV.

### 3. Generate ARCHE metadata (TTL)

```bash
python scripts/map_to_arche.py --data-dir data/ --output metadata/arche_metadata.ttl
```

## ARCHE Collection Structure

```
TopCollection: dhd-conferences-factgrid
│
├── Collection: conferences/
│   └── Resource: conferences.csv
│
├── Collection: publications/
│   └── Resource: publications.csv
│
├── Collection: authors/
│   ├── Resource: authors.csv
│   └── Resource: author_leaderboard.csv
│
├── Collection: affiliations/
│   └── Resource: affiliations.csv
│
└── Collection: gender/
    └── Resource: gender_distribution.csv
```

---

## ARCHE Compliance

This SIP was checked against the [ARCHE deposition process](https://arche.acdh.oeaw.ac.at/browser/deposition-process), the [ARCHE metadata schema](https://github.com/acdh-oeaw/arche-schema), and the automated [repo-file-checker](https://github.com/acdh-oeaw/repo-file-checker).

### Filenames

- ✅ Lowercase, underscores as separators, no special characters, no spaces
- ✅ No case-insensitive conflicts
- ✅ No duplicate files

### File Formats

- ✅ CSV (`text/csv`) — accepted and suitable for long-term preservation per `arche-assets/formats.json`
- ✅ Turtle/RDF (`.ttl`) — native ARCHE metadata format
- ✅ SPARQL (`.rq`) — plain text, UTF-8

### Metadata Properties (per level)

| Property                     | TopCollection | Collection | Resource | Notes                         |
| ---------------------------- | :-----------: | :--------: | :------: | ----------------------------- |
| `hasTitle`                 |      ✅      |     ✅     |    ✅    | EN + DE                       |
| `hasDescription`           |      ✅      |     ✅     |    ✅    |                               |
| `hasDepositor`             |      ✅      |     ✅     |    ✅    |                               |
| `hasMetadataCreator`       |      ✅      |     ✅     |    ✅    |                               |
| `hasOwner`                 |      ✅      |     ✅     |    ✅    |                               |
| `hasContact`               |      ✅      |     ✅     |    ✅    |                               |
| `hasRightsHolder`          |      ✅      |     —     |    —    | TopCollection only            |
| `hasLicensor`              |      ✅      |     —     |    —    | TopCollection only            |
| `hasPrincipalInvestigator` |      ✅      |     —     |    —    | TopCollection only            |
| `hasHosting`               |      ✅      |     —     |    —    | `id.acdh.oeaw.ac.at/arche`  |
| `hasLicense`               |      ✅      |     ✅     |    ✅    | CC BY 4.0                     |
| `hasFilename`              |      —      |     —     |    ✅    | Required by repo-file-checker |
| `hasFormat`                |      —      |     —     |    ✅    | `text/csv`                  |
| `hasCategory`              |      —      |     —     |    ✅    | `archecategory/dataset`     |
| `hasCoverageStartDate/End` |      ✅      |     —     |    —    | From FactGrid wdt:P49/P50     |
| `hasPid`                   |      ⏳      |     —     |    —    | Assigned by ARCHE post-ingest |

---

## Rights & Licence

The DHd Book of Abstracts data is published under **CC BY 4.0**. The SPARQL queries, scripts, and metadata mappings in this repository are also released under CC BY 4.0.

> Duan, Tinghui (2026). *DHd Conferences as an Evolving Constellation – ARCHE SIP*. GitHub. https://github.com/grid-creators/dhd-factgrid-arche

---

## SPARQL Endpoint

The `.rq` files in `sparql/` can be pasted directly into the [FactGrid Query Service](https://database.factgrid.de/query/).
