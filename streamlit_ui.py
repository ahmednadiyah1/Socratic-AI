import streamlit as st
import requests
import uuid


# get session id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# initialise session state for messages
if "messages" not in st.session_state:
     st.session_state.messages = []


# set page config
st.set_page_config(page_title = "My App", layout = "wide")

st.title("Socratic AI App")
st.markdown("Learn with Socratic AI Tutor")

# sidebar for configuration
with st.sidebar:
    st.header("Settings")
    learning_style = st.selectbox("Choose your learning style technique", ["Active Recall", "Scaffolding", "Analogy-Based", "Metacognition"])

    concept = st.text_input("What woould you like to learn today?")

for msg in st.session_state.messages:
    
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

    else:
        st.chat_message("AI Tutor").write(msg["content"])


prompt = st.chat_input("Enter your prompt")

# create a button to trigger the api call
if prompt:
    # # if not prompt.strip() or not learning_style.strip() or not concept.strip():
    if not concept.strip():
        st.error("Please provide a topic to learn with the AI tutor")

    else:
        try:
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            payload = {
                "session_id": st.session_state.session_id,
                "concept": concept,
                "learning_style": learning_style,
                "prompt": prompt
            }


            backend_url = "https://socratic-ai-1.onrender.com/generate_with_socratic/"  # Update with backend URL
            response = requests.post(backend_url, json = payload)

            # check if the request was successful
            if response.status_code == 200:
                data = response.json()

                # add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["response"]
                })


                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        st.chat_message("user").write(msg["content"])
                    else:
                        st.chat_message("assistant").write(msg["content"])


            else:
                st.error(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
                st.error(f"Connection failed. Is your FastAPI server running? Error: {e}")
