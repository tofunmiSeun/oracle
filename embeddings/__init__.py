
from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from sentence_transformers import SentenceTransformer
import time
from .models import DocumentEmbeddings

model_init_start = time.perf_counter()

# Are there alternative embedding models to use?
model_name = 'paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

model_init_stop = time.perf_counter()
print(f'''Time taken to initialize {model_name}=
      {model_init_stop - model_init_start} seconds''')


def get_embeddings(text: str) -> List[float]:
    embeddings = model.encode(text)
    converted_to_floats = [tensor.item() for tensor in embeddings]
    return converted_to_floats


class EmbeddingsService:
    def __init__(self, database: Database) -> None:
        self.collection: Collection[DocumentEmbeddings] = database[
            'document_embeddings']

    def insert_embedding(self, document_id: str, content: str):
        emb = get_embeddings(content)
        document_embeddings = DocumentEmbeddings(document_id=document_id,
                                                 content=content,
                                                 embeddings=emb)
        self.collection.insert_one(document_embeddings)


if __name__ == "__main__":
    text = 'This framework generates embeddings for each input sentence'
    embeddings = get_embeddings(text)
    print(f'''text={text},
          embeddings={embeddings[0:20]}...,
           embeddings length={len(embeddings)}''')
