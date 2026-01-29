import requests

def get_bird_photos_from_inaturalist(scientific_name: str, limit: int = 5):
    base_url = "https://api.inaturalist.org/v1/observations"
    
    params = {
        "taxon_name": scientific_name,
        "photos": "true",
        "per_page": limit,
        "quality_grade": "research",
        "order_by": "votes"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        photo_urls = []
        
        for obs in results:
            if obs.get("photos"):
                photo_data = obs["photos"][0]
                url = photo_data.get("url")
                
                if url:
                    high_res_url = url.replace("square", "medium")
                    photo_urls.append(high_res_url)
                    
        return photo_urls

    except Exception as e:
        print(f"iNaturalist Photo Error: {e}")
        return []
