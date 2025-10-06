"""
PDF download manager.
"""

import aiohttp
import aiofiles
import asyncio
from pathlib import Path
from typing import Optional, List, Dict
from urllib.parse import urlparse, unquote
import re

from .logger import get_logger
from .validators import validate_url, validate_pdf
from config.settings import Settings

logger = get_logger(__name__)


class PDFDownloader:
    """Async PDF downloader sa retry mehanizmom."""
    
    def __init__(
        self,
        output_dir: Path = None,
        max_concurrent: int = None,
        timeout: int = None
    ):
        """
        Inicijalizuje downloader.
        
        Args:
            output_dir: Direktorijum za čuvanje fajlova
            max_concurrent: Max broj istovremenih download-a
            timeout: Timeout za download u sekundama
        """
        self.output_dir = output_dir or Settings.OUTPUT_DIR
        self.max_concurrent = max_concurrent or Settings.MAX_CONCURRENT_DOWNLOADS
        self.timeout = timeout or Settings.DOWNLOAD_TIMEOUT
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        self.downloaded_files: List[Path] = []
        self.failed_downloads: List[Dict] = []
    
    async def download_file(
        self,
        url: str,
        filename: Optional[str] = None,
        category: str = "other"
    ) -> Optional[Path]:
        """
        Preuzima jedan fajl.
        
        Args:
            url: URL PDF fajla
            filename: Ime fajla (opcionalno, izvlači se iz URL-a)
            category: Kategorija za organizaciju
        
        Returns:
            Path do preuzetog fajla ili None ako je neuspešno
        """
        async with self.semaphore:
            try:
                # Validacija URL-a
                if not validate_url(url):
                    logger.warning(f"Nevažeći URL: {url}")
                    return None
                
                # Generiši ime fajla
                if not filename:
                    filename = self._extract_filename(url)
                
                # Osiguraj da ima .pdf ekstenziju
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                
                # Kreiraj output direktorijum
                output_path = self.output_dir / category
                output_path.mkdir(parents=True, exist_ok=True)
                
                # Potpuna putanja fajla
                filepath = output_path / filename
                
                # Ako fajl već postoji, preskoči
                if filepath.exists():
                    logger.info(f"Fajl već postoji: {filename}")
                    self.downloaded_files.append(filepath)
                    return filepath
                
                # Preuzmi fajl
                logger.info(f"Preuzimam: {filename}")
                
                timeout_obj = aiohttp.ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                    async with session.get(
                        url,
                        headers={'User-Agent': Settings.USER_AGENT}
                    ) as response:
                        
                        if response.status != 200:
                            logger.error(f"HTTP {response.status} za {url}")
                            self.failed_downloads.append({
                                'url': url,
                                'filename': filename,
                                'reason': f'HTTP {response.status}'
                            })
                            return None
                        
                        # Proveri Content-Type
                        content_type = response.headers.get('Content-Type', '')
                        if 'pdf' not in content_type.lower() and 'octet-stream' not in content_type.lower():
                            logger.warning(f"Možda nije PDF: {content_type}")
                        
                        # Sačuvaj fajl
                        async with aiofiles.open(filepath, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                await f.write(chunk)
                
                # Validacija PDF-a
                if not validate_pdf(filepath):
                    logger.error(f"Nevažeći PDF fajl: {filename}")
                    filepath.unlink()  # Obriši nevažeći fajl
                    self.failed_downloads.append({
                        'url': url,
                        'filename': filename,
                        'reason': 'Invalid PDF format'
                    })
                    return None
                
                logger.info(f"✓ Uspešno preuzeto: {filename}")
                self.downloaded_files.append(filepath)
                return filepath
                
            except asyncio.TimeoutError:
                logger.error(f"Timeout za {url}")
                self.failed_downloads.append({
                    'url': url,
                    'filename': filename or 'unknown',
                    'reason': 'Timeout'
                })
                return None
                
            except Exception as e:
                logger.error(f"Greška pri preuzimanju {url}: {e}")
                self.failed_downloads.append({
                    'url': url,
                    'filename': filename or 'unknown',
                    'reason': str(e)
                })
                return None
    
    async def download_multiple(
        self,
        urls: List[str],
        category: str = "other"
    ) -> List[Path]:
        """
        Preuzima više fajlova istovremeno.
        
        Args:
            urls: Lista URL-ova
            category: Kategorija za organizaciju
        
        Returns:
            Lista putanja do preuzet fajlova
        """
        tasks = [
            self.download_file(url, category=category)
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
    
    def _extract_filename(self, url: str) -> str:
        """Izvlači ime fajla iz URL-a."""
        # Parsuj URL
        parsed = urlparse(url)
        path = unquote(parsed.path)
        
        # Izvuci ime fajla
        filename = Path(path).name
        
        # Ako nema ime, generiši
        if not filename or filename == '':
            # Koristi hash ili deo URL-a
            filename = f"document_{abs(hash(url)) % 10000}.pdf"
        
        # Očisti ime fajla od nedozvoljenih karaktera
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        return filename
    
    def get_statistics(self) -> Dict:
        """Vraća statistiku preuzimanja."""
        return {
            'total_downloaded': len(self.downloaded_files),
            'total_failed': len(self.failed_downloads),
            'success_rate': (
                len(self.downloaded_files) / 
                (len(self.downloaded_files) + len(self.failed_downloads)) * 100
                if (len(self.downloaded_files) + len(self.failed_downloads)) > 0
                else 0
            ),
            'downloaded_files': [str(f) for f in self.downloaded_files],
            'failed_downloads': self.failed_downloads
        }
