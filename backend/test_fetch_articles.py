"""
Quick test script for NewsFetcher.fetch_articles()

Run from backend directory: python test_fetch_articles.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from services.news_fetcher import NewsFetcher


def main():
    print("=" * 70)
    print("Testing NewsFetcher.fetch_articles()")
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
    
    print("\n" + "-" * 70)
    print("Fetching articles (category='technology', page_size=100)...")
    print("-" * 70)
    
    # Test fetch
    try:
        articles = fetcher.fetch_articles(category="technology", page_size=100)
        
        print(f"\n✅ Success! Fetched {len(articles)} articles\n")
        
        if not articles:
            print("⚠️  No articles returned")
            return
        
        # Show first article details
        print("📄 First Article Details:")
        print("-" * 70)
        article = articles[0]
        
        print(f"Title:      {article.get('title', 'N/A')}")
        print(f"Source:     {article.get('source', 'N/A')}")
        print(f"Unique ID:  {article.get('unique_id', 'N/A')}")
        print(f"Category:   {article.get('category', 'N/A')}")
        print(f"Published:  {article.get('publishedAt', 'N/A')}")
        print(f"URL:        {article.get('url', 'N/A')[:60]}...")
        content_length = len(article.get('content', ''))
        print(f"Content:    {content_length} characters")
        if content_length > 0:
            print(f"Content preview: {article.get('content', '')[:150]}...")
        print(f"\n⚠️  Note: NewsAPI only provides ~200 char snippets, not full articles.")
        print(f"   To get full content, fetch from the article URL.")
        
        # Validate structure
        required = ["unique_id", "title", "content", "source", "publishedAt", "url", "category"]
        missing = [f for f in required if f not in article]
        
        print("\n" + "-" * 70)
        if not missing:
            print("✅ All required fields present")
        else:
            print(f"❌ Missing fields: {missing}")
        
        # Check unique_id format
        unique_id = article.get('unique_id', '')
        if '||' in unique_id:
            print("✅ unique_id format correct (title||source)")
        else:
            print(f"⚠️  unique_id format unexpected: {unique_id[:50]}...")
        
        # Check for duplicates
        unique_ids = [a.get('unique_id') for a in articles]
        duplicates = len(unique_ids) - len(set(unique_ids))
        if duplicates == 0:
            print("✅ No duplicate unique_ids in batch")
        else:
            print(f"⚠️  Found {duplicates} duplicate unique_ids")
        
        # Show sample of article titles (first 10)
        print("\n" + "-" * 70)
        print(f"📋 Sample Articles (showing first 10 of {len(articles)}):")
        print("-" * 70)
        for i, art in enumerate(articles[:10], 1):
            print(f"{i}. {art.get('title', 'N/A')[:60]}...")
            print(f"   Source: {art.get('source', 'N/A')} | Content: {len(art.get('content', ''))} chars")
        
        if len(articles) > 10:
            print(f"\n... and {len(articles) - 10} more articles")
        
        # Verify we got close to 100
        print("\n" + "-" * 70)
        if len(articles) >= 90:
            print(f"✅ Successfully fetched {len(articles)} articles (target was 100)")
        elif len(articles) >= 50:
            print(f"⚠️  Fetched {len(articles)} articles (target was 100, may be limited by available articles)")
        else:
            print(f"⚠️  Only fetched {len(articles)} articles (target was 100)")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
