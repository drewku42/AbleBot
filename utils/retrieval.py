# init.py
# This script is used to instantiate vector database.
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings

def load_retriever(query):
    new_db = FAISS.load_local("faiss_index", embeddings=OpenAIEmbeddings())
    docs = new_db.similarity_search(query)
    return docs