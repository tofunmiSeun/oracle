from . import dataloader
from database.service import DatabaseService
from embeddings import get_embeddings

db_service = DatabaseService()


async def run(website: str, doc_id: str):
    # ..........
    # Pseudo code
    # 1. Check if Data for website has already been saved
    # 2. Download data from website
    # 3. Split into chunks
    # 4. Get chunk embeddings
    # 5. Save embeddings
    # 6. Register content as saved
    # ..........

    print(f"website: {website}, document_id: {doc_id}")
    print("loading documents from datasource")
    chunks = dataloader.load_document_in_chunks(website)
    print(f'{len(chunks)} chunks of data')

    print("creating and saving embeddings")
    # Can we parallelize this?
    for doc in chunks:
        emb = get_embeddings(doc.page_content)
        db_service.insert_embedding(document_id=doc_id,
                                    content=doc.page_content,
                                    embeddings=emb)
    print("done!")
