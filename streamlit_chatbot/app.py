import streamlit as st
from chatbot import RAGChatbot

# TODO fix chat messages, dont want to see entire session state dict !!!
# https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state

# Initialize chatbot
chatbot = RAGChatbot()

st.title("AbleBot")
st.subheader("_____")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

print(st.session_state)

# Display previous messa🙋‍♀️ges
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

query = st.text_input("Ask a question:")
if query:
    response = chatbot.get_response(query)
    print("Debugging response: ", response)

    # Append user & assistant messages to session state
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": response["result"]})

    # Display messages in chat
    st.chat_message("user").write(query)
    st.chat_message("assistant").write(response["result"])
