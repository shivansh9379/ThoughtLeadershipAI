from backend.app.services.llm_service import generate


class HumanizationAgent:

    def run(self, article, review):

        title = article.get("title", "")
        subtitle = article.get("subtitle", "")
        content = article.get("article", "")
        takeaways = article.get("key_takeaways", [])
        cta = article.get("recommended_cta", "")

        issues = review.get("issues", [])
        required_changes = review.get("required_changes", [])
        reasoning_issues = review.get("reasoning_issues", [])

        prompt = f"""
You are AGENT 5 — REVISION & HUMANIZATION AGENT
inside an AI Thought Leadership Engine.

Your job is to transform a machine-generated thought-leadership
article into a credible, natural, publication-ready article.

You must preserve the article's strongest original ideas,
especially its distinctive argument and framework.

ORIGINAL TITLE:
{title}

ORIGINAL SUBTITLE:
{subtitle}

ORIGINAL ARTICLE:
{content}

KEY TAKEAWAYS:
{takeaways}

CTA:
{cta}

AUTHORITY REVIEW:

ISSUES:
{issues}

REQUIRED CHANGES:
{required_changes}

REASONING ISSUES:
{reasoning_issues}


YOUR TASK:

1. Fix every HIGH and MEDIUM severity issue.
2. Fix LOW severity issues where practical.
3. Remove unsupported absolute claims.
4. Clearly distinguish recommendations and heuristics
   from established industry facts.
5. Do not invent statistics.
6. Do not invent sources.
7. Do not introduce new factual claims that are not
   supported by the original article or review.
8. Preserve the central argument.
9. Preserve the Synthetic Triage Loop framework.
10. Make the article sound written by an experienced
    human thought leader.
11. Remove robotic or repetitive wording.
12. Avoid excessive AI buzzwords.
13. Avoid exaggerated phrases such as:
    "officially obsolete",
    "completely vanished",
    "everyone",
    "always",
    "never",
    unless genuinely justified.
14. Improve transitions between sections.
15. Keep the article intellectually strong.
16. Do not make the article bland merely to make it safe.
17. Maintain a confident but evidence-aware tone.
18. Do not mention that AI wrote or revised the article.
19. Do not mention this review process.

IMPORTANT:

The goal is NOT simply to shorten the article.

The goal is:

STRONG ARGUMENT
+
EVIDENCE-AWARE CLAIMS
+
HUMAN WRITING
+
PRACTICAL VALUE
=
PUBLICATION-READY THOUGHT LEADERSHIP


Return ONLY valid JSON.

FORMAT:

{{
    "title": "",
    "subtitle": "",
    "article": "",
    "key_takeaways": [
        ""
    ],
    "recommended_cta": "",
    "revision_summary": [
        ""
    ]
}}
"""

        print("\nSending article to Revision & Humanization Agent...")

        result = generate(prompt)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"]
            }

        print("\nRevision & Humanization Agent completed.")

        return {
            "success": True,
            "data": result["data"]
        }


humanization_agent = HumanizationAgent()