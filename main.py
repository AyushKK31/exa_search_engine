from exa_py import Exa
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("EXA_API_KEY")
exa = Exa(api_key)

print("🔍 Custom AI Search Engine")

query = input("Enter search query: ")
domain = input("Enter domain filter (example: github.com / leave blank for all): ")

if domain:
    response = exa.search_and_contents(
        query,
        num_results=5,
        include_domains=[domain],
        text=True
    )
else:
    response = exa.search_and_contents(
        query,
        num_results=5,
        text=True
    )

print("\nTop Results:\n")

for i, result in enumerate(response.results, 1):
    print(f"{i}. {result.title}")
    print(result.url)

    if result.text:
        print("Summary:", result.text[:300])

    print("-" * 60)