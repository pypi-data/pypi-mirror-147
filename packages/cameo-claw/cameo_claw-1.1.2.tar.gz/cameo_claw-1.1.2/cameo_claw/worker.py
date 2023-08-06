import httpx
import asyncio


async def loop():
    for i in range(2):
        async with httpx.AsyncClient() as client:
            r = await client.get('http://localhost:8000/api/get_task/')
            print(r.json())
        print('debug worker.py go to sleep')
        await asyncio.sleep(1)
    return 'loop return value'


async def main():
    result = await asyncio.gather(loop())
    print(f'result:{result}')


asyncio.run(main())
