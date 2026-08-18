from backend.app.services.llm_service import generate


class InsightExtractionAgent:

    def run(self, opportunity, research):

        # -----------------------------------------
        # Extract inputs
        # -----------------------------------------

        topic = opportunity.get("topic", "")
        content_gap = opportunity.get("content_gap", "")
        unique_angle = opportunity.get("unique_angle", "")
        audience = opportunity.get("underserved_audience", "")

        research_summary = research.get(
            "research_summary", ""
        )

        trends = research.get(
            "trends", []
        )

        # -----------------------------------------
        # Build trend context
        # -----------------------------------------

        trend_context = ""

        for i, trend in enumerate(trends, start=1):

            trend_context += f"""
TREND {i}

Topic:
{trend.get("topic", "")}

Why It Matters:
{trend.get("why_it_matters", "")}

Who It Impacts:
{trend.get("who_it_impacts", "")}

Why It Is Trending:
{trend.get("why_it_is_trending", "")}

Contrarian Insight:
{trend.get("contrarian_insight", "")}

Storytelling Opportunity:
{trend.get("storytelling_opportunity", "")}

Practical Takeaway:
{trend.get("practical_takeaway", "")}

"""

        # -----------------------------------------
        # Insight Extraction Prompt
        # -----------------------------------------

        prompt = f"""
You are AGENT 2 — INSIGHT EXTRACTION AGENT
inside an AI Thought Leadership Engine.

Your job is NOT to summarize the research.

Your job is to answer:

"SO WHAT?"

You must transform research and trends into
original, actionable thought leadership insights.

SELECTED OPPORTUNITY

Topic:
{topic}

Content Gap:
{content_gap}

Unique Angle:
{unique_angle}

Target Audience:
{audience}

RESEARCH SUMMARY:
{research_summary}

TRENDS:
{trend_context}

Analyze the material and identify:

1. Core Insight
   What is the most important non-obvious lesson?

2. Second-Order Effects
   What happens because of these trends?

3. Contrarian Perspective
   What common assumption should leaders
   reconsider?

4. Audience Implication
   What does this specifically mean for the
   target audience?

5. Practical Implications
   What should the audience actually do?

6. Original Framework
   Create a simple framework, model, or mental
   model that can explain the insight.

7. Evidence
   Connect important claims to the research.

8. Core Thesis
   Create ONE strong statement that could become
   the central argument of a thought leadership post.

IMPORTANT:

- Do not simply repeat the research.
- Do not invent statistics.
- Do not invent sources.
- Clearly distinguish evidence from interpretation.
- Prefer deeper second-order implications.
- Avoid generic statements like "AI is changing
  the world."
- The insight must be useful to the target audience.
- The final thesis should be debatable and
  thought-provoking rather than obvious.

Return ONLY valid JSON.

FORMAT:

{{
    "core_insight": "",
    "second_order_effects": [
        ""
    ],
    "contrarian_perspective": "",
    "audience_implication": "",
    "practical_implications": [
        ""
    ],
    "original_framework": {{
        "name": "",
        "description": "",
        "steps": [
            {{
                "step": "",
                "explanation": ""
            }}
        ]
    }},
    "evidence": [
        {{
            "claim": "",
            "source": "",
            "source_url": ""
        }}
    ],
    "core_thesis": ""
}}
"""

        # -----------------------------------------
        # Generate insights
        # -----------------------------------------

        print("\nSending research to Insight Extraction Agent...")

        result = generate(prompt)

        if not result["success"]:

            return {
                "success": False,
                "error": result["error"]
            }

        print("\nInsight Extraction Agent completed.")

        return {
            "success": True,
            "data": result["data"]
        }


insight_extraction_agent = InsightExtractionAgent()