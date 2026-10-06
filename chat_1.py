from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END # importing the edges START and END
from langchain_ollama import ChatOllama
#from langchain.chat_models import init_chat_model


# integrating llm into langGraph
llm = ChatOllama(
    model = "qwen2.5:7b",
    base_url="http://localhost:11434",
)

# creating a state / defining graph state
class   State(TypedDict): # State is a TypedDictionary
    messages: Annotated[list, add_messages]


# creating a node 
def chatbot(state: State):
  # print("\n\nInside chatbot node", state)
    response = llm.invoke(state.get("messages")) # Sends accumulated messages to the Ollama model
  # return {"messages": ["Hi, This is a message from ChatBot Node"]}
    return {"messages": [response]}

# creating another node
def sampleNode(state: State):
    print("\n\nInside sampleNode node", state)
    return {"messages": ["Sample message Appended"]}



# constructing graph 
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot) # now the graph knows there is node i.e chatbot
# state = {messages: ["Hey there"]}
# node runs : chatbot(state : ["Hey there"]) --> ["Hi, This is a message from ChatBot Node"]
# state = {messages: ["Hey there", "Hi, This is a message from ChatBot Node"]}
graph_builder.add_node("sampleNode", sampleNode)



# now nodes are ready we need to connect them (edges)
# defining the edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

# (START) --> chatbot --> sampleNode --> (END)


# Compiling the graph
graph = graph_builder.compile()


# running the graph
updated_state = graph.invoke(State({"messages": ["Hi, This is SuperMan!!"]}))
print("\n\nupdated_state", updated_state)



