from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from tavily import TavilyClient
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

load_dotenv()



tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
gemini_client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

class socratic_ai_tutor:
    def __init__(self, concept, learning_style, model1 = "gemma3:1b", model2 = "qwen3.5"):
        self.llm = ChatOllama(model=model1, 
                              validate_model_on_init=True, 
                              base_url = "https://splendor-ranked-wind.ngrok-free.dev",
                            client_kwargs={"headers": {"ngrok-skip-browser-warning": "true"}})


        self.messages = []

        self.concept = concept
        self.learning_style = learning_style



    # web search tool
    def web_search(self, query,
                     num_results = 10,
                     include_raw_content = False):
        
        results = tavily_client.search(
            query= query,
            max_results = num_results,
            include_raw_content = include_raw_content
        )

        text = "\n".join([r["content"] for r in results["results"]])

        return text        

    # create a knowledge graph
    def create_knowledge_graph(self, text):

        documents = [Document(page_content=text)]
        # llm = ChatOllama(model=self.agentic_model, validate_model_on_init=True)
        llm_transformer = LLMGraphTransformer(llm = self.llm)
        graph_documents = llm_transformer.convert_to_graph_documents(documents)

        # llm_transformer_filtered = LLMGraphTransformer(
        #     llm = model,
        # #     allowed_nodes = ["definition", "key idea", "prerequisite concepts", "explanation", "formula", "algorithm", "technique", "process/workflow", "properties", "theorems", "examples", "use cases", "scenarios", "applications", "related concepts", "interdisciplinary connections", "visualisations/diagrams", "research findings", ""]
        # #     allowed_relationships = ["is defined as", "is a key idea in", "is a prerequisite concept for", "explains", "is represented by formula", "is implemented by algorithm", "is applied using technique", "follows process/workflow", "has properties", "is supported by theorems", "has examples", "is used in use cases", "occurs in scenarios", "has applications", "is related to concepts", "has interdisciplinary connections", "can be visualised by visualisations/diagrams", "is supported by research findings"]
        # )
        # graph_documents_filtered = llm_transformer_filtered.convert_to_graph_documents(documents)

        graph_data = []

        for node in graph_documents[0].nodes:
            graph_data.append({
                "type": "node",
                "id": node.id
            })

        for edge in graph_documents[0].relationships:
            graph_data.append({
            "type": "edge",
            "source": edge.source.id,
            "target": edge.target.id,
            "relation": edge.type
            })

        return json.dumps(str(graph_data), indent = 2)
    


    def create_lesson_plan(self):
        conceptual_info = self.web_search(query = self.concept)
        knowledge_graph = self.create_knowledge_graph(conceptual_info)

        system_instruction = '''You are an expert socratic AI tutor that follows the views of Socrates on education. You believe that learning is a process of 
            seeking knowledge through self-examination and dialogue rather than passive memorization. You will use the socratic method and combine it with the
            student's preferred learning style to create a personalised lesson plan.  The different types of learning styles are:
            - Active Recall: Ask questions instead of explaining concepts to the student, encourage them to recall information from memory, and provide hints to guide them towards the answer.
            - Scaffolding: Break down complex concepts into smaller, more manageable parts, and provide support and guidance to help the student understand each part before moving on to the next.
            - Analogy-based learning: Use analogies and metaphors to help the student understand complex concepts by relating them to something they already know.
            - Metacognition: Encourage the student to think about their own thinking process, identify areas where they are struggling, and develop strategies to overcome those challenges.

            
            In order to create a lesson plan that is tailored to the student's preferred learning style and use the knowledge graph that contains information about the topic the student wants to learn.
            


            To Create a structured lesson plan.

            Requirements:
            - Follow prerequisite order
            - Adapt to learning style
            - Include:
                - explanation
                - example
                - analogy
                - 1 question per concept
                - 1 hint per question
            - Keep it engaging and interactive'''


        # llm = ChatOllama(model = self.agentic_model, validate_model_on_init=True)

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Create a lesson plan for the concept {self.concept} based on the following knowledge graph: {knowledge_graph} and tailored to the following learning style: {self.learning_style}. The lesson plan should be structured in a way that follows the prerequisite order of the concepts in the knowledge graph."}
        ]
        
        lesson_plan = self.llm.invoke(messages)

        return lesson_plan.content




    def interact_with_user(self, prompt):
        
        if not hasattr(self, "lesson_plan"):
            self.lesson_plan = self.create_lesson_plan()

        system_prompt = f'''You are an expert Socratic AI tutor who is helping a user to learn according to the given lesson plan. The lesson plan is {self.lesson_plan}
        Go through the lesson plan step-by-step and for each of the questions, help the user figure out the answer through guided hints instead giving them the answer straight away. 
        The message history will be provided along with the user response, use it to identify the next step in the lesson plan to help them learn'''

        self.messages.append({"role": "user", "content": prompt})

        history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in self.messages]
        )

        try:
            response = gemini_client.models.generate_content(
                model="gemini-3-flash-preview",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt),
                contents=f"{history_text}\nuser: {prompt}"
            )

        except Exception as e:
            print(f"Error initializing model: {e}")
            raise e
        
        self.messages.append({"role": "assistant", "content": response.text})

        return response.text
        
        
        


        







