# Global Crisis Monitoring System  

## Overview  
The **Global Crisis Monitoring System** is a Python-based tool that fetches the latest news articles, analyzes crisis-related keywords, assigns severity scores, and visualizes the impact on an interactive world map.  

This tool helps in identifying potential global crises by leveraging **Natural Language Processing (NLP), sentiment analysis, and geolocation services**.

## Features  
- **Fetches** at least **100 news articles** using NewsAPI  
- **Extracts** key crisis-related terms using NLP  
- **Ranks** keywords by **frequency & linguistic severity**  
- **Scores** news articles based on **keywords, sentiment, and recency**  
- **Maps** crisis locations using **Folium & Geopy**  
- **Customizable** crisis keyword weightings  


## Installation  

### Clone the Repository  
```bash
git clone https://github.com/your-username/global-crisis-monitor.git  
cd global-crisis-monitor
```

### Install Dependencies
```bash
pip install -r requirements.txt
```
### Download NLP Models
Run the following command to download spaCy's English model:
```bash
python -m spacy download en_core_web_sm
```
Ensure NLTK dependencies are available:
```python
import nltk
nltk.download("vader_lexicon")
```

## Usage in Jupyter Notebook
Open a Jupyter Notebook and run the following:

### Fetch News
```python
import fetch_news
news_list = fetch_news.fetch_news(101)
print(f"Fetched {len(news_list)} news articles.")
```
### Extract Crisis Keywords
```python
import extract_keywords

top_keywords = extract_keywords.get_top_keywords(news_list)
print("Top Crisis Keywords by Frequency:")
for keyword, count in top_keywords:
    print(f"{keyword}: {count}")

top_severe_keywords = extract_keywords.get_keywords_by_severity(news_list)
print("\n Top Crisis Keywords by Linguistic Severity:")
for keyword, impact in top_severe_keywords:
    print(f"{keyword}: {impact:.3f}")

news_list = extract_keywords.get_crisis_signals(news_list)
print(news_list[:5])  # Display first 5 articles with extracted keywords
```
### Modify Crisis Weights
You can customize crisis keyword weights according to the top keywords you get  by editing crisis_weights.json before running the script.

Example format:

```json

{
    "war": 5,
    "protests": 4,
    "inflation": 3,
    "curfew": 2
}
```

### Calculate Crisis Score
```python
import calculate_crisis_score
crisis_weights= calculate_crisis_score.load_crisis_weights("crisis_words.json")
news_list_score = calculate_crisis_score.get_crisis_score(news_list, crisis_weights)
```
### Generate Crisis Map
```python
from crisis_mapper import process_news_data

df = process_news_data(news_list)
df.head()
```
This saves an interactive map as crisis_map.html.

## Outputs
- News Data (DataFrame)
- The processed data includes:
-- Title
-- Description
-- Published Date
-- Crisis Score
-- Extracted Location
-- Latitude & Longitude

- Interactive Crisis Map
-- Saved as crisis_map.html

- Displays crisis locations with markers
-- Red (Severe) | Orange (Moderate) | Blue (Low Impact)

## Future Improvements
- Expand to multiple news sources

- Improve location extraction accuracy

- Add real-time updates

- Integrate machine learning for trend prediction

