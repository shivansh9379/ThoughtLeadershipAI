import os
from tavily import TavilyClient

from backend.app.config import TAVILY_API_KEY


client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query):

    try:

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            timeout=30
        )

        results = response.get("results", [])

        return {
            "success": True,
            "results": results
        }

    except Exception as e:

        print("\n******** WEB SEARCH ERROR ********")
        print(type(e))
        print(e)

        return {
            "success": False,
            "error": str(e)
        }