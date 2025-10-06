"""
Scraper za časopise i magazine.
"""

from crawlee.crawlers import PlaywrightCrawlingContext
from utils.logger import get_logger
from utils.validators import is_pdf_url
from .base_scraper import BaseScraper

logger = get_logger(__name__)


class MagazineScraper(BaseScraper):
    """Scraper specifičan za časopise i magazine."""

    async def extract_pdf_urls(self, context: PlaywrightCrawlingContext):
        """Izvlači PDF URL-ove časopisa."""
        page = context.page

        try:
            # Čekaj da se stranica učita
            await page.wait_for_load_state("networkidle", timeout=30000)

            logger.debug(f"Scraping stranice: {page.url}")

            # Internet Archive specifična logika
            if "archive.org" in page.url:
                await self._scrape_archive_org(context)
            else:
                await self._scrape_generic(context)

        except Exception as e:
            logger.error(f"Greška pri ekstrakciji sa {page.url}: {e}")

    async def _scrape_archive_org(self, context: PlaywrightCrawlingContext):
        """Scraping specifičan za Internet Archive."""
        page = context.page

        # Pronađi sve stavke
        items = await page.query_selector_all(".item-ia")

        for item in items[: self.max_results]:
            try:
                # Pronađi link do stavke
                link_elem = await item.query_selector("a.stealth")
                if not link_elem:
                    continue

                href = await link_elem.get_attribute("href")
                if not href:
                    continue

                # Normalizuj URL
                if href.startswith("/"):
                    href = f"https://archive.org{href}"

                # Poseti stranicu stavke
                detail_page = await context.browser_controller.new_page()

                try:
                    await detail_page.goto(href, timeout=30000)
                    await detail_page.wait_for_load_state("networkidle")

                    # Pronađi PDF link
                    pdf_link = await detail_page.query_selector(
                        'a[href$=".pdf"]'
                    )

                    if pdf_link:
                        pdf_href = await pdf_link.get_attribute("href")
                        if pdf_href:
                            if pdf_href.startswith("/"):
                                pdf_href = f"https://archive.org{pdf_href}"

                            if pdf_href not in self.pdf_urls:
                                # Izvuci naslov
                                title_elem = await detail_page.query_selector(
                                    "h1.item-title"
                                )
                                title = (
                                    await title_elem.inner_text()
                                    if title_elem
                                    else "Unknown"
                                )

                                self.pdf_urls.append(pdf_href)
                                self.metadata.append(
                                    {
                                        "url": pdf_href,
                                        "title": title.strip(),
                                        "source": "Internet Archive",
                                    }
                                )
                                logger.debug(f"Pronađen PDF: {title[:50]}...")
                finally:
                    await detail_page.close()

            except Exception as e:
                logger.debug(f"Greška pri obradi stavke: {e}")
                continue

    async def _scrape_generic(self, context: PlaywrightCrawlingContext):
        """Generički scraping za magazine."""
        page = context.page

        # Pronađi sve PDF linkove
        links = await page.evaluate(
            """
            () => {
                const links = [];
                document.querySelectorAll('a').forEach(link => {
                    const href = link.href;
                    if (href && (
                        href.toLowerCase().endsWith('.pdf') ||
                        link.textContent.toLowerCase().includes('pdf')
                    )) {
                        const title = link.textContent.trim() ||
                                     link.title ||
                                     'Unknown';
                        links.push({
                            url: href,
                            title: title
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
