from . import dataloader
from database import mongo_database
from embeddings import EmbeddingsService

embeddings_service = EmbeddingsService(database=mongo_database)


def get_unique_document_id(website_url: str) -> str:
    return f'website_{website_url.strip().lower()}'


async def run(website: str):
    # ..........
    # Pseudo code
    # 1. Check if Data for website has already been saved
    # 2. Download data from website
    # 3. Split into chunks
    # 4. Get chunk embeddings
    # 5. Save embeddings
    # 6. Register content as saved
    # ..........

    doc_id = get_unique_document_id(website)

    print(f"website: {website}, document_id: {doc_id}")
    print("loading documents from datasource")
    chunks = dataloader.load_document_in_chunks(website)
    print(f'{len(chunks)} chunks of data')

    print("creating and saving embeddings")
    # Can we parallelize this?
    for doc in chunks:
        embeddings_service.insert_embedding(document_id=doc_id,
                                            content=doc.page_content)
    print("done!")
