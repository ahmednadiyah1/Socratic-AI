from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import socratic_ai_tutor
import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import string


app = FastAPI()

session_ids = {}


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'

def preprocess_prompt(prompt):
     lemmatizer = WordNetLemmatizer()

     tokens = word_tokenize(prompt.lower())
     tagged = pos_tag(tokens)

     lemmatized_words = [lemmatizer.lemmatize(w, get_wordnet_pos(tag)) for w, tag in tagged if (w not in string.punctuation)]

     return f"Preprocessed text: {lemmatized_words}"

def run(session_id, prompt, concept, learning_style):
    if session_id not in session_ids:
        session_ids[session_id] = socratic_ai_tutor(concept, learning_style)

    tutor = session_ids[session_id]
    return tutor.interact_with_user(prompt)


    

class TextGenerationRequest(BaseModel):
     session_id: str
     concept: str
     learning_style: str
     prompt: str
    


@app.post("/generate_with_socratic/") # Endpoint for text generation
async def generate_with_socratic(request: TextGenerationRequest):

    preprocessed_text = preprocess_prompt(request.prompt)

    try:
            # call the generate_text function with the provided model and prompt
            response = run(request.session_id,
                         request.prompt, 
                         request.concept,
                         request.learning_style)

            return {"response": response,
                    "preprocessed_prompt": preprocessed_text}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

