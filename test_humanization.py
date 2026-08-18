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

if not review_result["success"]:
    print("Agent 4 failed:")
    print(review_result["error"])
    exit()

review = review_result["data"]


# =========================================
# AGENT 5
# =========================================

humanization_result = humanization_agent.run(
    article=article,
    review=review
)


print("\n================ AGENT 5 RESULT ================\n")

print(humanization_result)


if humanization_result["success"]:

    final_article = humanization_result["data"]

    print("\n================ FINAL TITLE ================\n")
    print(final_article["title"])

    print("\n================ FINAL ARTICLE ================\n")
    print(final_article["article"])

    print("\n================ FINAL TAKEAWAYS ================\n")

    for takeaway in final_article["key_takeaways"]:
        print("-", takeaway)

    print("\n================ CTA ================\n")
    print(final_article["recommended_cta"])

    print("\n================ REVISION SUMMARY ================\n")

    for change in final_article["revision_summary"]:
        print("-", change)
        