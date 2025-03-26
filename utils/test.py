from dotenv import load_dotenv
import os

load_dotenv()

print("Now running pipeline test . . .")

# Core Component Selection
# 1. Select Chat Model (OpenAI)
from langchain.chat_models import init_chat_model

my_api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4o-mini", model_provider="openai")
#print("GPT-4o-Mini: " + model.invoke("What's your name?").content + "\n")
print("Selecting Chat Model . . .")

# 2. Select Embeddings Model (OpenAI)
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
print("Selecting embeddings model . . .")

# 3. Initialize Vector Store (ChromaDB)
from langchain_chroma import Chroma

vector_store = Chroma(
  collection_name="able_data",
  embedding_function=embeddings,
  persist_directory="./chroma_langchain_db" # where to save data locally
)
print("Instantiating vector store . . .")

# Data Ingestion & Preprocessing
# 1. Scrape content (able.co)
import requests
from bs4 import BeautifulSoup

company_url = "https://able.co"
response = requests.get(company_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract text from paragraphs, headings, etc.
content = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])

# Save to file (local storage)}"
with open("company_info.txt", "w") as file:
    file.write(content)

# 2. Load Documents into LangChain > Use `Loader`s
from langchain_community.document_loaders import TextLoader

loader = TextLoader("company_info.txt")
documents = loader.load()
print(f"Loaded {len(documents)} document(s).")

# 3. Chunk the Data > use a `TextSplitter`, i.e., `RecursiveCharacterTextSplitter`
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=400,
  chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"Generated {len(chunks)} text chunks.")

# 4. Embed and Store the data > convert text to embeddings, store in DB
vector_store.add_documents(chunks)
print("Embedded and stored documents in ChromaDB.")

# Implement Retrieval-Augmented Generation (RAG)

# 1. Create a Retrieval Pipeline (using Chroma)
retriever = vector_store.as_retriever(search_kwargs={"k": 5}) # retrieve top k results
print("Retriever is ready!")

# 2. Define a RAG Chain > combine retrieved data with the LLM for contextual responses
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
  llm=model,
  chain_type="stuff", # stuffing retrieved docs directly into the prompt
  retriever=retriever
)

print("RAG chain is set up!")

query = "What does Able.co specialize in?"
response = qa_chain.invoke({"query": query})

print("\nBot Answer: ", response["result"])

# Implement Chat History (Optional)

print("Done!")

