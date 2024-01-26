from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from typing import List

load_dotenv()

prompt_template = """
You are a helpful assistant.
Answer the question based on information from the context provided.
Be very succint and only list answers in bullet points.

<context>
{context}
</context>

Question: {input}
"""

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
prompt = ChatPromptTemplate.from_template(prompt_template)


def ask_llm(query: str, retrieved_documents: List[str]) -> str:
    document_chain = create_stuff_documents_chain(llm, prompt)

    retr_output = [Document(page_content=text) for text in retrieved_documents]
    retriever = RunnableLambda((lambda _: retr_output))

    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    result = retrieval_chain.invoke({"input": query})
    return result['answer']
