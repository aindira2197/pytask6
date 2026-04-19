import aiohttp
import asyncio

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main():
    urls = [
        'https://jsonplaceholder.typicode.com/todos/1',
        'https://jsonplaceholder.typicode.com/todos/2',
        'https://jsonplaceholder.typicode.com/todos/3',
        'https://jsonplaceholder.typicode.com/todos/4',
        'https://jsonplaceholder.typicode.com/todos/5',
    ]
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, urls)
        for html in htmls:
            print(html)

async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_json(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch_json(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main_json():
    urls = [
        'https://jsonplaceholder.typicode.com/todos/1',
        'https://jsonplaceholder.typicode.com/todos/2',
        'https://jsonplaceholder.typicode.com/todos/3',
        'https://jsonplaceholder.typicode.com/todos/4',
        'https://jsonplaceholder.typicode.com/todos/5',
    ]
    async with aiohttp.ClientSession() as session:
        jsons = await fetch_all_json(session, urls)
        for json in jsons:
            print(json)

async def main_post():
    url = 'https://jsonplaceholder.typicode.com/todos'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'title': 'new todo', 'completed': False}) as response:
            print(await response.text())

asyncio.run(main())
asyncio.run(main_json())
asyncio.run(main_post())