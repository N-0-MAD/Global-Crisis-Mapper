from collections import Counter, defaultdict
import nltk
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")

def extract_crisis_keywords(text):

    if not text:
        return []

    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]

    crisis_keywords = list(set(entities + keywords))

    return crisis_keywords

def get_crisis_signals(news_list):
  for news in news_list:
    title = news.get("title", "")
    description = news.get("description", "")
    text_to_analyze = title + " " + (description if description is not None else "")
    news["crisis_signals"] = extract_crisis_keywords(text_to_analyze)
  return news_list

def get_top_keywords(news_list, num_keywords=30):
    
    news_list = get_crisis_signals(news_list)
    all_keywords = [keyword for news in news_list for keyword in news.get("crisis_signals", [])]
    keyword_counts = Counter(all_keywords)
    return keyword_counts.most_common(num_keywords)

def get_keywords_by_severity(news_list, num_keywords=100):
    
    keyword_severity = defaultdict(float)
    
    for news in news_list:
        for keyword in news.get("crisis_signals", []):
            severity = abs(sia.polarity_scores(keyword)["compound"])  # Get sentiment strength
            keyword_severity[keyword] += severity  # Accumulate severity scores
    
    sorted_keywords = sorted(keyword_severity.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:num_keywords]


