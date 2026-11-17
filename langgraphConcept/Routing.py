from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel
from typing import Literal

llm = init_chat_model(model=os.getenv('MODEL'))

class TicketState(BaseModel):
    issue:str=""
    category:str=""
    response:str=""

def classify(state:TicketState)-> TicketState:
    issue=state.issue.lower()
    if "payment" in issue or "amount" in issue:
        state.category="billing"
    elif "refund" in issue or "cancle" in issue:
        state.category='refund'
    else:
        state.category="status"
    return state

def billing(state:TicketState)->TicketState:
    print("Billing related issue!")
    return state

def refund(state:TicketState)->TicketState:
    print("Refund related issue!")
    return state

def status(state:TicketState)->TicketState:
    print("status related issue!")
    return state

# this is not a node it is conditional logic
def router_logic(state:TicketState)->Literal["billing","status","refund"]:
    return state.category


graph=StateGraph(TicketState)

graph.add_node("classify",classify)
graph.add_node('billing',billing)
graph.add_node('status',status)
graph.add_node('refund',refund)

graph.add_edge(START,"classify")
graph.add_conditional_edges("classify",router_logic) //you can passs a dictionary which maps the value to the fun require to do the task.
graph.add_edge('billing',END)
graph.add_edge('status',END)
graph.add_edge('refund',END)

final_graph = graph.compile()

final_graph.invoke({"issue":"Waiting for amount!"})


# there is two why you can router your node direction. First is to write logic that decide where should the node moves and 2nd is to use ai to decide the node direction. In production level we mostly use ai to decide direction.
