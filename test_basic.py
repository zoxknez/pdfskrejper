"""
Test skripta - proverava osnovnu funkcionalnost.
"""

import asyncio
import sys

async def test_imports():
    """Test importovanja modula."""
    print("Testing imports...")
    try:
        from config.sources import SourceType, get_sources_by_type
        from config.settings import Settings
        from scrapers import BooksScraper, ResearchScraper
        from utils.logger import setup_logger
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

async def test_configuration():
    """Test konfiguracije."""
    print("\nTesting configuration...")
    try:
        from config.sources import SourceType, get_sources_by_type
        from config.settings import Settings
        
        # Test sources
        sources = get_sources_by_type(SourceType.RESEARCH)
        print(f"✓ Found {len(sources)} research sources")
        
        # Test settings
        Settings.create_directories()
        print(f"✓ Created directories")
        print(f"  - Storage: {Settings.STORAGE_DIR}")
        print(f"  - Output: {Settings.OUTPUT_DIR}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

async def test_scraper_creation():
    """Test kreiranja scraper-a."""
    print("\nTesting scraper creation...")
    try:
        from config.sources import SourceType, get_sources_by_type
        from scrapers import ResearchScraper
        
        sources = get_sources_by_type(SourceType.RESEARCH)
        if sources:
            source = sources[0]
            scraper = ResearchScraper(
                source=source,
                max_results=5
            )
            print(f"✓ Created scraper for: {source.name}")
            return True
        else:
            print("✗ No sources available")
            return False
    except Exception as e:
        print(f"✗ Scraper creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("="*60)
    print("PDF SCRAPER - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(await test_imports())
    results.append(await test_configuration())
    results.append(await test_scraper_creation())
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
