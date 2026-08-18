from backend.app.agents.content_gap_agent import content_gap_agent
from backend.app.agents.trend_research_agent import trend_research_agent
from backend.app.agents.insight_extraction_agent import (
    insight_extraction_agent
)
from backend.app.agents.content_writer_agent import (
    content_writer_agent
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


print("\n================ AGENT 3 RESULT ================\n")

print(writer_result)


if writer_result["success"]:

    article = writer_result["data"]

    print("\n================ TITLE ================\n")
    print(article["title"])

    print("\n================ ARTICLE ================\n")
    print(article["article"])

    print("\n================ TAKEAWAYS ================\n")

    for takeaway in article["key_takeaways"]:
        print("-", takeaway)

    print("\n================ CTA ================\n")
    print(article["recommended_cta"])