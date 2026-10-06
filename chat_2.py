# Conditional Edges and smart Routing

from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END # importing the edges START and END
from langchain_ollama import ChatOllama


llm_1 = ChatOllama(
    model="gemma4:e2b",
    base_url="http://localhost:11434",
    temperature=0.7,
)

# alternate or stronger model for feedback
llm_2 = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",
    temperature=0.2,
    
)

class State(TypedDict):
    user_query: str # (state: 1)
    llm_output: Optional[str] # (state: 2)
    is_good: Optional[bool] # rating if output is good or not (state: 3)


# defining a node   (node 1: initial Chatbot)
def chatbot(state: State):
    print("ChatBot Node", state)
    response = llm_1.invoke(state.get("user_query"))


    state["llm_output"] = response.content
    return state


# creating another node i.e for evaluation
def evaluate_response(state: State) -> Literal["chatbot_qwen", "endnode"]:
    print("evaluate_response Node", state)
    if True:  # check with False
        return "endnode" # node id where we want to re-direct

    else:
        return "chatbot_qwen" # node id where we want to re-direct


# assuming there is a better node 
def chatbot_qwen(state: State): # does the same thing but with a different model
    print("chatbot_qwen Node", state)
    response = llm_2.invoke(state.get("user_query"))

    state["llm_output"] = response.content
    return state


# creating a end node
def endnode(state: State):
    print("endnode Node", state)
    return state # does nothing and returns the state

    
# constructing graph
graph_builder = StateGraph(State)

# nodes are ready so registering them
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_qwen", chatbot_qwen)
graph_builder.add_node("endnode", endnode)


# defining the edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response) # as evaluate_response is conditional using .add_conditional_edges

graph_builder.add_edge("chatbot_qwen", "endnode")
graph_builder.add_edge("endnode", END)


# compiling the graph
graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, What is 3 * 3  = ?"}))
print(updated_state)


# OUTPUT : if True
# evaluate_response Node {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 = 9'}
# endnode Node {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 = 9'}
# {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 = 9'}



# OUTPUT : if False
# ChatBot Node {'user_query': 'Hey, What is 3 * 3  = ?'}
# evaluate_response Node {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 = 9'}
# chatbot_qwen Node {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 = 9'}
# endnode Node {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 equals 9.'}
# {'user_query': 'Hey, What is 3 * 3  = ?', 'llm_output': '3 * 3 equals 9.'}