# Fan_out TO Fan_in
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel
from langgraph.graph import StateGraph,START,END
from typing import Annotated
from langgraph.types import Send,Overwrite
from langgraph.checkpoint.memory import InMemorySaver
import operator
from datetime import datetime

load_dotenv()

llm= init_chat_model(model=(os.getenv('MODEL')))

DOCUMENTS = [
    {"id": 1, "text": "LangGraph is a library for building stateful, multi-actor applications with LLMs."},
    {"id": 2, "text": "Python is a high-level programming language known for its simple syntax and readability."},
    {"id": 3, "text": "Machine learning enables systems to learn from data automatically."},
]

def custom_reducer(existing:list,new:list):
    all_msg=existing +new
    return all_msg

class SummarizerState(BaseModel):
    documents:list[dict] = []
    summaries: Annotated[list,custom_reducer]

class Document(BaseModel):
    id:int=0
    text:str=""

def route_to_summarizer(state:SummarizerState):
    sends=[]
    for doc in state.documents:
        document=Document(id=doc["id"],text=doc["text"])
        sends.append(Send("summarize",document))
    return sends

def summarize(state:Document):
    now = datetime.now()
    print("\n Summarize Node...", now.strftime("%M:%S"))
    response = llm.invoke(f"Summarize is 5 Words: {state.text}")
    return {"summaries": [ {"id": state.id, "summary": response.content.strip()} ]}

def collect_all(state:SummarizerState):
    print("All Summaries: ",state.summaries)
    return state



graph = StateGraph(SummarizerState)
graph.add_node("summarize", summarize)
graph.add_node("collect_all", collect_all)

graph.add_conditional_edges(START, route_to_summarizer, ["summarize"])
graph.add_edge("summarize", "collect_all")
graph.add_edge("collect_all", END)

final_graph = graph.compile(checkpointer=InMemorySaver())
final_graph

res = final_graph.invoke({"documents": DOCUMENTS, "summaries": Overwrite([])}, {"configurable": {"thread_id":"asd10"}})
print(res)