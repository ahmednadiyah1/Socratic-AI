Socractic AI is an application that integrates openai and gemini services to run their models in a simple user interface. The app is built in python uses FastAPI to create endpoints and streamlit to develop a front-end. The frontend and the backend are both deployed on Render.

The following instructions will help in setting up the application on a local machine. 

Begin with cloning the github repository on the local machine using the following command 

``` git clone https://github.com/ahmednadiyah1/Socratic-AI/ ```

Next, install all dependencies related to the project 

``` pip install -r requirements.txt ```

We will setup the frontend and the backend in two different terminals, running simultaneously.

To begin with the backend, start the service and create an endpoint with fastapi with the following command \\

```fastapi dev main.py```

You can also uvicorn to start the service instead, 

``` uvicorn main:app --reload ```

Now we move onto setting up the frontend by the time the backend service starts up and gets running. Open a new terminal in the root directory and run the following command 

``` streamlit run streamlit_ui.py ```

Once, both services are up and running, open access the frontend on URL: http://localhost:8501 and test it out!
