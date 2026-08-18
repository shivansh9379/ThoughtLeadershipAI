from backend.app.services.llm_service import generate


class AuthorityReviewerAgent:

    def run(self, article, research):

        title = article.get("title", "")
        subtitle = article.get("subtitle", "")
        content = article.get("article", "")
        takeaways = article.get("key_takeaways", [])

        research_summary = research.get(
            "research_summary", ""
        )

        trends = research.get(
            "trends", []
        )

        # -----------------------------------------
        # Build source context
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

            for source in trend.get("supporting_sources", []):

                source_context += f"""
Source Name: {source.get("source_name", "")}
URL: {source.get("source_url", "")}
Fact: {source.get("supporting_fact", "")}
"""

        # -----------------------------------------
        # Review Prompt
        # -----------------------------------------

        prompt = f"""
You are AGENT 4 — AUTHORITY REVIEWER AGENT
inside an AI Thought Leadership Engine.

Your job is to critically review a thought-leadership
article BEFORE publication.

You are NOT a writer.

You are an evidence, credibility, reasoning and
authority reviewer.

ARTICLE TITLE:
{title}

SUBTITLE:
{subtitle}

ARTICLE:
{content}

KEY TAKEAWAYS:
{takeaways}

RESEARCH SUMMARY:
{research_summary}

RESEARCH SOURCES:
{source_context}

Review the article for:

1. FACTUAL ACCURACY
   Identify claims that are unsupported, exaggerated,
   misleading, or potentially incorrect.

2. EVIDENCE QUALITY
   Check whether important claims are actually
   supported by the supplied research.

3. SOURCE ALIGNMENT
   Check whether claims accurately represent
   the supporting sources.

4. LOGICAL REASONING
   Identify leaps in reasoning, unsupported
   cause-and-effect claims, or overgeneralizations.

5. AUTHORITY
   Determine whether the article sounds like
   genuine thought leadership rather than generic
   AI commentary.

6. ORIGINALITY
   Identify whether the article contains a
   genuinely differentiated argument.

7. PRACTICAL VALUE
   Determine whether recommendations logically
   follow from the evidence.

8. OVERCLAIMS
   Flag statements that are too absolute.

IMPORTANT:

- Do NOT invent replacement sources.
- Do NOT invent statistics.
- Do NOT assume unsupported claims are true.
- Use ONLY the supplied research for factual verification.
- Clearly distinguish supported claims from interpretation.
- A strong opinion is acceptable when it is clearly
  presented as an argument.
- Flag claims that require verification rather than
  silently approving them.

For every important issue provide:

- The problematic claim
- Why it is problematic
- Severity
- Recommended action

Severity levels:

HIGH
MEDIUM
LOW

Also provide an overall authority score from 1-10.

Return ONLY valid JSON.

FORMAT:

{{
    "overall_score": 0,
    "publication_ready": false,
    "strengths": [
        ""
    ],
    "issues": [
        {{
            "claim": "",
            "problem": "",
            "severity": "HIGH",
            "recommended_action": ""
        }}
    ],
    "unsupported_claims": [
        ""
    ],
    "reasoning_issues": [
        ""
    ],
    "source_alignment": [
        {{
            "claim": "",
            "source": "",
            "supported": true,
            "comment": ""
        }}
    ],
    "authority_assessment": "",
    "required_changes": [
        ""
    ]
}}
"""

        print("\nSending article to Authority Reviewer Agent...")

        result = generate(prompt)

        if not result["success"]:

            return {
                "success": False,
                "error": result["error"]
            }

        print("\nAuthority Reviewer Agent completed.")

        return {
            "success": True,
            "data": result["data"]
        }


authority_reviewer_agent = AuthorityReviewerAgent()