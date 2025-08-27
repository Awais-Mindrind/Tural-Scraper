import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.schemas import ProfileFilters


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

parser = PydanticOutputParser(pydantic_object=ProfileFilters)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that converts a natural language TikTok profile search into structured filters."),
    ("system", "Output the result strictly in JSON matching this schema: {schema}"),
    ("human", "{query}")
])


def parse_query_to_filters(query: str) -> ProfileFilters:
    prompt = prompt_template.format_messages(
        query=query,
        schema=parser.get_format_instructions()
    )
    response = llm.invoke(prompt)
    return parser.parse(response.content)

