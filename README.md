<img width="1907" height="903" alt="image" src="https://github.com/user-attachments/assets/e03efdfb-febb-4302-86bc-cff419c5635c" />

## Project Description

Socratic AI is an AI-powered educational application that takes a personalised approach to learning. Inspired by the Socratic method, it adapts to a user’s learning style and generates structured lesson plans for any topic of interest.

Rather than providing direct answers, the system guides users through each stage of learning using targeted questions and hints, encouraging deeper understanding through dialogue.

The application features a clean, intuitive interface with a sidebar that allows users to select their preferred learning style and topic, creating a tailored and interactive learning experience.

The following instructions will help in setting up the application on a local machine. 

## Architecture Overview

#### Frontend
The Streamlit frontend provides a clean, interactive chat-based interface for users. It incorporates custom CSS styling to enhance the user experience. Users can input a topic and select their preferred learning style, and responses are rendered in real time.

### Backend 
The FastAPI backend receives requests from the frontend with user prompts and learning preferences. It acts as an orchestration layer that preprocesses the user text and invokes the tutor pipeline to generate lesson plans and responses.

### LLM Layer
The LLM layer encapsulates the core intelligence of the system through a structured tutor pipeline.

To reduce hallucinations and improve factual grounding, the system first retrieves relevant information using the Tavily API. The retrieved content is then processed to construct a knowledge graph, identifying key concepts and relationships within the topic.

This structured representation is used, along with the user’s preferred learning style, to generate a coherent lesson plan. 

**Knowledge Graph and Lesson Planning**: Powered by Llama-3-8B
**Interactive Tutoring (Dialogue Generation)**: Powered by Mistral AI models via API

```
   User 
    ↓        
Streamlit UI 
    ↓      
FastAPI Backend 
    ↓             
Tavily (Search) 
    ↓
Knowledge Graph
    ↓     
LLM (Mistral)
    ↓     
Guided Response
```

      
## Setting up the Project

### Clone Repository

Begin with cloning the github repository on the local machine using the following command 

``` git clone https://github.com/ahmednadiyah1/Socratic-AI/ ```


### Setting up Environment Variables
Create a .env file in the root directory of the project. Open the .env file and add your following API keys:
```
TAVILY_API_KEY=your_tavily_api_key
HUGGINGFACE_API=your_huggingface_api_key
MISTRAL_API=your_mistral_api_key
```


### Install Dependencies

Next, install all dependencies related to the project 

``` pip install -r requirements.txt ```

### Setup Frontend and Backend Servers on the Local Machine

We will setup the frontend and the backend in two different terminals, running simultaneously.


To begin with the backend, start the service and create an endpoint with fastapi with the following command

```fastapi dev main.py```

You can also uvicorn to start the service instead, 

``` uvicorn main:app --reload ```

Now we move onto setting up the frontend by the time the backend service starts up and gets running. Open a new terminal in the root directory and run the following command 

``` streamlit run streamlit_ui.py ```

Once the model has been set-up and the frontend and backend services are up and running, open access the frontend on URL: http://localhost:8501 and test it out!

The Socratic-AI app is also deployed on render.com and can be accessed through the following link- https://socratic-ai-2.onrender.com
