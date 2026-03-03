#!/usr/bin/env python3
"""
map_to_arche.py
===============
Reads the fetched CSV files (output of fetch_data.py) and generates ARCHE-compliant
metadata in Turtle (TTL) format, following the ACDH metadata schema.

Usage:
    python scripts/map_to_arche.py [--data-dir data/] [--output metadata/arche_metadata.ttl]

ARCHE schema documentation:
    https://acdh-oeaw.github.io/arche-schema/
    https://arche.acdh.oeaw.ac.at/browser/filenames-formats-metadata

Requirements:
    pip install pandas rdflib

Compliance notes (checked against ARCHE deposition process, arche-schema, repo-file-checker):
    TopCollection : hasTitle, hasDescription, hasDepositor, hasPrincipalInvestigator,
                    hasMetadataCreator, hasRightsHolder, hasLicensor, hasOwner, hasContact,
                    hasHosting, hasLicense, hasLanguage
    Collection    : hasTitle, hasDepositor, hasMetadataCreator, hasOwner, hasContact,
                    hasLicense, isPartOf
    Resource      : hasTitle, hasFilename, hasFormat, hasCategory, hasDepositor,
                    hasMetadataCreator, hasOwner, hasContact, hasLicense, isPartOf, hasCreatedDate
    NOTE: hasPid is assigned by ARCHE after ingest — do NOT provide it manually.
"""

import os
import argparse
import logging
from datetime import datetime

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ─── Namespaces ────────────────────────────────────────────────────────────────
ACDH  = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
ID    = Namespace("https://id.acdh.oeaw.ac.at/")
ORCID = Namespace("https://orcid.org/")

# ─── Collection constants ──────────────────────────────────────────────────────
TOP_COLLECTION_ID  = "dhd-conferences-factgrid"
TOP_COLLECTION_URI = ID[TOP_COLLECTION_ID]

DEPOSITOR_ORCID    = ORCID["0000-0002-3324-0938"]

# ARCHE controlled vocabulary URIs
ARCHE_LICENSE_CC_BY = URIRef("https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0")
ARCHE_LANG_DE       = URIRef("https://vocabs.acdh.oeaw.ac.at/iso6391/de")
ARCHE_LANG_EN       = URIRef("https://vocabs.acdh.oeaw.ac.at/iso6391/en")
ARCHE_CATEGORY_DS   = URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/dataset")
ARCHE_HOSTING       = URIRef("https://id.acdh.oeaw.ac.at/arche")
ARCHE_DISCIPLINE    = URIRef("https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/602")

FACTGRID_PROJECT = URIRef(
    "https://database.factgrid.de/wiki/FactGrid:The_DHd_conferences_as_an_evolving_constellation"
)


def init_graph() -> Graph:
    g = Graph()
    g.bind("acdh", ACDH)
    g.bind("id",   ID)
    g.bind("rdf",  RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd",  XSD)
    return g


def _add_common_agent_props(g: Graph, uri: URIRef) -> None:
    """Shared agent + rights properties for Collection and Resource nodes."""
    g.add((uri, ACDH.hasDepositor,       DEPOSITOR_ORCID))
    g.add((uri, ACDH.hasMetadataCreator, DEPOSITOR_ORCID))
    g.add((uri, ACDH.hasOwner,           DEPOSITOR_ORCID))
    g.add((uri, ACDH.hasContact,         DEPOSITOR_ORCID))
    g.add((uri, ACDH.hasLicense,         ARCHE_LICENSE_CC_BY))


def add_top_collection(g: Graph) -> None:
    """Create the TopCollection node."""
    tc = TOP_COLLECTION_URI
    g.add((tc, RDF.type,                      ACDH.TopCollection))
    g.add((tc, ACDH.hasTitle,                 Literal(
        "DHd Conferences as an Evolving Constellation (FactGrid)", lang="en")))
    g.add((tc, ACDH.hasTitle,                 Literal(
        "DHd-Konferenzen als evolutionäre Konstellation (FactGrid)", lang="de")))
    g.add((tc, ACDH.hasDescription,           Literal(
        "This collection preserves structured data about the annual Conferences of the Alliance "
        "of Digital Humanities in the German-speaking area (DHd), covering the years 2014-2025. "
        "The data was originally modelled in FactGrid, a Wikibase instance for historical and "
        "humanities research data, and includes information on conferences, publications/abstracts, "
        "authors, institutional affiliations, and gender distribution.",
        lang="en"
    )))
    _add_common_agent_props(g, tc)
    g.add((tc, ACDH.hasPrincipalInvestigator, DEPOSITOR_ORCID))
    g.add((tc, ACDH.hasRightsHolder,          DEPOSITOR_ORCID))
    g.add((tc, ACDH.hasLicensor,              DEPOSITOR_ORCID))
    g.add((tc, ACDH.hasHosting,               ARCHE_HOSTING))
    g.add((tc, ACDH.hasLanguage,              ARCHE_LANG_DE))
    g.add((tc, ACDH.hasLanguage,              ARCHE_LANG_EN))
    g.add((tc, ACDH.hasSubject,               Literal("Digital Humanities", lang="en")))
    g.add((tc, ACDH.hasSubject,               Literal("Conference Proceedings", lang="en")))
    g.add((tc, ACDH.hasSubject,               Literal("Bibliometrics", lang="en")))
    g.add((tc, ACDH.hasSubject,               Literal("Linked Open Data", lang="en")))
    g.add((tc, ACDH.hasSubject,               Literal("Wikibase", lang="en")))
    g.add((tc, ACDH.hasRelatedDiscipline,     ARCHE_DISCIPLINE))
    g.add((tc, ACDH.hasCoverageStartDate,     Literal("2014-01-01", datatype=XSD.date)))
    g.add((tc, ACDH.hasCoverageEndDate,       Literal("2025-12-31", datatype=XSD.date)))
    g.add((tc, ACDH.hasNamingScheme,          Literal(
        "Files follow the pattern {topic}.csv (lowercase, underscores). "
        "No special characters, no spaces. Example: gender_distribution.csv",
        lang="en"
    )))
    g.add((tc, ACDH.hasUrl,                   FACTGRID_PROJECT))
    g.add((tc, RDFS.seeAlso,                  URIRef("https://database.factgrid.de/wiki/FactGrid:The_DHd_conferences_as_an_evolving_constellation")))
    log.info("TopCollection added.")


def add_sub_collection(g: Graph, name: str, label_en: str, label_de: str,
                        description_en: str) -> URIRef:
    """Add a thematic sub-Collection."""
    uri = ID[f"{TOP_COLLECTION_ID}/{name}"]
    g.add((uri, RDF.type,            ACDH.Collection))
    g.add((uri, ACDH.hasTitle,       Literal(label_en, lang="en")))
    g.add((uri, ACDH.hasTitle,       Literal(label_de, lang="de")))
    g.add((uri, ACDH.hasDescription, Literal(description_en, lang="en")))
    g.add((uri, ACDH.isPartOf,       TOP_COLLECTION_URI))
    _add_common_agent_props(g, uri)
    return uri


def add_resource(g: Graph, file_name: str, parent_uri: URIRef,
                  title_en: str, description_en: str,
                  date_created: str = None) -> URIRef:
    """Add a single Resource (CSV file) node with all required properties."""
    uri = ID[f"{TOP_COLLECTION_ID}/{file_name}"]
    basename = file_name.split("/")[-1]
    g.add((uri, RDF.type,            ACDH.Resource))
    g.add((uri, ACDH.hasTitle,       Literal(title_en, lang="en")))
    g.add((uri, ACDH.hasDescription, Literal(description_en, lang="en")))
    g.add((uri, ACDH.isPartOf,       parent_uri))
    g.add((uri, ACDH.hasFilename,    Literal(basename)))
    g.add((uri, ACDH.hasFormat,      Literal("text/csv")))
    g.add((uri, ACDH.hasCategory,    ARCHE_CATEGORY_DS))
    _add_common_agent_props(g, uri)
    if date_created:
        g.add((uri, ACDH.hasCreatedDate, Literal(date_created, datatype=XSD.date)))
    return uri


def build_collection_structure(g: Graph) -> None:
    """Define sub-collections and resources (mirrors the six SPARQL queries)."""
    today = datetime.today().strftime("%Y-%m-%d")

    sc = add_sub_collection(g, "conferences",
        "DHd Annual Conferences", "DHd-Jahreskonferenzen",
        "Basic metadata for each DHd annual conference: location, dates, website.")
    add_resource(g, "conferences/conferences.csv", sc,
        "DHd Conferences - Basic Data",
        "CSV via query 01_conferences.rq. Columns: item, itemLabel, itemDescription, "
        "Localisation, LocalisationLabel, Begin_date, End_date, Website, Online_information.",
        today)

    sc = add_sub_collection(g, "publications",
        "DHd Conference Publications / Abstracts", "DHd-Konferenzbeitraege und Abstracts",
        "All papers and abstracts submitted to DHd conferences, with DOI/URL where available.")
    add_resource(g, "publications/publications.csv", sc,
        "DHd Publications - Full List",
        "CSV via query 02_publications.rq. Columns: item, itemLabel, conference, "
        "conferenceLabel, year, doi, url.", today)

    sc = add_sub_collection(g, "authors",
        "DHd Conference Authors", "DHd-Konferenzautorinnen",
        "All persons who authored at least one DHd conference contribution, "
        "with ORCID identifiers where available.")
    add_resource(g, "authors/authors.csv", sc,
        "DHd Authors - Full List",
        "CSV via query 03_authors.rq. Columns: author, authorLabel, orcid, "
        "publication, publicationLabel, conference, conferenceLabel, year.", today)
    add_resource(g, "authors/author_leaderboard.csv", sc,
        "DHd Author Leaderboard by Publication Count",
        "CSV via query 06_author_leaderboard.rq. "
        "Columns: author, authorLabel, orcid, pubCount, conferences.", today)

    sc = add_sub_collection(g, "affiliations",
        "Author Institutional Affiliations", "Institutionelle Zugehoerigkeiten der Autorinnen",
        "Affiliations of DHd authors at the time of each contribution, including country.")
    add_resource(g, "affiliations/affiliations.csv", sc,
        "DHd Author Affiliations",
        "CSV via query 04_affiliations.rq. Columns: author, authorLabel, affiliation, "
        "affiliationLabel, affiliationCountry, affiliationCountryLabel, "
        "conference, conferenceLabel, year.", today)

    sc = add_sub_collection(g, "gender",
        "Gender Distribution at DHd Conferences", "Geschlechterverteilung auf DHd-Konferenzen",
        "Aggregated gender distribution of authors per DHd conference year.")
    add_resource(g, "gender/gender_distribution.csv", sc,
        "DHd Gender Distribution per Conference",
        "CSV via query 05_gender_distribution.rq. "
        "Columns: conference, conferenceLabel, year, gender, genderLabel, count.", today)

    log.info("Sub-collections and resources added.")


def add_person_node(g: Graph) -> None:
    g.add((DEPOSITOR_ORCID, RDF.type,      ACDH.Person))
    g.add((DEPOSITOR_ORCID, ACDH.hasTitle, Literal("Tinghui Duan")))


def main():
    parser = argparse.ArgumentParser(description="Map DHd/FactGrid data to ARCHE TTL")
    parser.add_argument("--data-dir", default="data/")
    parser.add_argument("--output",   default="metadata/arche_metadata.ttl")
    args = parser.parse_args()

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    g = init_graph()
    add_person_node(g)
    add_top_collection(g)
    build_collection_structure(g)
    g.serialize(destination=args.output, format="turtle")
    log.info(f"TTL written to {args.output}  ({len(g)} triples)")


if __name__ == "__main__":
    main()
