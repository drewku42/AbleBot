from utils.ingestion import ingest_data
from utils.retrieval import load_retriever
from utils.chat import setup_chatbot, query_chatbot

def main():
    # Ingest data, create DB
    ingest_data('company_info.txt')

    # Load retriever
    retriever = load_retriever()

    # Set up chatbot
    qa_chain = setup_chatbot(retriever)

    # Interact with chatbot
    query = input("Ask a question: ")
    response = query_chatbot(qa_chain, query)
    print("Response:", response)

if __name__ == "__main__":
    main()