import streamlit as st
import time
from chatbot import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot()

st.title("AbleBot")
st.markdown("Answering questions about the software company, [Able](https://able.co)!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

# Function to handle query submission
def handle_query():
    st.session_state.pending_query = st.session_state.user_input  # Store input for processing
    st.session_state.user_input = ""  # Clear input field immediately after submission

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box for user to type their query
user_input = st.text_input(
    "Ask a question:",
    key="user_input",
    on_change=handle_query
)

# Display the bot's response incrementally
if st.session_state.pending_query:
    with st.spinner("Processing..."):
        response = chatbot.get_response(st.session_state.pending_query)
        assistant_message = response["result"]
        
        # Display the user message
        st.session_state.messages.append({"role": "user", "content": st.session_state.pending_query})

        # Stream bot response incrementally
        st.session_state.messages.append({"role": "assistant", "content": ""})
        assistant_message_placeholder = st.chat_message("assistant").empty()  # Placeholder for streaming response
        
        # Stream the response character by character (you can adjust speed)
        for i in range(len(assistant_message)):
            assistant_message_placeholder.write(assistant_message[:i + 1])
            time.sleep(0.005)  # Adjust this for faster/slower streaming
        
        # Store the final message
        st.session_state.messages[-1]["content"] = assistant_message
        
    # Clear pending query before rerunning
    st.session_state.pending_query = ""
    st.rerun()
