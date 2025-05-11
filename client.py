import httpx
import asyncio
import time

async def fetch_item(item_id: int):
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"http://127.0.0.1:8090/process/{item_id}")
        return response.json()

async def main():
    tasks = [fetch_item(i) for i in range(5)]
    start_time = time.perf_counter()
    results = await asyncio.gather(*tasks)
    end_time = time.perf_counter()

    for result in results:
        print(f"Result: {result}")

    print(f"Total elapsed time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
