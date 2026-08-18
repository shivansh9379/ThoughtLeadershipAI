from backend.app.services.llm_service import generate
from backend.app.tools.web_search import search_web


class ContentGapAgent:

    def run(self, topics, audience):

        # -----------------------------------------
        # 1. Research existing conversations
        # -----------------------------------------

        search_query = (
            f"{topics} {audience} AI careers future of work "
            f"professional development trends"
        )

        search_result = search_web(search_query)

        if not search_result["success"]:
            return {
                "success": False,
                "error": search_result["error"]
            }

        results = search_result["results"]

        web_context = ""

        for i, item in enumerate(results, start=1):

            web_context += f"""
SOURCE {i}
Title: {item.get("title")}
Content: {item.get("content")}
URL: {item.get("url")}
"""

        # -----------------------------------------
        # 2. Content Gap Analysis
        # -----------------------------------------

        prompt = f"""
You are AGENT 0 — CONTENT GAP AGENT
inside an AI Thought Leadership Engine.

Your objective is to identify valuable conversations
that are missing or poorly covered around the selected
thought leadership topics.

PRIMARY TOPICS:
{topics}

TARGET AUDIENCE:
{audience}

RESEARCH RESULTS:
{web_context}

Do NOT simply select the most popular trend.

Look specifically for:

1. Under-discussed topics
2. Poorly explained topics
3. Missing practical implications
4. Missing career implications
5. Missing audience-specific insights
6. Missing second-order effects
7. Contrarian opportunities

For each opportunity determine:

- Topic
- Content Gap
- Why Existing Content Is Incomplete
- Underserved Audience
- Unique Angle
- Supporting Evidence
- Thought Leadership Potential (1-10)
- Authority Potential (1-10)
- Suggested Story Angle
- Suggested Title

Ranking formula:

40% Content Gap Size
25% Authority Potential
20% Audience Relevance
15% Trend Momentum

Return ONLY valid JSON.

JSON format:

{{
    "opportunities": [
        {{
            "topic": "",
            "content_gap": "",
            "why_existing_content_is_incomplete": "",
            "underserved_audience": "",
            "unique_angle": "",
            "supporting_evidence": [],
            "thought_leadership_potential": 0,
            "authority_potential": 0,
            "suggested_story_angle": "",
            "suggested_title": "",
            "ranking_score": 0
        }}
    ],
    "selected_opportunity": {{
        "topic": "",
        "content_gap": "",
        "why_existing_content_is_incomplete": "",
        "underserved_audience": "",
        "unique_angle": "",
        "supporting_evidence": [],
        "thought_leadership_potential": 0,
        "authority_potential": 0,
        "suggested_story_angle": "",
        "suggested_title": "",
        "ranking_score": 0
    }}
}}
"""

        result = generate(prompt)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"]
            }

        return {
            "success": True,
            "data": result["data"]
        }


content_gap_agent = ContentGapAgent()