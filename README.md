# AbleBot QnA Chatbot

## RAG w/ LangChain Overview
- Retrieval Augmented Generation (RAG)
- A typical RAG application has two main components, indexing and retreival augmented generation
    - Indexing: A pipeline for ingesting data from a source (i.e., `able.co`) and indexing it. Usually done offline.
    - RAG: Takes a user query at run time and retreieves the relevant data from the index, then passes it to the model.

## A Common Pipeline
Indexing Phase:
1. Load: First we need to load our data using a `Document Loader`.
2. Split: We need to break these documents into smaller chunks using a `Text Splitter`. This is useful for indexing and passing data into a model. 
    - Note: Larger chunks are harder to search over and won't fit in a model's finite context window.
3. We need somewhere to store and index the splits, so that they can be searched over later. This is done with a `VectorStore` (database) and `Embeddings` model (semantic representation).

RAG Phase:
4. Retreive: Given a user input, releveant splits are retrieved from storage using a `Retriever`.
5. Generate: A `ChatModel` (or LLM) produces an answer using a prompt that includes both the question and retreived data.