"""
Konfiguracija izvora za scraping PDF dokumenata.
"""

from enum import Enum
from typing import Dict, List


class SourceType(Enum):
    """Tipovi izvora dokumenata."""

    BOOKS = "books"
    RESEARCH = "research"
    MAGAZINES = "magazines"
    DOCUMENTS = "documents"
    CUSTOM = "custom"


class Source:
    """Predstavlja jedan izvor za scraping."""

    def __init__(
        self,
        name: str,
        url: str,
        source_type: SourceType,
        description: str = "",
        selectors: Dict[str, str] = None,
    ):
        self.name = name
        self.url = url
        self.source_type = source_type
        self.description = description
        self.selectors = selectors or {}

    def __repr__(self):
        return f"Source(name='{self.name}', type='{self.source_type.value}')"


# Definisani izvori za scraping
SOURCES = {
    SourceType.BOOKS: [
        Source(
            name="Project Gutenberg",
            url="https://www.gutenberg.org/",
            source_type=SourceType.BOOKS,
            description="Besplatne knjige u javnom domenu",
            selectors={
                "search_url": "https://www.gutenberg.org/ebooks/search/?query={query}",
                "book_link": "a.link",
                "pdf_link": "a[href$='.pdf']",
                "title": "h1",
            },
        ),
        Source(
            name="Open Library",
            url="https://openlibrary.org/",
            source_type=SourceType.BOOKS,
            description="Otvorena biblioteka knjiga",
            selectors={
                "search_url": "https://openlibrary.org/search?q={query}",
                "book_link": "a.results",
                "title": "h3.booktitle",
            },
        ),
    ],
    SourceType.RESEARCH: [
        Source(
            name="arXiv",
            url="https://arxiv.org/",
            source_type=SourceType.RESEARCH,
            description="Naučni radovi iz fizike, matematike, računarstva",
            selectors={
                "search_url": "https://arxiv.org/search/?query={query}&searchtype=all",
                "paper_link": "li.arxiv-result",
                "pdf_link": "a[title='Download PDF']",
                "title": "p.title",
                "abstract": "span.abstract-full",
            },
        ),
        Source(
            name="PubMed Central",
            url="https://www.ncbi.nlm.nih.gov/pmc/",
            source_type=SourceType.RESEARCH,
            description="Biomedicinski i životni naučni radovi",
            selectors={
                "search_url": "https://www.ncbi.nlm.nih.gov/pmc/?term={query}",
                "paper_link": "div.rprt",
                "pdf_link": "a.pdf",
                "title": "a.title",
            },
        ),
        Source(
            name="SSRN",
            url="https://www.ssrn.com/",
            source_type=SourceType.RESEARCH,
            description="Društvene nauke istraživački radovi",
            selectors={
                "search_url": "https://www.ssrn.com/index.cfm/en/search/?search={query}",
                "paper_link": "div.paper-item",
                "pdf_link": "a.download",
                "title": "h3.title",
            },
        ),
    ],
    SourceType.MAGAZINES: [
        Source(
            name="Internet Archive",
            url="https://archive.org/",
            source_type=SourceType.MAGAZINES,
            description="Digitalni arhiv časopisa i publikacija",
            selectors={
                "search_url": "https://archive.org/search.php?query={query}&and[]=mediatype:texts",
                "item_link": "div.item-ia",
                "pdf_link": "a[href$='.pdf']",
                "title": "div.item-ttl",
            },
        ),
    ],
    SourceType.DOCUMENTS: [
        Source(
            name="Custom Source",
            url="",
            source_type=SourceType.DOCUMENTS,
            description="Dodaj custom URL za scraping",
            selectors={},
        ),
    ],
}


def get_sources_by_type(source_type: SourceType) -> List[Source]:
    """Vraća sve izvore za dati tip."""
    return SOURCES.get(source_type, [])


def get_all_sources() -> List[Source]:
    """Vraća sve dostupne izvore."""
    all_sources = []
    for sources_list in SOURCES.values():
        all_sources.extend(sources_list)
    return all_sources


def get_source_by_name(name: str) -> Source:
    """Pronalazi izvor po imenu."""
    for sources_list in SOURCES.values():
        for source in sources_list:
            if source.name.lower() == name.lower():
                return source
    return None
