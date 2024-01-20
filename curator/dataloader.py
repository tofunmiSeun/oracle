from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)


def load_document_in_chunks(url: str) -> List[Document]:
    loader = WebBaseLoader(url)
    loaded_documents = loader.load()
    return text_splitter.split_documents(loaded_documents)


if __name__ == "__main__":
    url = 'https://www.cntraveller.com/gallery/best-things-to-do-in-paris'
    print('url={}'.format(url))
    chunks = load_document_in_chunks(url=url)
    for chunk in chunks:
        print(chunk.page_content, "\n\n")
