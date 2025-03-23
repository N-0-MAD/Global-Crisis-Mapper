import requests
import time

API_KEY = "64e39296283e430a802f0296bb24b5b5"
query = "economic collapse OR war OR riots OR protests OR pandemic OR lawsuit OR hijack OR bombing OR revolt OR curfew OR shutdown OR legislation OR Global Crisis OR Ban OR Strike"
url = "https://newsapi.org/v2/everything"

def fetch_news(max_articles=500):
    """Fetch at least `max_articles` news articles using pagination."""
    news_list = []
    page = 1
    page_size = 100  # Max allowed by NewsAPI

    while len(news_list) < max_articles:
        params = {
            "q": query,
            "language": "en",
            "apiKey": API_KEY,
            "pageSize": page_size,
            "page": page
        }
        response = requests.get(url, params=params)
        data = response.json()

        articles = data.get("articles", [])
        if not articles:
            break  # Stop if no more articles

        news_list.extend([
            {
                "title": article["title"].lower() if article.get("title") else "",
                "description": article["description"].lower() if article.get("description") else "",
                "publishedAt": article["publishedAt"]
            }
            for article in articles
        ])

        print(f"Fetched {len(news_list)} articles...")  # Debugging output
        page += 1
        time.sleep(1)  # Avoid rate limits

    return news_list[:max_articles]  # Trim to exact number

# Example usage
news_list = fetch_news(500)
print(f"Total articles fetched: {len(news_list)}")
