import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START,END
from pydantic import BaseModel
from langgraph.types import interrupt,Command
from langgraph.checkpoint.memory import InMemorySaver
from typing import Literal

load_dotenv()

llm= init_chat_model(model=(os.getenv('MODEL')))

class PurchaseState(BaseModel):
    item:str=""
    price:int=0
    confirmed:bool=False
    status:str=""

def show_orders(state:PurchaseState) ->PurchaseState:
    print(f"Order Summary:Product:{state.item} & Price:{state.price}")
    return state

def user_confirmation(state:PurchaseState)-> PurchaseState:
    response= interrupt(
        {
            "question":f"Confirm Your Purchase for {state.item} and Price is {state.price}. Please reply in yes or no onli"
        }
    )
    state.confirmed=response.lower()=="yes"
    return state

def Order_cancel(state:PurchaseState)->PurchaseState:
    print("Order cancel, Thanks!")
    return state

def Order_confirm(state:PurchaseState) ->PurchaseState:
    print("order confirm! Congratulations!")
    return state

#  this is not a node
def router(state:PurchaseState) -> Literal["Order_cancel","Order_confirm"]:
    if state.confirmed:
        return "Order_confirm"
    return "Order_cancel"   


graph= StateGraph(PurchaseState)

graph.add_node("show_orders",show_orders)
graph.add_node("user_confirmation",user_confirmation)
graph.add_node("Order_cancel",Order_cancel)
graph.add_node("Order_confirm",Order_confirm)

graph.add_edge(START,"show_orders")
graph.add_edge("show_orders","user_confirmation")
graph.add_conditional_edges("user_confirmation",router)
graph.add_edge("Order_cancel",END)
graph.add_edge("Order_confirm",END)

final_graph=graph.compile(checkpointer=InMemorySaver())

# res=final_graph.invoke(
#     {
#         "item":"Samsung S23", "price":12000
#     },
#     {
#         "configurable":{"thread_id":"asd10"}
#     }
# )

### this will work in google collabe ot jupiter note book


res=final_graph.invoke(
    Command(resume="no"),
    {
        "configurable":{"thread_id":"asd10"}
    }
)

print(res)