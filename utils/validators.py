"""
Validatori za URL-ove i fajlove.
"""

import re
from pathlib import Path
from urllib.parse import urlparse
from typing import Union

from .logger import get_logger

logger = get_logger(__name__)


def validate_url(url: str) -> bool:
    """
    Validira da li je URL ispravan.
    
    Args:
        url: URL za validaciju
    
    Returns:
        True ako je validan, inače False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.debug(f"URL validacija neuspešna za {url}: {e}")
        return False


def validate_pdf(filepath: Union[str, Path]) -> bool:
    """
    Validira da li je fajl validan PDF.
    
    Args:
        filepath: Putanja do fajla
    
    Returns:
        True ako je validan PDF, inače False
    """
    filepath = Path(filepath)
    
    # Proveri da li fajl postoji
    if not filepath.exists():
        logger.debug(f"Fajl ne postoji: {filepath}")
        return False
    
    # Proveri veličinu (mora biti > 0)
    if filepath.stat().st_size == 0:
        logger.debug(f"Fajl je prazan: {filepath}")
        return False
    
    # Proveri PDF magic bytes (%PDF)
    try:
        with open(filepath, 'rb') as f:
            header = f.read(5)
            if header != b'%PDF-':
                logger.debug(f"Nevažeći PDF header: {filepath}")
                return False
    except Exception as e:
        logger.debug(f"Greška pri čitanju fajla {filepath}: {e}")
        return False
    
    return True


def sanitize_filename(filename: str) -> str:
    """
    Čisti ime fajla od nedozvoljenih karaktera.
    
    Args:
        filename: Originalno ime fajla
    
    Returns:
        Očišćeno ime fajla
    """
    # Ukloni nedozvoljene karaktere
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Ukloni višestruke underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Ograniči dužinu
    if len(filename) > 200:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:200] + (f'.{ext}' if ext else '')
    
    return filename.strip('_')


def is_pdf_url(url: str) -> bool:
    """
    Provjerava da li URL verovatno vodi do PDF-a.
    
    Args:
        url: URL za provjeru
    
    Returns:
        True ako izgleda kao PDF URL
    """
    url_lower = url.lower()
    
    # Proveri ekstenziju
    if url_lower.endswith('.pdf'):
        return True
    
    # Proveri query parametre
    if 'pdf' in url_lower and ('download' in url_lower or 'view' in url_lower):
        return True
    
    # Proveri specifične paterne
    pdf_patterns = [
        r'\.pdf(\?|$)',
        r'/pdf/',
        r'type=pdf',
        r'format=pdf',
    ]
    
    for pattern in pdf_patterns:
        if re.search(pattern, url_lower):
            return True
    
    return False
