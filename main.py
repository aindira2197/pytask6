import asyncio
import aiohttp

class API:
    def __init__(self, url):
        self.url = url

    async def get_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.json()

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        processed_data = []
        for item in self.data:
            processed_data.append(item['name'])
        return processed_data

async def main():
    api = API('https://jsonplaceholder.typicode.com/posts')
    data = await api.get_data()
    processor = DataProcessor(data)
    processed_data = processor.process_data()
    for item in processed_data:
        print(item)

async def get_user_data(user_id):
    api = API(f'https://jsonplaceholder.typicode.com/users/{user_id}')
    data = await api.get_data()
    return data

async def get_post_data(post_id):
    api = API(f'https://jsonplaceholder.typicode.com/posts/{post_id}')
    data = await api.get_data()
    return data

async def get_comment_data(comment_id):
    api = API(f'https://jsonplaceholder.typicode.com/comments/{comment_id}')
    data = await api.get_data()
    return data

async def fetch_data():
    user_data = await get_user_data(1)
    post_data = await get_post_data(1)
    comment_data = await get_comment_data(1)
    return user_data, post_data, comment_data

async def print_data():
    user_data, post_data, comment_data = await fetch_data()
    print(user_data)
    print(post_data)
    print(comment_data)

asyncio.run(main())
asyncio.run(print_data())
asyncio.run(fetch_data())