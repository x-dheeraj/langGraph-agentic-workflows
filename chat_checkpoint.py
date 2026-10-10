from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END # importing the edges START and END
from langchain_ollama import ChatOllama
from langgraph.checkpoint.mongodb import MongoDBSaver



# llm setup 
llm = ChatOllama(
    model = "qwen2.5:7b",
    base_url="http://localhost:11434",
)

# creating a state / defining graph state
class State(TypedDict): # State is a TypedDictionary
    messages: Annotated[list, add_messages]


# creating a node 
def chatbot(state: State):
    response = llm.invoke(state.get("messages")) # Sends accumulated messages to the Ollama model
    return {"messages": [response]}


# constructing graph 
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot) 


# defining edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

    
# MongoDB URI with authSource=admin
DB_URI = "mongodb://admin:admin@localhost:27017/?authSource=admin"

config = {
        "configurable": { 
            "thread_id": "BatMan" # try changing "SuperMan" to "BatMan"
        }
}


# keeping the invocation inside the checkpointer context
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)

    # first invocation : introducing the person
    updated_state = graph_with_checkpointer.invoke(
    {"messages": ["my power's include flight, super strength, super speed, invulnerability, heat vision, X-ray vision, and super breath."]}, # Hey, my name is Kal-El ----> my power's include flight, super strength, super speed, invulnerability, heat vision, X-ray vision, and super breath.
    config=config,
        )
    print("\nResponse 1:")
    print(updated_state["messages"][-1].content)

    # second invocation : verifying memory retention
    followup_state = graph_with_checkpointer.invoke(
    {"messages": ["What is my name?"]}, # What is my name ?" ----> Do i have the power Heat Vision? ---> changing thread_id and asking : What is my name?
    config=config,
       )
    
    print("\nResponse 2:")
    print(followup_state["messages"][-1].content)



# OUTPUT :
# Response 1:
# Hello Kal-El! It's a pleasure to meet you. As Kal-El, are you perhaps from Krypton or have you come from a different planet? I'm here to assist you with any questions or topics you'd like to discuss, whether they are related to your background or something else entirely. How can I help you today?

# Response 2:
# Your name is Kal-El. How can I assist you further with this or any other information related to your character or interests?




# Response 1:
# Got it, Kal-El! Here’s a summary of your powers:

# - **Flight**: The ability to fly at supersonic speeds.
# - **Super Strength**: Unusually high physical strength, allowing you to lift or move heavy objects with ease.
# - **Super Speed**: The ability to move at incredible speeds, both in running and reaction times.
# - **Invulnerability**: Resistance to physical damage, making it difficult for you to be harmed by normal means.
# - **Heat Vision**: The ability to emit intense heat from your eyes.
# - **X-ray Vision**: The ability to see through solid objects.
# - **Super Breath**: The ability to exhale a freezing cold or hot blast of air.

# If you have any specific questions about these powers, or if you'd like to explore how you might use them in different scenarios, feel free to ask!

# Response 2:
# Yes, Kal-El, you do have the power of Heat Vision. This ability allows you to emit intense heat from your eyes, which can be used for various purposes such as cooking food, melting metal, or even as a defensive or offensive weapon.

# Is there anything specific you'd like to know about your Heat Vision, or are you ready to explore other aspects of your powers or character?




# Output after changing the config "thread_id":  "SuperMan" --> "BatMan" and asking What is my name ?

# Response 1:
# Got it! You have a comprehensive set of superpowers. Here’s a summary of your abilities and some potential uses:

# 1. **Flight**:
#    - **Use**: Quickly reach high altitudes, avoid danger, or escape from threats.
#    - **Examples**: Evading aerial attacks, delivering urgent messages, or rescuing people from tall buildings.

# 2. **Super Strength**:
#    - **Use**: Lift or move heavy objects, break through obstacles, or engage in powerful combat.
#    - **Examples**: Moving large machinery, rescuing people from collapsed buildings, or stopping a truck that’s out of control.

# 3. **Super Speed**:
#    - **Use**: Move incredibly fast, outmaneuver enemies, or quickly reach destinations.
#    - **Examples**: Escaping from danger, delivering emergency aid, or outrunning a pursuing vehicle.

# 4. **Invulnerability**:
#    - **Use**: Protect yourself from physical and environmental attacks.
#    - **Examples**: Surviving explosions, falling from great heights, or withstanding intense heat or cold.

# 5. **Heat Vision**:
#    - **Use**: Create fire, melt metals, or heat up objects and food.
#    - **Examples**: Igniting flammable materials, melting through obstacles, or warming up food.

# 6. **X-ray Vision**:
#    - **Use**: See through solid objects, detect hidden objects or people, or perform medical diagnostics.
#    - **Examples**: Locating hidden explosives, finding a missing person behind a wall, or identifying internal injuries.

# 7. **Super Breath**:
#    - **Use**: Blow away enemies, extinguish fires, or lift heavy objects.
#    - **Examples**: Knocking down enemies, extinguishing a fire, or lifting a heavy object.

# With these powers, you can handle a wide range of situations, from combat and rescue operations to everyday challenges. How do you plan to use these abilities in your next adventure?

# Response 2:
# Your name hasn't been mentioned yet. Since you're a character with such an impressive set of abilities, you might want to choose a name that reflects your powers and persona. Here are a few suggestions:

# 1. **Phoenix**: Inspired by your invulnerability and the ability to rise from the ashes.
# 2. **Therion**: Meaning "beast" in Greek, it can reflect your strength and speed.
# 3. **Ignis**: Meaning "fire" in Latin, it ties well with your heat vision.
# 4. **Aether**: Reflecting your flight and connection to the sky.
# 5. **Radiant**: Reflecting your invulnerability and the heat vision.
# 6. **Triton**: If you have a sea-themed element to your powers, this could be fitting.
# 7. **Maverick**: Reflecting your unique and powerful abilities.

# If you have any preferences or specific themes in mind, feel free to share, and I can suggest more tailored names!



#   Result : name is lost as the thread_id is changed from "SuperMan" to "BatMan"