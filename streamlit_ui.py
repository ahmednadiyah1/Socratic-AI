import streamlit as st
import requests

# set page config
st.set_page_config(page_title = "My App", layout = "wide")

st.title("Socratic AI App")
st.markdown("Select a service, enter your prompt, and see the NLP-processed output.")

# sidebar for configuration
with st.sidebar:
    st.header("Settings")
    service = st.selectbox("Choose service", ["gemini", "openai"])

    model = st.text_input("Enter Model Name")
    max_tokens = st.text_input("Max Tokens")
    st.info(f"Currently targeting {model} via {service}")

prompt = st.text_area("Enter your prompt")

# create a button to trigger the api call
if st.button("Generate response"):
    if not prompt.strip() or not model.strip() or not service.strip():
        st.error("Please fill in all fields before generating a response.")

    else:
        try:
            payload = {
                "service": service,
                "model": model,
                "prompt": prompt
            }

            if max_tokens:
                 payload["max_tokens"] = int(max_tokens)

            backend_url = "http://localhost:8000/generate_with_socratic/"  # Update with your backend URL
            response = requests.post(backend_url, json = payload)

            # check if the request was successful
            if response.status_code == 200:
                data = response.json()

                st.divider()

                # display the response clearly
                st.markdown("##### Response is ")
                st.write(data["response"])

                st.markdown("##### NLP preprocessing details")
                st.write("Tokens: ", data["input_word_tokens"])
                st.write("Lemmatized words: ", data["input_lemmatized_words"])

            else:
                st.error(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
                st.error(f"Connection failed. Is your FastAPI server running? Error: {e}")