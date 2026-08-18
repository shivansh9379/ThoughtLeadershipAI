from backend.app.agents.trend_research_agent import trend_research_agent


opportunity = {
    "topic": "Career Ladder & Leadership Development",
    "content_gap": "The Loss of the Junior Apprenticeship Model and How MBAs Can Build Business Intuition Without Entry-Level Technical Repetitions",
    "underserved_audience": "MBA Students seeking post-graduation roles in Investment Banking, Management Consulting, and Corporate Strategy.",
    "unique_angle": "Shift from managing junior humans doing execution to managing algorithmic outputs using critical intuition."
}


print("\n================ AGENT 1 TEST ================\n")

result = trend_research_agent.run(opportunity)

print("\n================ RESULT ================\n")
print(result)