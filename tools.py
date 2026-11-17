from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition,ToolNode
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage

load_dotenv()

llm= init_chat_model(model=os.getenv('MODEL'))

conn=sqlite3.connect("db.AI",check_same_thread=False)
sql_memory=SqliteSaver(conn)
sql_memory.setup()



class AgentState(BaseModel):
    messages:Annotated[list,add_messages]



@tool
def weather_tool(city:str)->str:
    """
    get the real time weather details for any city.
    Args:
        city- city name for weather details.
    """
    data={
        "bhopal":"32",
        "delhi":"38",
        "mumbai":"36"
        }

    return data.get(city.lower().strip(),"City not found")

@tool
def calculate(expression:str):
    """
        Execute the math equations: Ex. '4*4-4'
    """
    return eval(expression)

tools= [weather_tool,calculate]

llm_with_tools=llm.bind_tools(tools)


def chat_bot(state:AgentState):
    res=llm_with_tools.invoke(state.messages)
    state.messages =[res]
    return state

tool_node= ToolNode(tools)

graph = StateGraph(AgentState)
graph.add_node("chat_bot",chat_bot)
graph.add_node("tools",tool_node)

graph.add_edge(START,"chat_bot")
graph.add_conditional_edges(
    "chat_bot",
    tools_condition
)
graph.add_edge("tools","chat_bot")
graph.add_edge("chat_bot",END)

final_graph=graph.compile(checkpointer=sql_memory)
res=final_graph.invoke({
    "messages":[HumanMessage(content="what is 3 +7")]
},
{"configurable":{"thread_id":"asd1"}}

)

ans= res['messages'][-1].content

print(ans)