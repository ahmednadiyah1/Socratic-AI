from openai import OpenAI
from google import genai
from google.genai import types
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download("punkt_tab")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()


client_openai = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
client_gemini = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

app = FastAPI()


def preprocess_text(input):
     lemmatizer = WordNetLemmatizer()
     word_tokens = word_tokenize(input)
     lemmatized_words = [lemmatizer.lemmatize(word) for word in word_tokens]
     return word_tokens, lemmatized_words



def generate_text(service, model, prompt, max_tokens = 1024):
        word_tokens, lemmatized_words = preprocess_text(prompt)
        try:
            if service == "openai" :
                response = client_openai.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens
            )

                return {"input_word_tokens": word_tokens,
                        "input_lemmatized_words": lemmatized_words,
                        "response": response.output_text} 
            
            elif service == "gemini":
                response = client_gemini.models.generate_content(
                    model = model,
                    contents = prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens = max_tokens
                    ), 
                )

                return {"input_word_tokens": word_tokens,
                        "input_lemmatized_words": lemmatized_words,
                        "response": response.text}
        
        except Exception as e:
            print(f"Error generating text with {model}: {e}")
            raise e
        

class TextGenerationRequest(BaseModel):
     service: str
     model: str
     prompt: str
     max_tokens: int = 1024


@app.post("/generate_with_socratic/") # Endpoint for text generation
async def generate_with_socratic(request: TextGenerationRequest):
    try:
          # call the generate_text function with the provided model and prompt
          response = generate_text(request.service, request.model, request.prompt, request.max_tokens)
          return response
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

# print(generate_text("gemini", 'gemini-2.5-flash', 'What is the capital of France?'))