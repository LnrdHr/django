from typing import Annotated
import os
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch
import json
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

"""I could've used prebuilt nodes that replace BasicToolNode and route_tools, 
but for learning purposes I wanted to build them from scratch."""

load_dotenv(".env")

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

#A node that runs the tools requested in the last received message
class BasicToolNode:

    def __init__(self, tools: list):
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs:dict):
        if messages := inputs.get("messages",[]):
            message = messages[-1]
        else:
            raise ValueError("No messages found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    
def route_tools(state: State):
        """ 
        Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end.
        """
        if isinstance(state,list): #state is a list
            ai_message = state[-1]
        elif messages := state.get("messages",[]): #state is a dictionary
            ai_message = messages[-1]
        else:
            raise ValueError("No messages found in state")
        
        #if there was a tool call in the last message, we will route to the tools node
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return END

graph_builder = StateGraph(State)
tool = TavilySearch(max_results=2)
tools = [tool]
memory = MemorySaver() #checkpointer.In a production version it would be a connected to a database

""" chatbot only saves history of conversation in one thread
(is it possible to have multiple threads in a single conversation?)"""
config = {"configurable": {"thread_id": "1"}} 
tool_node = BasicToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools, #the chatbot node can go to the tools node or to the end node
    {
        "tools": "tools",
        END: END,
    }
)
graph_builder.add_edge("tools", "chatbot")

llm = init_chat_model("openai:gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

#this is called a node
#returns a dictionary of updated messages
def chatbot(state: State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot",chatbot)
#adding the entry point, so that the graph knows where to start its work each time it's run
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot",END)
#compiling the graph.This creates a CompiledStateGraph which we can invoke on our state
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input=" "):
    events = graph.stream(
        {"messages" : [{"role":"user", "content": user_input}]},
        config,
        stream_mode="values"
    )
    for event in events:
        print(event["messages"][-1])


while True:
    try:
        user_input = input("User: ")
        if user_input == "q": 
            print("Conversation ended.\nBye!")
            break
        
        stream_graph_updates(user_input)
        
    
    except:
        raise RuntimeError("Something went wrong while trying to read user input.")
