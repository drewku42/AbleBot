# ingestion.py
# This script is used to load a document, split it into chunks, create embeddings for each chunk, and store them in a vector database.

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def ingest_data(document_path):
    # Load Data
    loader = TextLoader(document_path)
    documents = loader.load()

    # Split Data
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Create Embeddings
    embeddings = OpenAIEmbeddings()

    # Store in Vector DB
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")