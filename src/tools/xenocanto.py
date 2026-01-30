import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_bird_sounds_from_xenocanto(scientific_name: str, limit: int = 3):
    base_url = "https://xeno-canto.org/api/3/recordings"
    
    query = f'sp:"{scientific_name}" q:A'
    
    api_key = os.getenv("XENOCANTO_API_KEY")
    
    if not api_key:
        print("⚠️ Warning: XENOCANTO_API_KEY is missing in .env")
    
    params = {
        "query": query,
        "key": api_key
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"⚠️ API Error Code: {response.status_code}")
            print(f"⚠️ Request URL: {response.url}")
            
        response.raise_for_status()
        data = response.json()
        
        recordings = data.get("recordings", [])
        audio_urls = []
        
        for rec in recordings[:limit]:
            file_url = rec.get("file")
            if file_url:
                audio_urls.append(file_url)
                
        return audio_urls

    except Exception as e:
        print(f"Xeno-canto Sound Error: {e}")
        return []