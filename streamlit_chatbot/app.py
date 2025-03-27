import streamlit as st
from chatbot import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot()

st.title("📚 Able QnA Chatbot 🤖")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

query = st.text_input("Ask a question:")
if query:
    response = chatbot.get_response(query)

    # Append user & assistant messages to session state
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display messages in chat
    #st.chat_message("user").write(query)
    st.chat_message("assistant").write(response["result"])
