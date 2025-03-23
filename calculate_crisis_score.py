import json
from textblob import TextBlob
from datetime import datetime

def load_crisis_weights(config_path):
    try:
        with open(config_path, "r") as file:
            crisis_weights = json.load(file)
        return crisis_weights
    except Exception as e:
        print(f"Error loading crisis weights: {e}")
        return {}

def calculate_crisis_score(news, crisis_weights):
    
    crisis_signals = news.get("crisis_signals", [])
    base_score = sum(crisis_weights.get(word.lower(), 1) for word in crisis_signals)
    base_score /= len(crisis_signals) if crisis_signals else 1  # Normalize for long keyword lists

    # Sentiment Analysis
    description = news.get("description", "")
    sentiment = TextBlob(description).sentiment.polarity if description else 0
    sentiment_boost = (1 - sentiment) * 5  # Negative sentiment boosts crisis severity

    published_date = datetime.strptime(news["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    days_old = (datetime.utcnow() - published_date).days
    recency_boost = max(10 - days_old, 0)  # Older crises lose impact

    final_score = base_score + sentiment_boost + recency_boost
    return round(final_score, 2)

def get_crisis_score(news_list, crisis_weights):
    for news in news_list:
        news["crisis_score"] = calculate_crisis_score(news, crisis_weights)
    return news_list  

    

