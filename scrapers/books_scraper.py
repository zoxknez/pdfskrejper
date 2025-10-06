"""
Scraper za knjige.
"""

from crawlee.crawlers import PlaywrightCrawlingContext
from utils.logger import get_logger
from utils.validators import is_pdf_url
from .base_scraper import BaseScraper

logger = get_logger(__name__)


class BooksScraper(BaseScraper):
    """Scraper specifičan za knjige."""
    
    async def extract_pdf_urls(self, context: PlaywrightCrawlingContext):
        """Izvlači PDF URL-ove knjiga."""
        page = context.page
        
        try:
            # Čekaj da se stranica učita
            await page.wait_for_load_state('networkidle', timeout=30000)
            
            logger.debug(f"Scraping stranice: {page.url}")
            
            # Izvuci sve linkove koji vode do PDF-a
            links = await page.evaluate("""
                () => {
                    const links = [];
                    
                    // Pronađi sve <a> tagove
                    document.querySelectorAll('a').forEach(link => {
                        const href = link.href;
                        if (href && (
                            href.toLowerCase().includes('.pdf') ||
                            href.toLowerCase().includes('pdf') && 
                            href.toLowerCase().includes('download')
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
            """)
            
            # Dodaj pronađene URL-ove
            for link in links:
                url = link['url']
                title = link['title']
                
                if is_pdf_url(url) and url not in self.pdf_urls:
                    self.pdf_urls.append(url)
                    self.metadata.append({
                        'url': url,
                        'title': title,
                        'source': self.source.name
                    })
                    logger.debug(f"Pronađen PDF: {title[:50]}...")
            
            # Pronađi dodatne stranice sa knjigama
            book_links = await page.query_selector_all(
                self.source.selectors.get('book_link', 'a')
            )
            
            # Dodaj dodatne stranice za crawling
            for book_link in book_links[:10]:  # Limit na prvih 10
                href = await book_link.get_attribute('href')
                if href:
                    # Normalizuj URL
                    if href.startswith('/'):
                        from urllib.parse import urljoin
                        href = urljoin(page.url, href)
                    
                    # Dodaj u queue ako nije PDF direktno
                    if not is_pdf_url(href):
                        await context.add_requests([href])
            
        except Exception as e:
            logger.error(f"Greška pri ekstrakciji sa {page.url}: {e}")
