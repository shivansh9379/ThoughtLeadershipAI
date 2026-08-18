from backend.app.services.llm_service import generate


class FinalEditorAgent:

    def run(self, article, research, review):

        title = article.get("title", "")
        subtitle = article.get("subtitle", "")
        content = article.get("article", "")
        takeaways = article.get("key_takeaways", [])
        cta = article.get("recommended_cta", "")

        research_summary = research.get(
            "research_summary", ""
        )

        trends = research.get(
            "trends", []
        )

        issues = review.get(
            "issues", []
        )

        required_changes = review.get(
            "required_changes", []
        )

        # -----------------------------------------
        # BUILD SOURCE CONTEXT
        # -----------------------------------------

        source_context = ""

        for i, trend in enumerate(trends, start=1):

            source_context += f"""
TREND {i}:
{trend.get("topic", "")}

WHY IT MATTERS:
{trend.get("why_it_matters", "")}

SUPPORTING SOURCES:
"""

            for source in trend.get(
                "supporting_sources", []
            ):

                source_context += f"""
Source Name:
{source.get("source_name", "")}

Source URL:
{source.get("source_url", "")}

Supporting Fact:
{source.get("supporting_fact", "")}
"""

        # -----------------------------------------
        # FINAL EDITOR PROMPT
        # -----------------------------------------

        prompt = f"""
You are AGENT 6 — FINAL EDITOR AGENT
inside an AI Thought Leadership Engine.

Your job is to produce the FINAL publication-ready
version of a thought-leadership article.

You are the final quality gate before publication.

Do NOT completely rewrite the author's argument.

Preserve the strongest original insight,
framework, evidence and point of view.

ARTICLE TITLE:
{title}

SUBTITLE:
{subtitle}

ARTICLE:
{content}

KEY TAKEAWAYS:
{takeaways}

CTA:
{cta}

RESEARCH SUMMARY:
{research_summary}

RESEARCH SOURCES:
{source_context}

AUTHORITY REVIEW ISSUES:
{issues}

REQUIRED CHANGES:
{required_changes}


FINAL EDITING REQUIREMENTS:

1. Improve readability.

2. Improve narrative flow.

3. Strengthen the opening hook.

4. Remove unnecessary repetition.

5. Remove generic AI-sounding language.

6. Remove unnecessary jargon.

7. Keep the argument intellectually strong.

8. Preserve evidence-backed claims.

9. Do not invent statistics.

10. Do not invent sources.

11. Do not introduce unsupported factual claims.

12. Clearly distinguish facts from interpretation.

13. Keep the writing conversational and professional.

14. Make the article feel written by an experienced
professional.

15. Preserve the central argument and unique insight.

16. Keep practical recommendations.

17. Make the conclusion memorable without being
sensational.

18. Avoid engagement bait.

19. Avoid phrases such as:
    "In today's rapidly changing world"
    "The future is here"
    "AI is revolutionizing everything"
    "game changer"
    "paradigm shift"

20. Avoid excessive use of:
    AI
    transformation
    revolution
    unprecedented
    leverage
    ecosystem

unless genuinely necessary.

21. Do not mention the agents.

22. Do not mention this editing process.

23. Do not mention that AI generated the article.

24. Keep the article suitable for LinkedIn.

25. Maintain short readable paragraphs.

FINAL QUALITY TEST:

Ask:

"Would a smart professional learn something
new from this?"

If not, improve the article.


Also generate:

- A strong final headline
- A concise subtitle
- One-sentence core insight
- A professional CTA
- 5-8 relevant hashtags
- Key takeaways
- Sources and references


SOURCE REQUIREMENTS:

Only use sources supplied in the research.

For each source provide:

- source_name
- source_url
- supporting_fact

Do not invent publication dates.
If a publication date is unavailable,
return an empty string.


RETURN ONLY VALID JSON.

FORMAT:

{{
    "headline": "",
    "subtitle": "",
    "article": "",
    "core_insight": "",
    "key_takeaways": [
        ""
    ],
    "cta": "",
    "hashtags": [
        ""
    ],
    "sources": [
        {{
            "source_name": "",
            "source_url": "",
            "publication_date": "",
            "supporting_fact": ""
        }}
    ]
}}
"""

        print("\nSending article to Final Editor Agent...")

        result = generate(prompt)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"]
            }

        print("\nFinal Editor Agent completed.")

        return {
            "success": True,
            "data": result["data"]
        }


final_editor_agent = FinalEditorAgent()