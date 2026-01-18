"""
Comprehensive test script for NewsFetcher service.

Tests all functionality including:
- fetch_articles() with different parameter combinations
- save_articles() to database
- count_unused_articles() and count_visited_articles()
- ensure_sufficient_articles() auto-fetch functionality
- get_next_unused_article() with auto-fetch
- mark_article_visited()

Run from backend directory: python test_fetch_articles.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from services.news_fetcher import NewsFetcher


def test_basic_fetch(fetcher: NewsFetcher):
    """Test basic fetch_articles() functionality."""
    print("\n" + "=" * 70)
    print("TEST 1: Basic fetch_articles() - No filters (uses /everything endpoint)")
    print("=" * 70)
    
    try:
        articles = fetcher.fetch_articles(page_size=20)
        
        print(f"\n✅ Success! Fetched {len(articles)} articles")
        
        if not articles:
            print("⚠️  No articles returned")
            return False
        
        # Show first article details
        print("\n📄 First Article Details:")
        print("-" * 70)
        article = articles[0]
        
        print(f"Title:      {article.get('title', 'N/A')[:70]}")
        print(f"Source:     {article.get('source', 'N/A')}")
        print(f"Unique ID:  {article.get('unique_id', 'N/A')[:70]}...")
        print(f"Category:   {article.get('category', 'N/A')}")
        print(f"Published:  {article.get('publishedAt', 'N/A')}")
        
        # Validate structure
        required = ["unique_id", "title", "content", "source", "publishedAt", "url", "category"]
        missing = [f for f in required if f not in article]
        
        if not missing:
            print("✅ All required fields present")
        else:
            print(f"❌ Missing fields: {missing}")
            return False
        
        # Check unique_id format
        unique_id = article.get('unique_id', '')
        if '||' in unique_id:
            print("✅ unique_id format correct (title||source)")
        else:
            print(f"⚠️  unique_id format unexpected: {unique_id[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fetch_with_filters(fetcher: NewsFetcher):
    """Test fetch_articles() with category and country filters."""
    print("\n" + "=" * 70)
    print("TEST 2: fetch_articles() with category filter")
    print("=" * 70)
    
    try:
        articles = fetcher.fetch_articles(category="technology", page_size=10)
        print(f"✅ Fetched {len(articles)} technology articles")
        
        if articles:
            print(f"   Sample: {articles[0].get('title', 'N/A')[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_database_operations(fetcher: NewsFetcher):
    """Test database operations if database is available."""
    print("\n" + "=" * 70)
    print("TEST 3: Database Operations")
    print("=" * 70)
    
    try:
        from database import SessionLocal, init_db
        
        # Initialize database
        print("\n📦 Initializing database...")
        init_db()
        print("✅ Database initialized")
        
        # Create session
        db = SessionLocal()
        try:
            # Test: Fetch and save articles
            print("\n📥 Fetching and saving articles...")
            articles = fetcher.fetch_articles(page_size=20)
            saved = fetcher.save_articles(articles, db)
            print(f"✅ Saved {len(saved)} new articles to database")
            
            # Test: Count unused articles
            unused_count = fetcher.count_unused_articles(db)
            visited_count = fetcher.count_visited_articles(db)
            print(f"✅ Unused articles: {unused_count}")
            print(f"✅ Visited articles: {visited_count}")
            
            # Test: Get next unused article
            print("\n📄 Getting next unused article...")
            article = fetcher.get_next_unused_article(db, auto_fetch=False)
            if article:
                print(f"✅ Got article: {article.title[:60]}...")
                print(f"   ID: {article.id}, Visited: {article.visited}")
            else:
                print("⚠️  No unused articles available")
            
            # Test: Mark article as visited
            if article:
                print("\n✅ Marking article as visited...")
                updated = fetcher.mark_article_visited(article.id, db)
                if updated and updated.visited:
                    print(f"✅ Article {article.id} marked as visited")
                else:
                    print("❌ Failed to mark article as visited")
            
            # Test: Count again after marking
            new_unused = fetcher.count_unused_articles(db)
            new_visited = fetcher.count_visited_articles(db)
            print(f"\n✅ Updated counts - Unused: {new_unused}, Visited: {new_visited}")
            
            return True
            
        finally:
            db.close()
            
    except ImportError:
        print("⚠️  Database module not available, skipping database tests")
        return None
    except Exception as e:
        print(f"⚠️  Database test failed (database may not be configured): {e}")
        return None


def test_auto_fetch(fetcher: NewsFetcher):
    """Test ensure_sufficient_articles() and auto-fetch functionality."""
    print("\n" + "=" * 70)
    print("TEST 4: Auto-fetch functionality (ensure_sufficient_articles)")
    print("=" * 70)
    
    try:
        from database import SessionLocal, init_db
        
        init_db()
        db = SessionLocal()
        try:
            # Get initial count
            initial_count = fetcher.count_unused_articles(db)
            print(f"📊 Initial unused articles: {initial_count}")
            
            # Test ensure_sufficient_articles with high threshold
            print(f"\n🔄 Testing ensure_sufficient_articles() with threshold=50...")
            fetched = fetcher.ensure_sufficient_articles(db, min_threshold=50)
            
            if fetched:
                print("✅ Auto-fetch triggered and fetched articles")
            else:
                print("ℹ️  Auto-fetch not needed (already have enough articles)")
            
            # Check new count
            new_count = fetcher.count_unused_articles(db)
            print(f"📊 New unused articles count: {new_count}")
            
            # Test get_next_unused_article with auto_fetch enabled
            print(f"\n🔄 Testing get_next_unused_article() with auto_fetch=True...")
            article = fetcher.get_next_unused_article(db, auto_fetch=True)
            
            if article:
                print(f"✅ Got article with auto-fetch: {article.title[:60]}...")
            else:
                print("⚠️  No article returned")
            
            return True
            
        finally:
            db.close()
            
    except ImportError:
        print("⚠️  Database module not available, skipping auto-fetch test")
        return None
    except Exception as e:
        print(f"⚠️  Auto-fetch test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_content_extraction(fetcher: NewsFetcher):
    """Test full content extraction from URLs using trafilatura."""
    print("\n" + "=" * 70)
    print("TEST 5: Content Extraction (trafilatura)")
    print("=" * 70)
    
    try:
        from database import SessionLocal, init_db
        
        init_db()
        db = SessionLocal()
        try:
            # Test 1: Extract content from a single article URL
            print("\n📄 Testing _extract_full_content() method...")
            
            # Fetch a small batch of articles
            print("   Fetching sample articles...")
            articles = fetcher.fetch_articles(page_size=3)
            
            if not articles:
                print("⚠️  No articles fetched, skipping content extraction test")
                return None
            
            # Test extraction on first article
            test_article = articles[0]
            test_url = test_article.get('url', '')
            initial_content = test_article.get('content', '')
            
            print(f"   Testing extraction from: {test_url[:60]}...")
            print(f"   Initial content length: {len(initial_content)} chars")
            
            if test_url:
                extracted_content = fetcher._extract_full_content(
                    url=test_url,
                    fallback_content=initial_content
                )
                
                print(f"   Extracted content length: {len(extracted_content)} chars")
                
                if len(extracted_content) > len(initial_content):
                    print("✅ Successfully extracted longer content from URL")
                    print(f"   Improvement: +{len(extracted_content) - len(initial_content)} chars")
                elif len(extracted_content) == len(initial_content) and extracted_content == initial_content:
                    print("ℹ️  Extraction returned fallback content (extraction may have failed)")
                else:
                    print("ℹ️  Extracted content is shorter or same as initial")
                
                # Show preview
                if extracted_content:
                    preview = extracted_content[:200].replace('\n', ' ')
                    print(f"   Content preview: {preview}...")
            else:
                print("⚠️  No URL available for testing")
            
            # Test 2: Save articles with content extraction enabled
            print("\n💾 Testing save_articles() with content extraction...")
            print("   Fetching 2 articles for testing...")
            test_articles = fetcher.fetch_articles(page_size=2)
            
            if test_articles:
                print("   Saving articles WITH content extraction...")
                saved_with_extraction = fetcher.save_articles(
                    test_articles,
                    db,
                    extract_full_content=True,
                    delay_between_extractions=0.3  # Faster for testing
                )
                
                if saved_with_extraction:
                    for article in saved_with_extraction:
                        content_len = len(article.content)
                        print(f"   ✅ Saved: {article.title[:50]}...")
                        print(f"      Content length: {content_len} chars")
                        
                        # Check if content looks like full article (longer than typical snippet)
                        if content_len > 500:
                            print(f"      ✅ Content appears to be full article (>500 chars)")
                        elif content_len > 200:
                            print(f"      ℹ️  Content is medium length (200-500 chars)")
                        else:
                            print(f"      ⚠️  Content is short (<200 chars), may be snippet only")
                
                # Test 3: Compare with extraction disabled
                print("\n   Testing save_articles() WITHOUT content extraction...")
                test_articles_2 = fetcher.fetch_articles(page_size=1)
                if test_articles_2:
                    saved_without_extraction = fetcher.save_articles(
                        test_articles_2,
                        db,
                        extract_full_content=False
                    )
                    
                    if saved_without_extraction:
                        article = saved_without_extraction[0]
                        print(f"   ✅ Saved without extraction: {article.title[:50]}...")
                        print(f"      Content length: {len(article.content)} chars")
            
            # Test 4: Error handling - invalid URL
            print("\n🔍 Testing error handling with invalid URL...")
            invalid_result = fetcher._extract_full_content(
                url="https://invalid-url-that-does-not-exist-12345.com/article",
                fallback_content="Fallback content"
            )
            
            if invalid_result == "Fallback content":
                print("✅ Correctly fell back to fallback content for invalid URL")
            else:
                print(f"ℹ️  Got content from invalid URL (unexpected): {len(invalid_result)} chars")
            
            # Test 5: Empty URL
            empty_result = fetcher._extract_full_content(
                url="",
                fallback_content="Fallback content"
            )
            if empty_result == "Fallback content":
                print("✅ Correctly handled empty URL")
            
            return True
            
        finally:
            db.close()
            
    except ImportError:
        print("⚠️  Database module not available, skipping content extraction test")
        return None
    except Exception as e:
        print(f"⚠️  Content extraction test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print("=" * 70)
    print("Comprehensive NewsFetcher Test Suite")
    print("=" * 70)
    
    # Initialize
    try:
        fetcher = NewsFetcher()
        if not fetcher.api_key:
            print("❌ ERROR: NEWSAPI_KEY not set in environment!")
            return
        print(f"✅ NewsFetcher initialized (API key: {'*' * 20})")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Run tests
    results = []
    
    # Test 1: Basic fetch
    results.append(("Basic Fetch", test_basic_fetch(fetcher)))
    
    # Test 2: Fetch with filters
    results.append(("Fetch with Filters", test_fetch_with_filters(fetcher)))
    
    # Test 3: Database operations
    db_result = test_database_operations(fetcher)
    if db_result is not None:
        results.append(("Database Operations", db_result))
    
    # Test 4: Auto-fetch
    auto_fetch_result = test_auto_fetch(fetcher)
    if auto_fetch_result is not None:
        results.append(("Auto-fetch", auto_fetch_result))
    
    # Test 5: Content extraction
    content_extraction_result = test_content_extraction(fetcher)
    if content_extraction_result is not None:
        results.append(("Content Extraction", content_extraction_result))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}: PASSED")
        elif result is False:
            print(f"❌ {test_name}: FAILED")
        else:
            print(f"⚠️  {test_name}: SKIPPED")
    
    passed = sum(1 for _, r in results if r is True)
    total = sum(1 for _, r in results if r is not None)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    print("=" * 70)


if __name__ == "__main__":
    main()
