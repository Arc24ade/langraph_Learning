
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import ALL_TOOLS
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = create_agent(
    model=os.getenv("MODEL"),
    tools=ALL_TOOLS,
    system_prompt=(
        "You are a research assistant with Google search and weather tools. "
        "Use 'google_search' to search for current information on the web. "
        "Use 'weather_tool' when the user asks about weather, including "
        "temperature, humidity, or other weather details. "
        "Use the tools when they are relevant to the user's request."
        "just use tools and give me wheather info anything else whenever i ask about the city or country"
    ),
    checkpointer=InMemorySaver()
)


config = {
    "configurable": {
        "thread_id": "test-session-1"
    }
}

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    response = llm.invoke(
        {
            "messages": [
                {"role": "user", "content": user_input}
            ]
        },
        config=config
    )
    res=response["messages"][-1].content
    ans=res[0]['text']
    print("\nAI:", ans)
