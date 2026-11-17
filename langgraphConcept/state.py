import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel
from langgraph.graph import StateGraph,START,END

load_dotenv()

llm= init_chat_model(model=os.getenv('MODEL'))

# state
class MyState(BaseModel):
    message:str=""

# node
def greet(state:MyState):
    "I am greet node"
    print(state.message)
    return state

graph= StateGraph(MyState)
graph.add_node("greet",greet)
graph.add_edge(START,"greet")
graph.add_edge("greet",END)

final_graph=graph.compile()

res=final_graph.invoke({"message":"Hello"})


