from typing_extensions import TypedDict


class State(TypedDict):
    query: str
    llm_result: str | None

def chat_bot(state: State):
    query = state['query']
    # llm call
    result = "Hello, how can i help you?"
    state["llm_result"] = result
    
    return state

