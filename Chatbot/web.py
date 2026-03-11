import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Chat Assistant",
    page_icon="💬",
    layout="wide"
)

# Title and description
st.title("🏗️ ihhn-host-lib")
st.caption("⚡ Build beautiful, consistent, and accessible Angular apps effortlessly.")
st.markdown("""
**ihhn-host-lib** is a modern **Angular component library** designed to simplify UI development 
with **Material Design–styled** components.  
It offers ready-to-use **buttons, forms, navigation elements**, and more — all built with a focus on 
**accessibility**, **performance**, and **developer experience**.
""")


# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input(
        "API URL",
        value="http://127.0.0.1:8000/ask",
        help="Enter the API endpoint URL"
    )
    st.divider()
    st.markdown("### About")
    st.info("This app sends questions to your API and displays the responses in markdown format.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(question)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Make API request
                response = requests.post(
                    api_url,
                    headers={
                        'accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    json={"question": question},
                    timeout=3000
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer provided")
                    
                    # Display the answer in markdown
                    st.markdown("```typescript\n" + answer + "\n```")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "```typescript\n" + answer + "\n```"
                    })
                else:
                    error_msg = f"❌ Error: API returned status code {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    
            except requests.exceptions.Timeout:
                error_msg = "❌ Error: Request timed out. Please try again."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
                
            except requests.exceptions.ConnectionError:
                error_msg = f"❌ Error: Could not connect to {api_url}. Please check if the API is running."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Clear chat button
if st.session_state.messages:
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

