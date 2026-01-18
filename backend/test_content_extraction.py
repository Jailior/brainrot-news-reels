import backend.services.news_fetcher as NewFetcher

test_fetch = NewFetcher.NewsFetcher()

output = test_fetch.fetch_articles()
print(output)