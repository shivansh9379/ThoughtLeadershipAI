from backend.app.agents.content_gap_agent import content_gap_agent
from backend.app.agents.trend_research_agent import trend_research_agent
from backend.app.agents.insight_extraction_agent import (
    insight_extraction_agent
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


print("\n================ AGENT 0 COMPLETE ================\n")

print(
    opportunity["suggested_title"]
)


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


print("\n================ AGENT 1 COMPLETE ================\n")

print(
    research["research_summary"]
)


# =========================================
# AGENT 2
# =========================================

insight_result = insight_extraction_agent.run(
    opportunity=opportunity,
    research=research
)


print("\n================ AGENT 2 RESULT ================\n")

print(insight_result)


if insight_result["success"]:

    data = insight_result["data"]

    print("\n================ CORE INSIGHT ================\n")

    print(
        data["core_insight"]
    )

    print("\n================ SECOND ORDER EFFECTS ================\n")

    for effect in data["second_order_effects"]:
        print("-", effect)

    print("\n================ CONTRARIAN PERSPECTIVE ================\n")

    print(
        data["contrarian_perspective"]
    )

    print("\n================ FRAMEWORK ================\n")

    framework = data["original_framework"]

    print(
        framework["name"]
    )

    print(
        framework["description"]
    )

    for step in framework["steps"]:

        print(
            f"{step['step']}: "
            f"{step['explanation']}"
        )

    print("\n================ CORE THESIS ================\n")

    print(
        data["core_thesis"]
    )