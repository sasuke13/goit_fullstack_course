import asyncio
import aiohttp

async def fetch_url(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession(
        headers={"Content-Type": "application/json", "Authorization": "Bearer 1234567890"},
        timeout=aiohttp.ClientTimeout(total=10, connect=5, sock_read=5, sock_connect=5),
    ) as session:
        async with session.post("https://python.org", data={"key": "value"}) as response:


asyncio.run(main())
