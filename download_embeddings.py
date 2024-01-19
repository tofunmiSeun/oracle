import asyncio


async def download(website: str):
    print("website: {}".format(website))
    await asyncio.sleep(2)
    print("done!")
