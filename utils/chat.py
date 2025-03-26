# chat.py
# This script is used to start the chatbot and perform retrieval augmented generation.

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Import API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=new_db.as_retriever())

result = qa_chin.run(query)
print(result)