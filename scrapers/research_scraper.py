"""
Scraper za naučne radove.
"""

from crawlee.crawlers import PlaywrightCrawlingContext
from utils.logger import get_logger
from utils.validators import is_pdf_url
from .base_scraper import BaseScraper

logger = get_logger(__name__)


class ResearchScraper(BaseScraper):
    """Scraper specifičan za naučne radove."""

    async def extract_pdf_urls(self, context: PlaywrightCrawlingContext):
        """Izvlači PDF URL-ove naučnih radova."""
        page = context.page

        try:
            # Čekaj da se stranica učita
            await page.wait_for_load_state("networkidle", timeout=30000)

            logger.debug(f"Scraping stranice: {page.url}")

            # Specifična logika za arXiv
            if "arxiv.org" in page.url:
                await self._scrape_arxiv(context)

            # Specifična logika za PubMed
            elif "pubmed" in page.url or "ncbi.nlm.nih.gov" in page.url:
                await self._scrape_pubmed(context)

            # Generička logika
            else:
                await self._scrape_generic(context)

        except Exception as e:
            logger.error(f"Greška pri ekstrakciji sa {page.url}: {e}")

    async def _scrape_arxiv(self, context: PlaywrightCrawlingContext):
        """Scraping specifičan za arXiv."""
        page = context.page

        # Pronađi sve PDF linkove
        pdf_links = await page.query_selector_all('a[title="Download PDF"]')

        for link in pdf_links:
            href = await link.get_attribute("href")
            if href:
                # arXiv PDF URL-ovi počinju sa /pdf/
                if href.startswith("/"):
                    href = f"https://arxiv.org{href}"

                if href not in self.pdf_urls:
                    # Izvuci naslov
                    try:
                        title_elem = await link.evaluate_handle(
                            'el => el.closest("li").querySelector(".title")'
                        )
                        title = (
                            await title_elem.inner_text()
                            if title_elem
                            else "Unknown"
                        )
                    except Exception as e:
                        logger.debug(f"Error extracting title: {e}")
                        title = "Unknown"

                    self.pdf_urls.append(href)
                    self.metadata.append(
                        {
                            "url": href,
                            "title": title.strip(),
                            "source": "arXiv",
                        }
                    )
                    logger.debug(f"Pronađen PDF: {title[:50]}...")

    async def _scrape_pubmed(self, context: PlaywrightCrawlingContext):
        """Scraping specifičan za PubMed."""
        page = context.page

        # Pronađi PDF linkove
        links = await page.evaluate(
            """
            () => {
                const results = [];
                document.querySelectorAll('a').forEach(link => {
                    const href = link.href;
                    const text = link.textContent.toLowerCase();

                    if (href && (
                        text.includes('pdf') ||
                        href.includes('.pdf')
                    )) {
                        const titleElem = link.closest('.rprt')
                            ?.querySelector('.title');
                        const title = titleElem?.textContent ||
                                     'Unknown';
                        results.push({
                            url: href,
                            title: title
                        });
                    }
                });
                return results;
            }
        """
        )

        for link in links:
            url = link["url"]
            if url not in self.pdf_urls:
                self.pdf_urls.append(url)
                self.metadata.append(
                    {
                        "url": url,
                        "title": link["title"].strip(),
                        "source": "PubMed",
                    }
                )
                logger.debug(f"Pronađen PDF: {link['title'][:50]}...")

    async def _scrape_generic(self, context: PlaywrightCrawlingContext):
        """Generički scraping za research papere."""
        page = context.page

        # Pronađi sve linkove koji vode do PDF-a
        links = await page.evaluate(
            """
            () => {
                const links = [];
                document.querySelectorAll('a').forEach(link => {
                    const href = link.href;
                    if (href && (
                        href.toLowerCase().endsWith('.pdf') ||
                        link.textContent.toLowerCase().includes('download pdf')
                    )) {
                        links.push({
                            url: href,
                            title: link.textContent.trim() || 'Unknown'
                        });
                    }
                });
                return links;
            }
        """
        )

        for link in links:
            url = link["url"]
            if is_pdf_url(url) and url not in self.pdf_urls:
                self.pdf_urls.append(url)
                self.metadata.append(
                    {
                        "url": url,
                        "title": link["title"],
                        "source": self.source.name,
                    }
                )
                logger.debug(f"Pronađen PDF: {link['title'][:50]}...")
