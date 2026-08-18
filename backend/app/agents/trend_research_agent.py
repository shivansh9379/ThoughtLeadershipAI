from backend.app.services.llm_service import generate
from backend.app.tools.web_search import search_web


class TrendResearchAgent:

    def run(self, opportunity):

        topic = opportunity.get("topic", "")
        content_gap = opportunity.get("content_gap", "")
        audience = opportunity.get("underserved_audience", "")
        unique_angle = opportunity.get("unique_angle", "")

        # Use only 2 focused searches to keep the pipeline fast
        queries = [
            f"{topic} latest AI developments 2026",
            f"{content_gap} research report AI careers"
        ]

        all_results = []

        # -----------------------------------------
        # WEB RESEARCH
        # -----------------------------------------

        for query in queries:

            print(f"\nSearching web: {query}")

            try:
                search_result = search_web(query)

                if search_result["success"]:
                    all_results.extend(search_result["results"])
                    print(
                        f"Found {len(search_result['results'])} results."
                    )
                else:
                    print(
                        f"Search failed: {search_result.get('error')}"
                    )

            except Exception as e:
                print(f"Search error: {e}")

        if not all_results:
            return {
                "success": False,
                "error": "No web research results found."
            }

        # -----------------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------------

        unique_results = {}

        for item in all_results:

            url = item.get("url")

            if url and url not in unique_results:
                unique_results[url] = item

        # -----------------------------------------
        # BUILD RESEARCH CONTEXT
        # -----------------------------------------

        research_context = ""

        for i, item in enumerate(
            list(unique_results.values())[:10],
            start=1
        ):

            research_context += f"""
SOURCE {i}

Title:
{item.get("title", "")}

Content:
{item.get("content", "")}

URL:
{item.get("url", "")}

"""

        print("\nWeb research completed.")
        print(f"Total unique sources: {len(unique_results)}")

        # -----------------------------------------
        # TREND ANALYSIS
        # -----------------------------------------

        prompt = f"""
You are AGENT 1 — TREND RESEARCH AGENT
inside an AI Thought Leadership Engine.

Selected opportunity:

Topic:
{topic}

Content Gap:
{content_gap}

Audience:
{audience}

Unique Angle:
{unique_angle}

Research:

{research_context}

Your job is to identify CURRENT developments that
strengthen or challenge this opportunity.

Look for:

- Recent developments
- Emerging trends
- Industry shifts
- Research findings
- Workplace changes
- New AI tools
- Business implications

Do NOT invent facts.

Separate facts from interpretation.

For every trend provide:

- topic
- why_it_matters
- who_it_impacts
- why_it_is_trending
- contrarian_insight
- storytelling_opportunity
- practical_takeaway
- supporting_sources

Each source must contain:

- source_name
- source_url
- supporting_fact

Return ONLY valid JSON.

Format:

{{
    "research_summary": "",
    "trends": [
        {{
            "topic": "",
            "why_it_matters": "",
            "who_it_impacts": "",
            "why_it_is_trending": "",
            "contrarian_insight": "",
            "storytelling_opportunity": "",
            "practical_takeaway": "",
            "supporting_sources": [
                {{
                    "source_name": "",
                    "source_url": "",
                    "supporting_fact": ""
                }}
            ]
        }}
    ]
}}
"""

        print("\nSending research to Gemini...")

        result = generate(prompt)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"]
            }

        print("\nTrend Research Agent completed.")

        return {
            "success": True,
            "data": result["data"]
        }


trend_research_agent = TrendResearchAgent()