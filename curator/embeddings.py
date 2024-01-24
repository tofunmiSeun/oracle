from sentence_transformers import SentenceTransformer
from typing import List
import time

model_init_start = time.perf_counter()

model_name = 'paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

model_init_stop = time.perf_counter()
print(f'''Time taken to initialize {model_name}=
      {model_init_stop - model_init_start} seconds''')


def get_embeddings(text: str) -> List[float]:
    return model.encode(text)


if __name__ == "__main__":
    text = 'This framework generates embeddings for each input sentence'
    embeddings = get_embeddings(text)
    print(f'''text={text},
          embeddings={embeddings[0:20]}...,
           embeddings length={len(embeddings)}''')
