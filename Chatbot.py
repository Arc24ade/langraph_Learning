from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()


llm= init_chat_model(model=os.getenv("MODEL"))
history=[]

while True:
    query=input("user: ")
    if query =="exit":
        break
    history.append(query)
    res=llm.invoke([{"role":"user","content":history}])
    history.append(res.content[0]["text"])
    print("AI: ",res.content[0]["text"])