from backend.app.agents.content_gap_agent import content_gap_agent


result = content_gap_agent.run(
    topics="AI Impact on Careers, Future of Work, Career Growth",
    audience="MBA Students"
)

print("\n================ CONTENT GAP AGENT ================\n")
print(result)

if result["success"]:

    print("\n================ SELECTED OPPORTUNITY ================\n")

    print(
        result["data"]["selected_opportunity"]
    )