from backend.app.agents.content_gap_agent import content_gap_agent
from backend.app.agents.trend_research_agent import trend_research_agent
from backend.app.agents.insight_extraction_agent import (
    insight_extraction_agent
)
from backend.app.agents.content_writer_agent import (
    content_writer_agent
)
from backend.app.agents.authority_reviewer_agent import (
    authority_reviewer_agent
)
from backend.app.agents.humanization_agent import (
    humanization_agent
)
from backend.app.agents.final_editor_agent import (
    final_editor_agent
)


def generate_thought_leadership(
    topics: str,
    audience: str
):

    # =========================================
    # AGENT 0 — CONTENT GAP
    # =========================================

    print("\n========== AGENT 0: CONTENT GAP ==========")

    gap_result = content_gap_agent.run(
        topics=topics,
        audience=audience
    )

    if not gap_result["success"]:
        return {
            "success": False,
            "stage": "content_gap",
            "error": gap_result["error"]
        }

    opportunity = gap_result["data"]["selected_opportunity"]


    # =========================================
    # AGENT 1 — TREND RESEARCH
    # =========================================

    print("\n========== AGENT 1: TREND RESEARCH ==========")

    research_result = trend_research_agent.run(
        opportunity
    )

    if not research_result["success"]:
        return {
            "success": False,
            "stage": "trend_research",
            "error": research_result["error"]
        }

    research = research_result["data"]


    # =========================================
    # AGENT 2 — INSIGHT EXTRACTION
    # =========================================

    print("\n========== AGENT 2: INSIGHT EXTRACTION ==========")

    insight_result = insight_extraction_agent.run(
        opportunity=opportunity,
        research=research
    )

    if not insight_result["success"]:
        return {
            "success": False,
            "stage": "insight_extraction",
            "error": insight_result["error"]
        }

    insights = insight_result["data"]


    # =========================================
    # AGENT 3 — CONTENT WRITER
    # =========================================

    print("\n========== AGENT 3: CONTENT WRITER ==========")

    writer_result = content_writer_agent.run(
        opportunity=opportunity,
        research=research,
        insights=insights
    )

    if not writer_result["success"]:
        return {
            "success": False,
            "stage": "content_writer",
            "error": writer_result["error"]
        }

    article = writer_result["data"]


    # =========================================
    # AGENT 4 — AUTHORITY REVIEWER
    # =========================================

    print("\n========== AGENT 4: AUTHORITY REVIEWER ==========")

    review_result = authority_reviewer_agent.run(
        article=article,
        research=research
    )

    if not review_result["success"]:
        return {
            "success": False,
            "stage": "authority_reviewer",
            "error": review_result["error"]
        }

    review = review_result["data"]


    # =========================================
    # AGENT 5 — HUMANIZATION / REVISION
    # =========================================

    print("\n========== AGENT 5: HUMANIZATION ==========")

    humanization_result = humanization_agent.run(
        article=article,
        review=review
    )

    if not humanization_result["success"]:
        return {
            "success": False,
            "stage": "humanization",
            "error": humanization_result["error"]
        }

    humanized_article = humanization_result["data"]


    # =========================================
    # AGENT 6 — FINAL EDITOR
    # =========================================

    print("\n========== AGENT 6: FINAL EDITOR ==========")

    final_editor_result = final_editor_agent.run(
        article=humanized_article,
        research=research,
        review=review
    )

    if not final_editor_result["success"]:
        return {
            "success": False,
            "stage": "final_editor",
            "error": final_editor_result["error"]
        }

    final_article = final_editor_result["data"]


    # =========================================
    # FINAL RESULT
    # =========================================

    print("\n========== PIPELINE COMPLETED ==========")

    return {
        "success": True,

        # Agent 0
        "opportunity": opportunity,

        # Agent 1
        "research": research,

        # Agent 2
        "insights": insights,

        # Agent 3
        "article": article,

        # Agent 4
        "authority_review": review,

        # Agent 5
        "humanized_article": humanized_article,

        # Agent 6
        "final_article": final_article
    }