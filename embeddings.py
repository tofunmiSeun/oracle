
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
import time

model_init_start = time.perf_counter()

# Are there alternative embedding models to use?
model_name = 'paraphrase-MiniLM-L6-v2'
embedding_model = HuggingFaceEmbeddings(model_name=model_name)

model_init_stop = time.perf_counter()
print(f'''Time taken to initialize {model_name}=
      {model_init_stop - model_init_start} seconds''')


def embed_documents(text: str) -> List[float]:
    return embedding_model.embed_documents([text])[0]


def embed_query(text: str) -> List[float]:
    return embedding_model.embed_query(text)
