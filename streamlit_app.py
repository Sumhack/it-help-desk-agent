from strands_agent import agent
import streamlit as st

st.set_page_config(page_title="IT Help Desk Agent", page_icon="🤖")

st.title("👩‍🌾 IT Help Desk Agent")

# Initialize session state for storing conversation
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar: option to clear conversation
if st.sidebar.button("🧹 Clear Conversation"):
    st.session_state["messages"] = []

# Display conversation
for role, msg in st.session_state["messages"]:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg)

# Input box for new message
if user_input := st.chat_input("Type your message..."):
    # Save user message
    st.session_state["messages"].append(("user", user_input))

    # Get agent response
    response = agent(user_input)
    st.session_state["messages"].append(("assistant", response))

    # Rerun so new messages appear
    st.rerun()
