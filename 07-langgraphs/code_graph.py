# flake8: noqa

from typing_extensions import TypedDict
from openai import OpenAI
from typing import Literal
# from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
# load_dotenv()
# client = OpenAI()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# pydantic is zod for py
class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: str

class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None

def classify_message(state: State):
    query = state["user_query"]
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
    Return the response in specified JSON boolean only.
    """


    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format = ClassifyMessageResponse,
        messages = [
            {"role":"system", "content":SYSTEM_PROMPT},
            {"role":"user","content":query},
        ]
    )

    response.choice[s0].message.parsed.is_coding_question
    state["is_coding_question"] = is_coding_question

    return state

def route_query(state: State):
    is_coding = state["is_coding_question"]
    if is_coding:
        return "coding_query"
    return "general_query"

def general_query(state: State):
    query = state["user_query"]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user", "content":  query}
        ]
    )
    state["llm_result"] = response.choices[0].message.content
    return state

def coding_query(state: State):
    query = state["user_query"]
    SYSTEM_PROMPT = """
        You are a Coding Expert Agent
    """
    response = client.chat.completions.create(
        model="Anthropic: Claude Sonnet 4.5",
        messages=[
            {"role":"system", "content":  SYSTEM_PROMPT},
            {"role":"user", "content":  query}
        ]
    )
    state["llm_result"] = response.choices[0].message.content
    return state

def coding_validate_query(state: State):
    query = state["user_query"]
    llm_code = state["llm_result"]
    SYSTEM_PROMPT = """
        You are expert in calculating accuracy of the code according to the question, Return the percentage of accuracy.
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format = CodeAccuracyResponse,
        messages=[
            {"role":"system", "content":  SYSTEM_PROMPT},
            {"role":"user", "content":  query}
        ]
    )

    state["accuracy_percentage"] = response.choices[0].message.parsed.accuracy_percentage
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("classify_message",classify_message)
graph_builder.add_node("route_message",route_message)
graph_builder.add_node("general_query",general_query)
graph_builder.add_node("coding_message",coding_message)

graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", "route_query")
graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", "coding_validate_query")
graph_builder.add_edge("coding_validate_query", END)

graph = graph_builder.compile()

def main():
    user = input("> ")

    _state: State = {
        "user_query": user,
        "accuracy_percentage": None,
        "is_coding_question": False,
        "llm_result": None
    }

    for event in graph.stream(_state):
        print("Event", event)

    # response = graph.invoke(_state)

    # print(response)


main()
