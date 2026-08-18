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


# =========================================
# AGENT 0
# =========================================

gap_result = content_gap_agent.run(
    topics="AI Impact on Careers, Future of Work, Career Growth",
    audience="MBA Students"
)

if not gap_result["success"]:
    print("Agent 0 failed:")
    print(gap_result["error"])
    exit()

opportunity = gap_result["data"]["selected_opportunity"]


# =========================================
# AGENT 1
# =========================================

research_result = trend_research_agent.run(
    opportunity
)

if not research_result["success"]:
    print("Agent 1 failed:")
    print(research_result["error"])
    exit()

research = research_result["data"]


# =========================================
# AGENT 2
# =========================================

insight_result = insight_extraction_agent.run(
    opportunity=opportunity,
    research=research
)

if not insight_result["success"]:
    print("Agent 2 failed:")
    print(insight_result["error"])
    exit()

insights = insight_result["data"]


# =========================================
# AGENT 3
# =========================================

writer_result = content_writer_agent.run(
    opportunity=opportunity,
    research=research,
    insights=insights
)

if not writer_result["success"]:
    print("Agent 3 failed:")
    print(writer_result["error"])
    exit()

article = writer_result["data"]


# =========================================
# AGENT 4
# =========================================

review_result = authority_reviewer_agent.run(
    article=article,
    research=research
)


print("\n================ AGENT 4 RESULT ================\n")

print(review_result)


if review_result["success"]:

    review = review_result["data"]

    print("\n================ AUTHORITY SCORE ================\n")

    print(
        review["overall_score"]
    )

    print("\n================ PUBLICATION READY ================\n")

    print(
        review["publication_ready"]
    )

    print("\n================ STRENGTHS ================\n")

    for item in review["strengths"]:
        print("-", item)

    print("\n================ ISSUES ================\n")

    for issue in review["issues"]:

        print(
            f"\nClaim: {issue['claim']}"
        )

        print(
    f"Problem: {issue.get('problem', issue.get('thought', 'No explanation provided.'))}"
)

        print(
            f"Severity: {issue['severity']}"
        )

        print(
            f"Action: {issue['recommended_action']}"
        )

    print("\n================ REQUIRED CHANGES ================\n")

    for change in review["required_changes"]:
        print("-", change)

    print("\n================ AUTHORITY ASSESSMENT ================\n")

    print(
        review["authority_assessment"]
    )