import wikipedia

def get_wiki_data(query: str, lang: str = "en"):
    wikipedia.set_lang(lang)
    
    search_results = wikipedia.search(query)
    
    if not search_results:
        return None
        
    target_page_title = search_results[0]
    page = wikipedia.page(target_page_title, auto_suggest=False)
    
    return page.content