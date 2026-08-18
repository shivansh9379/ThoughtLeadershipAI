from backend.app.tools.tool_router import router

queries = [
    "Today's news",
    "Latest AI news",
    "245*567",
    "Weather in Chennai",
    "Explain Java Polymorphism"
]

for q in queries:
    print("=" * 60)
    print("Query :", q)
    print(router.detect(q))