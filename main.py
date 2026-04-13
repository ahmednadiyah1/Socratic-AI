from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import socratic_ai_tutor
import traceback

app = FastAPI()

session_ids = {}



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



    try:
        print("Step 1: Request received")
        print(f"Payload: {request}")
        
        tutor = socratic_ai_tutor(
            concept=request.concept,
            learning_style=request.learning_style
        )
        print("Step 2: Tutor initialized")

        response = tutor.interact_with_user(request.prompt)
        print("Step 3: Response generated")

        return {"response": response}

    except Exception as e:
        error_detail = traceback.format_exc()
        print(f"FULL TRACEBACK:\n{error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

    # try:
    #         # call the generate_text function with the provided model and prompt
    #         response = run(request.session_id,
    #                      request.prompt, 
    #                      request.concept,
    #                      request.learning_style)

    #         return {"response": response}
    
    # except Exception as e:
    #     raise HTTPException(status_code = 500, detail = str(e))

