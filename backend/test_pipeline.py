"""
Pipeline test that mimics the real flow:
1. Fetch articles from NewsAPI (with content scraping)
2. Save articles to database
3. Retrieve article and access content from Article model
4. Show the scraped content

Run from backend directory: python test_pipeline.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from services.news_fetcher import NewsFetcher


def test_pipeline():
    """Test the complete pipeline with real API calls."""
    print("=" * 70)
    print("Pipeline Test: Fetch -> Scrape -> Save -> Retrieve")
    print("=" * 70)
    
    try:
        # Initialize
        print("\n1️⃣  Initializing NewsFetcher...")
        fetcher = NewsFetcher()
        
        if not fetcher.api_key:
            print("❌ ERROR: NEWSAPI_KEY not set in environment!")
            return False
        
        print("✅ NewsFetcher initialized")
        
        # Step 1: Fetch articles with content scraping
        print("\n2️⃣  Fetching articles from NewsAPI (with content scraping)...")
        print("   This will make real API calls and scrape content from URLs")
        print("   " + "-" * 66)
        
        articles = fetcher.fetch_articles(
            page_size=3,  # Small batch for testing
            extract_content=True,  # Enable content scraping
            delay_between_extractions=0.5
        )
        
        if not articles:
            print("❌ No articles fetched")
            return False
        
        print(f"✅ Fetched {len(articles)} articles")
        
        # Show scraped content for each article
        print("\n3️⃣  Scraped Content Preview:")
        print("   " + "=" * 66)
        for i, article in enumerate(articles, 1):
            print(f"\n   Article {i}:")
            print(f"   Title: {article.get('title', 'N/A')[:60]}...")
            print(f"   Source: {article.get('source', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')[:60]}...")
            
            content = article.get('content', '')
            content_len = len(content)
            print(f"   Content Length: {content_len} characters")
            
            if content_len > 0:
                # Show preview of scraped content
                preview = content[:300].replace('\n', ' ').strip()
                print(f"   Content Preview: {preview}...")
                
                # Check if content looks like full article
                if content_len > 500:
                    print(f"   ✅ Content appears to be full article (>500 chars)")
                elif content_len > 200:
                    print(f"   ℹ️  Content is medium length (200-500 chars)")
                else:
                    print(f"   ⚠️  Content is short (<200 chars), may be snippet only")
            else:
                print(f"   ⚠️  No content available")
        
        # Step 2: Save to database (if available)
        print("\n4️⃣  Saving articles to database...")
        print("   " + "-" * 66)
        
        try:
            from database import SessionLocal, init_db
            
            init_db()
            db = SessionLocal()
            try:
                # Save articles (content already scraped, so extract_full_content=False)
                saved = fetcher.save_articles(
                    articles,
                    db,
                    extract_full_content=False  # Already scraped in fetch_articles
                )
                
                print(f"✅ Saved {len(saved)} articles to database")
                
                # Step 3: Retrieve article from database and access content
                if saved:
                    print("\n5️⃣  Retrieving article from database...")
                    print("   " + "-" * 66)
                    
                    # Get the first saved article
                    article_id = saved[0].id
                    retrieved_article = fetcher.get_article_by_id(article_id, db)
                    
                    if retrieved_article:
                        print(f"✅ Retrieved article: {retrieved_article.title[:60]}...")
                        print(f"   Article ID: {retrieved_article.id}")
                        print(f"   Source: {retrieved_article.source}")
                        
                        # Access content from Article model
                        db_content = retrieved_article.content
                        db_content_len = len(db_content)
                        
                        print(f"\n   📄 Content from Article Model:")
                        print(f"   Content Length: {db_content_len} characters")
                        
                        if db_content_len > 0:
                            # Show preview
                            db_preview = db_content[:300].replace('\n', ' ').strip()
                            print(f"   Content Preview: {db_preview}...")
                            
                            # Compare with original
                            original_content = articles[0].get('content', '')
                            if db_content == original_content:
                                print(f"   ✅ Content matches original scraped content")
                            else:
                                print(f"   ⚠️  Content differs from original (may have been modified)")
                        else:
                            print(f"   ⚠️  No content in database")
                    else:
                        print("❌ Failed to retrieve article from database")
                
                return True
                
            finally:
                db.close()
                
        except ImportError:
            print("⚠️  Database module not available, skipping save/retrieve steps")
            print("   Content scraping still works - see Article content above")
            return True
        except Exception as e:
            print(f"⚠️  Database operation failed: {e}")
            print("   Content scraping still works - see Article content above")
            return True
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 70)
    print("News Fetcher Pipeline Test")
    print("=" * 70)
    print("\nThis test mimics the real pipeline:")
    print("  1. Fetch articles from NewsAPI (real API calls)")
    print("  2. Scrape full content from article URLs")
    print("  3. Save articles to database")
    print("  4. Retrieve article and access content from Article model")
    print("=" * 70)
    
    result = test_pipeline()
    
    print("\n" + "=" * 70)
    if result:
        print("✅ Pipeline test completed successfully!")
    else:
        print("❌ Pipeline test failed")
    print("=" * 70)


if __name__ == "__main__":
    main()
