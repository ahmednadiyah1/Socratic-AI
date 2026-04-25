import streamlit as st
import requests
import uuid
import time
import base64


# convert image to base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
# setting a colour sceheme and applying it to all message boxes, chat box and sidebar

# setting colour scheme for side bar
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #FFEFE8;  /* light peach */
}
</style>
""", unsafe_allow_html=True)

# setting colour scheme for message boxes and chat box
st.markdown("""
<style>

/* MAIN chat container (removes grey background) */
[data-testid="stChatFloatingInputContainer"],
[data-testid="stChatMessage"],
[data-testid="stChatMessageList"] {
    background: transparent;
}


/* Message wrapper */
[data-testid="stChatMessage"] {
    background: transparent;
    padding: 0;
    border: none;
}

/* Message bubble */
[data-testid="stChatMessageContent"] {
    background-color: #FFEFE8;
    border-radius: 12px;
    padding: 10px;
}

/* User vs assistant differentiation */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])
[data-testid="stChatMessageContent"] {
    background-color: #FFEFE8;
}
            


</style>
""", unsafe_allow_html=True)

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

logo_base64 = get_base64_image("logo.png")
st.markdown(f"""
<style>
.header {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}}

.header-inner {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 600px;  /* controls total width */
}}

.header-title {{
    flex: 1;
    text-align: center;
    font-size: 64px;
    font-weight: 700;
    margin: 0;
    white-space: nowrap;
}}

.header img {{
    height: 50px;
}}
</style>

<div class="header">
    <div class="header-inner">
        <img src="data:image/png;base64,{logo_base64}">
        <div class="header-title">Socratic AI Tutor</div>
        <div style="width:100px;"></div> <!-- spacer equal to logo -->
    </div>
</div>
""", unsafe_allow_html=True)
# st.image("logo.png", width = 100)
# st.title("Socratic AI")




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
                # backend_url = "http://127.0.0.1:8000/generate_with_socratic/"
                
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



