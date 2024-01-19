import asyncio


async def download(website: str):
    print("website: {}".format(website))
    # Download data from website
    # Split into chunks
    # Get chunk embeddings
    # Save embeddings
    # Register content as saved
    await asyncio.sleep(2)
    print("done!")
