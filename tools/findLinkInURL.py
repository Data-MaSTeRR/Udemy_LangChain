# 목적: 이름 -> linkedin URL

from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    """Searches for LinkedIn or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")

    return res[0]["url"] # 첫번째 응답의 "url"만 가져올 것임
