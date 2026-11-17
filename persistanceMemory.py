# we can use sqlliteSaver ot pgsql to store

import os 
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel
from typing import Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()
llm= init_chat_model(model=os.getenv('MODEL'))

conn=sqlite3.connect("db.AI",check_same_thread=False)
sql_memory=SqliteSaver(conn)
sql_memory.setup()

class ChatState(BaseModel):
    messages: Annotated[list,add_messages]

def chat_bot(state:BaseModel):
    state.messages=[llm.invoke(state.messages)]
    return state

graph=StateGraph(ChatState)

graph.add_node("chat_bot",chat_bot)
graph.add_edge(START,"chat_bot")
graph.add_edge("chat_bot",END)

memory=InMemorySaver()
final_graph=graph.compile(checkpointer=sql_memory)

res=final_graph.invoke({
    "messages":[HumanMessage(content='how old is he?')]
},
{"configurable":{"thread_id":"asd1"}}
)

ans=res['messages'][-1].content
print(ans[0]['text'])



# this is persistance memory helps to store context in db so it is not dependable on ram that's why we can use context even after new ru of script.