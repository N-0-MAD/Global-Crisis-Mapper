import pandas as pd
import folium
import spacy
import time
from geopy.geocoders import Nominatim

nlp = spacy.load("en_core_web_sm")

geolocator = Nominatim(user_agent="geo_news")

def extract_location(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    return locations[0] if locations else None

def get_location_coordinates(place_name):
    try:
        if not place_name:
            return None, None
        location = geolocator.geocode(place_name, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geolocation error for {place_name}: {e}")
    return None, None

def process_news_data(news_list):
    for news in news_list:
        title = news.get("title", "")
        description = news.get("description", "")

        location_name = extract_location(title + " " + description)
        news["location_name"] = location_name

        if location_name:
            lat, lon = get_location_coordinates(location_name)
            news["latitude"], news["longitude"] = lat, lon
            time.sleep(1)  

    df = pd.DataFrame(news_list)

    world_map = folium.Map(location=[20, 0], zoom_start=2)

    for _, row in df.dropna(subset=["latitude", "longitude"]).iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['title']} - Severity: {row.get('crisis_score', 'N/A')}",
            icon=folium.Icon(color="red" if row.get("crisis_score", 0) > 7 else "orange" if row.get("crisis_score", 0) > 4 else "blue"),
        ).add_to(world_map)

    world_map.save("crisis_map.html")
    print("Crisis map saved! Open 'crisis_map.html' to view.")

    return df

if __name__ == "__main__":
    news_list = [
        {"title": "Explosion in Paris", "description": "A massive explosion occurred downtown.", "crisis_score": 8},
        {"title": "US-China Trade War Escalates", "description": "Tariffs increased on both sides.", "crisis_score": 5},
        {"title": "Mass Protests in Brazil", "description": "Thousands march against the new law.", "crisis_score": 6},
    ]

    df_result = process_news_data(news_list)
    print(df_result)
