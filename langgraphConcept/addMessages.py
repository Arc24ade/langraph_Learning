# In LangGraph, add_messages is a special reducer function that manages messages in your graph's state.

from langgraph.graph.message import add_messages
from typing import Annotated
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model
from random import randint
from pydantic import BaseModel

load_dotenv()

llm= init_chat_model(model=os.getenv('MODEL'))

def customReducer(existing:list,new:list):
    return ['Hello']

# class ChatState(BaseModel):
#     messages:Annotated[list,add_messages]=[]
class ChatState(BaseModel):
    messages:Annotated[list,customReducer]=[]

def chat_bot(state:ChatState):
    state.messages=llm.invoke(state.messages)
    return state
   

graph=StateGraph(ChatState)
graph.add_node("chat_bot",chat_bot)

graph.add_edge(START,"chat_bot")
graph.add_edge("chat_bot",END)

final_graph=graph.compile()

res=final_graph.invoke({"messages":[{"role":"user","content":"how are you"}]})
print(res)