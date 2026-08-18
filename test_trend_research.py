from backend.app.agents.content_gap_agent import content_gap_agent
from backend.app.agents.trend_research_agent import trend_research_agent


# -----------------------------------------
# Agent 0
# -----------------------------------------

gap_result = content_gap_agent.run(
    topics="AI Impact on Careers, Future of Work, Career Growth",
    audience="MBA Students"
)

if not gap_result["success"]:

    print("Content Gap Agent failed:")
    print(gap_result["error"])

    exit()


opportunity = gap_result["data"]["selected_opportunity"]


print("\n================ SELECTED OPPORTUNITY ================\n")
print(opportunity)


# -----------------------------------------
# Agent 1
# -----------------------------------------

trend_result = trend_research_agent.run(
    opportunity
)


print("\n================ TREND RESEARCH RESULT ================\n")
print(trend_result)


if trend_result["success"]:

    print("\n================ RESEARCH SUMMARY ================\n")

    print(
        trend_result["data"]["research_summary"]
    )

    print("\n================ TRENDS ================\n")

    for trend in trend_result["data"]["trends"]:

        print("\n----------------------------------------")

        print("Topic:")
        print(trend["topic"])

        print("\nWhy It Matters:")
        print(trend["why_it_matters"])

        print("\nWhy Trending:")
        print(trend["why_it_is_trending"])

        print("\nContrarian Insight:")
        print(trend["contrarian_insight"])

        print("\nPractical Takeaway:")
        print(trend["practical_takeaway"])

        print("\nSources:")

        for source in trend["supporting_sources"]:

            print(
                f"- {source['source_name']}: "
                f"{source['source_url']}"
            )
            