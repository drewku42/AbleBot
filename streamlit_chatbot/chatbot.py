from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# TODO Define a system prompt !!!

# TODO Citations ? ? ?

class RAGChatbot:
    def __init__(self, doc_path="streamlit_chatbot/company_info.txt", model_name="gpt-3.5-turbo"):
        self.doc_path = doc_path
        self.model_name = model_name
        self.qa_chain = self._initialize_pipeline()

    def _initialize_pipeline(self):
        # Load and process documents
        loader = TextLoader(self.doc_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        docs = text_splitter.split_documents(documents)

        # Convert text into embeddings
        embeddings = OpenAIEmbeddings()
        vector_db = FAISS.from_documents(docs, embeddings)

        # Define LLM and retriever
        llm = ChatOpenAI(model_name=self.model_name)
        retriever = vector_db.as_retriever()

        # Create RetrievalQA pipeline
        return RetrievalQA.from_chain_type(llm, retriever=retriever)

    def get_response(self, query):
        return self.qa_chain.invoke(query)
