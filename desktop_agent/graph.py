from typing import Annotated, Sequence, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from tools import tools

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state: AgentState):
    sys_msg = SystemMessage(content="You are a desktop management assistant.")
    return {"messages": [model.invoke([sys_msg] + state["messages"])]}

def should_continue(state: AgentState):
    return "continue" if state["messages"][-1].tool_calls else "end"

workflow = StateGraph(AgentState)
workflow.add_node("our_agent", model_call)
workflow.add_node("tools", ToolNode(tools=tools))
workflow.set_entry_point("our_agent")
workflow.add_conditional_edges("our_agent", should_continue, {"continue": "tools", "end": END})
workflow.add_edge("tools", "our_agent")

compiled_graph = workflow.compile()