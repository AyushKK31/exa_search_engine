from exa_py import Exa
from dotenv import load_dotenv
import os

load_dotenv()

exa = Exa(os.getenv("EXA_API_KEY"))

print("🔍 Custom AI Search Engine")

query = input("Enter your search query: ")

response = exa.search(query, num_results=5)

print("\nTop Results:\n")

for i, result in enumerate(response.results, 1):
    print(f"{i}. {result.title}")
    print(result.url)
    print("-" * 50)