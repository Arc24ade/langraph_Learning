import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
llm= init_chat_model(model=os.getenv("MODEL"))

HUMAN_STYLE = """
Avoid robotic phrases such as “In today’s fast-paced world,” “delve into,” “unlock the power of,” “game-changer,” “revolutionary,” and “in conclusion.”

Avoid vague statements, generic claims, unnecessary filler, and exaggerated promises. Use specific details and concrete examples wherever possible.

Use simple, conversational language with varied sentence lengths and natural transitions. Avoid repetitive sentence structures and excessive adjectives.

Focus on the reader’s real problems, practical benefits, and actionable information. Do not invent facts, statistics, testimonials, or product features.

Keep the writing clear, engaging, and authentic. Every sentence should add value, and the call to action should be relevant and natural."""

OUTLINE_PROMPT=ChatPromptTemplate.from_template(
    "write a short online for a blog post.\n\n"
    "Topic:{topic}\n"
    "Tone:{tone}\n\n"
    "Give me:\n"
    "- one opening line that makes the reader curious\n"
    "- 4 section headings\n"
    "- 5 key points the post must cover\n\n"
    "just the outline. Do not write the post."
)

DRAFT_PROMPT=ChatPromptTemplate.from_template(
    "write a blog post from this outline. \n\n"
    "{outline}\n\n"
    +HUMAN_STYLE
    +"\n\n"
    "Tone:{tone}\n\n"
    "output markdown, with the section heading as ##. \n"
)

POLISH_PROMPT = ChatPromptTemplate.from_template(
    "Rewrite and polish the following blog post to make it sound natural, "
    "clear, and engaging.\n\n"
    "Original blog post:\n"
    "{draft}\n\n"
    + HUMAN_STYLE
    + "\n\n"
    "Improve awkward sentences, remove repetition, and make transitions "
    "smoother without changing the original meaning.\n"
    "Keep the writing specific, useful, and relevant to the reader.\n"
    "Do not add unsupported facts or claims.\n\n"
    "Tone: {tone}\n\n"
    "Output clean Markdown with section headings formatted using ##.\n"
    "Return only the polished blog post, without explanations."
)

outline_chain = OUTLINE_PROMPT | llm | StrOutputParser()
draft_chain= DRAFT_PROMPT | llm | StrOutputParser()
final_chain = POLISH_PROMPT | llm | StrOutputParser()



blog_chain = (
    RunnablePassthrough.assign(
        outline=outline_chain
    )
    | RunnablePassthrough.assign(
        draft=draft_chain
    )
    | final_chain
)

result = blog_chain.invoke({
    "topic": "Benefits of wireless headphones for students",
    "tone": "Friendly and conversational",
})

print(result)