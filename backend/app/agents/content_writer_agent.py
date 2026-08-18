from backend.app.services.llm_service import generate


class ContentWriterAgent:

    def run(self, opportunity, research, insights):

        topic = opportunity.get("topic", "")
        audience = opportunity.get("underserved_audience", "")
        unique_angle = opportunity.get("unique_angle", "")
        suggested_title = opportunity.get("suggested_title", "")

        research_summary = research.get(
            "research_summary", ""
        )

        trends = research.get(
            "trends", []
        )

        core_insight = insights.get(
            "core_insight", ""
        )

        contrarian_perspective = insights.get(
            "contrarian_perspective", ""
        )

        practical_implications = insights.get(
            "practical_implications", []
        )

        framework = insights.get(
            "original_framework", {}
        )

        core_thesis = insights.get(
            "core_thesis", ""
        )

        prompt = f"""
You are AGENT 3 — CONTENT WRITER AGENT
inside an AI Thought Leadership Engine.

Your job is to turn research and extracted insights
into a strong thought-leadership article.

TOPIC:
{topic}

TARGET AUDIENCE:
{audience}

UNIQUE ANGLE:
{unique_angle}

SUGGESTED TITLE:
{suggested_title}

RESEARCH SUMMARY:
{research_summary}

CORE INSIGHT:
{core_insight}

CONTRARIAN PERSPECTIVE:
{contrarian_perspective}

CORE THESIS:
{core_thesis}

PRACTICAL IMPLICATIONS:
{practical_implications}

ORIGINAL FRAMEWORK:
{framework}

TRENDS:
{trends}

WRITING REQUIREMENTS:

1. Write an authoritative thought-leadership article.
2. Make the argument clear from the beginning.
3. Do not merely summarize the research.
4. Build a logical narrative.
5. Explain the second-order consequences.
6. Include the original framework naturally.
7. Give practical recommendations.
8. Use evidence where appropriate.
9. Avoid generic AI hype.
10. Avoid repetitive statements.
11. Do not invent statistics or sources.
12. Clearly distinguish opinion from evidence.
13. Write for an intelligent professional audience.
14. Make the article useful enough to act on.

STRUCTURE:

- Strong headline
- Opening hook
- The problem
- Why the conventional view is incomplete
- What is actually changing
- Second-order consequences
- The contrarian argument
- Original framework
- Practical recommendations
- Closing insight

STYLE:

- Clear
- Intelligent
- Professional
- Thought-provoking
- Specific
- Natural
- No unnecessary jargon

Return ONLY valid JSON.

FORMAT:

{{
    "title": "",
    "subtitle": "",
    "article": "",
    "key_takeaways": [
        ""
    ],
    "recommended_cta": ""
}}
"""

        print("\nSending content to Content Writer Agent...")

        result = generate(prompt)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"]
            }

        print("\nContent Writer Agent completed.")

        return {
            "success": True,
            "data": result["data"]
        }


content_writer_agent = ContentWriterAgent()