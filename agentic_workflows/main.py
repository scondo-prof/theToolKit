import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI()


async def worker(topic: str, strategy: str, system: str) -> str:
    resp = await client.responses.create(
        model="gpt-5",
        input=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": f"Topic: {topic}\nSearch strategy: {strategy}\nFind 3-5 high-quality items with citations.",
            },
        ],
        tools=[{"type": "web_search"}],
        parallel_tool_calls=True,
    )
    return resp.output_text


async def orchestrate(topic: str, search_strategies: list[str], system: str) -> str:

    worker_tasks: list[any] = []

    for strategy in search_strategies:
        print(f"Spawning worker for strategy: {strategy}")
        worker_tasks.append(worker(topic=topic, strategy=strategy, system=system))

    partials = await asyncio.gather(*worker_tasks)

    # Synthesis + de-dup + ranking pass:
    synth = await client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": "Merge JSON arrays; dedupe by URL domain; rank by evidence quality + recency; output JSON {summary, key_points[], citations[]}",
            },
            {"role": "user", "content": "\n".join(partials)},
        ],
    )

    with open("test.json", "w") as output_file:
        output_file.write(synth.output_text)
    return synth.output_text


if __name__ == "__main__":
    #!<--- Commented out other list items because ran into rate limits due to concurrency.
    search_strategies: list[str] = [
        "recent news, after:2025-10-01, intitle:report",
        "primary docs: site:.gov OR site:.edu OR site:who.int filetype:pdf",
        # "industry: site:ft.com OR site:bloomberg.com OR site:nejm.org",
        # "long-tail: exact phrases in quotes + minus common noise terms",
    ]

    system: str = """You are a focused research agent. 
Return STRICT JSON: { "findings": [{ "claim": str, "evidence": str, "url": str, "publisher": str, "published": str }]} 
Only include items with a working URL.
"""

    topic: str = "News in the greater Hartford Area in CT"

    asyncio.run(orchestrate(topic=topic, search_strategies=search_strategies, system=system))
