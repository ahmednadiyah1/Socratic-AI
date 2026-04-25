import streamlit as st
import requests
import uuid
import time

# set page config
st.set_page_config(page_title = "Socratic AI", layout = "wide")

# initialise session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# initialise session state for messages
if "messages" not in st.session_state:
     st.session_state.messages = []


if "is_loading" not in st.session_state:
    st.session_state.is_loading = False



# page header

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
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Only write messages to the output once
        st.chat_message("user").write(prompt)

        with st.spinner("Generating response..."):

            try:


                payload = {
                    "session_id": st.session_state.session_id,
                    "concept": concept,
                    "learning_style": learning_style,
                    "prompt": prompt
                }


                backend_url = "https://socratic-ai-1.onrender.com/generate_with_socratic/"  # Update with backend URL

                
                response = requests.post(
                    backend_url,
                    json = payload)


                if response and response.status_code == 200:
                    data = response.json()
                    assistant_msg = data["response"]
                    preprocessed_prompt = data["preprocessed_prompt"]


                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_msg
                    })

                    st.chat_message("preprocessed_prompt").write(preprocessed_prompt)
                    
                    st.chat_message("assistant").write(assistant_msg)

                else:
                    status = response.status_code if response else "No response"
                    text = response.text if response else ""
                    st.error(f"API Error: {status} - {text}")

            except Exception as e:
                print(e)
                st.error(f"Connection failed.")



