import streamlit as st
from chatbot import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot()

st.title("AbleBot")
st.subheader("_____")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box remains at the bottom
query = st.text_input("Ask a question:", key="user_input", value="", on_change=lambda: st.session_state.update(pending_query=st.session_state.user_input))

# Process new query
if st.session_state.pending_query:
    response = chatbot.get_response(st.session_state.pending_query)
    
    # Store messages
    st.session_state.messages.append({"role": "user", "content": st.session_state.pending_query})
    st.session_state.messages.append({"role": "assistant", "content": response["result"]})

    # Clear query before rerunning
    st.session_state.pending_query = ""

    # Refresh to display updated messages
    st.rerun()
