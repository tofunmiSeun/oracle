import asyncio
from . import dataloader


async def run(website: str):
    print("website: {}".format(website))
    _ = dataloader.load_document_in_chunks(website)
    # ..........
    # Pseudo code
    # 1. Check if Data for website has already been saved
    # 2. Download data from website
    # 3. Split into chunks
    # 4. Get chunk embeddings
    # 5. Save embeddings
    # 6. Register content as saved
    # ..........
    # Questions
    # 1. Can/Should I be recursive about crawling the URL?
    # 2. Is a different kind of text splitter better?
    # 3. are there alternative embeddings to use?
    await asyncio.sleep(2)
    print("done!")
