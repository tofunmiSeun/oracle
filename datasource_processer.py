from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from database.service import DatabaseService
from embeddings import get_embeddings

db_service = DatabaseService()
# Is a different kind of text splitter better?
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)


def load_document_in_chunks(url: str) -> List[Document]:
    loader = WebBaseLoader(url)

    print('Loading documents...')
    loaded_documents = loader.load()

    print('Splitting documents...')
    chunks = text_splitter.split_documents(loaded_documents)
    return chunks


async def process_website(website: str, doc_id: str):
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
    chunks = load_document_in_chunks(website)
    print(f'{len(chunks)} chunks of data')

    print("creating and saving embeddings")
    # Can we parallelize this?
    for doc in chunks:
        emb = get_embeddings(doc.page_content)
        db_service.insert_embeddings(document_id=doc_id,
                                     content=doc.page_content,
                                     embeddings=emb)
    print("done!")
