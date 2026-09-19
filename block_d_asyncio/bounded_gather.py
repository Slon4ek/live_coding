import asyncio
import time

async def bounded_gather(*coros, limit: int) -> list:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")
    if not coros:
        return []

    semaphore = asyncio.Semaphore(limit)
    async def _wrap(coro):
        async with semaphore:
           return await coro


    tasks = [asyncio.create_task(_wrap(coro)) for coro in coros]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return list(results)

