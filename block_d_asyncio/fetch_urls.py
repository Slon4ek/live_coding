import asyncio
import aiohttp
from block_b_decorators.universal_timed import timed


async def fetch_url(
    url: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    retries: int,
    backoff: float,
) -> str:
    async with semaphore:
        last_exception = None
        for i in range(retries + 1):
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
            except aiohttp.ClientResponseError as e:
                if 400 <= e.status < 500:
                    raise
                last_exception = e
            except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
                last_exception = e

            if i < retries:
                await asyncio.sleep(backoff * (2 ** i))

        raise last_exception from None


async def fetch_urls(
    urls: list[str],
    limit: int,
    timeout: float,
    retries: int,
    backoff: float,
) -> tuple[dict[str, str], dict[str, BaseException]]:
    ok: dict[str, str] = {}
    failed: dict[str, BaseException] = {}

    unique_urls: list[str] = list(dict.fromkeys(urls))

    sem = asyncio.Semaphore(limit)
    client_timeout = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        tasks = [
            asyncio.create_task(fetch_url(url, session, sem, retries, backoff))
            for url in unique_urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for url, res in zip(unique_urls, results):
        if isinstance(res, BaseException):
            failed[url] = res
        else:
            ok[url] = res

    return ok, failed

@timed(threshold=5)
async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",        # 4xx — без ретраев
        "https://httpbin.org/status/500",        # 5xx — с ретраями
        "https://httpbin.org/status/503",        # 5xx — с ретраями
        "https://httpbin.org/delay/2",           # нормальный медленный
        "https://httpbin.org/delay/35",          # таймаут (если timeout=30)
        "https://не-существует-вообще.рф",       # DNS-ошибка
        "https://httpbin.org/get",               # дубликат
    ]

    ok, failed = await fetch_urls(
        urls,
        limit=5,
        timeout=5.0,
        retries=3,
        backoff=1.0,
    )

    total_processed = len(ok) + len(failed)
    print(f"Обработано: {total_processed} URL (уникальных из {len(urls)})")
    print(f"OK: {len(ok)}")
    for url, body in ok.items():
        print(f"  ✓ {url}  ({len(body)} байт)")

    print(f"\nFAILED: {len(failed)}")
    for url, err in failed.items():
        print(f"  ✗ {url}  → {type(err).__name__}: {err}")


if __name__ == "__main__":
    asyncio.run(main())
