import wikipedia

def get_wiki_data(query: str, lang: str = "en"):
    wikipedia.set_lang(lang)
    
    try:
        search_results = wikipedia.search(query)
        
        if not search_results:
            return None
            
        target_page_title = search_results[0]
        try:
            page = wikipedia.page(target_page_title, auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            print(f"Wiki: Ambiguous term '{target_page_title}', trying first option: '{e.options[0]}'")
            try:
                page = wikipedia.page(e.options[0], auto_suggest=False)
            except Exception:
                return None
        except wikipedia.PageError:
            print(f"Wiki: Page '{target_page_title}' not found.")
            return None
        
        return page.content
        
    except Exception as e:
        print(f"Wiki: Error fetching data for '{query}': {e}")
        return None