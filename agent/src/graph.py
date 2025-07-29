from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from nodes.reasoning_node import reasoning_node
from nodes.tool_nodes import rag_tool_node, tavily_tool_node

class ChatState(TypedDict):
    history: List[str]
    user_input: str
    result: str

graph = StateGraph(ChatState)

graph.add_node("reasoning", reasoning_node)
graph.add_node("rag_tool", rag_tool_node)
graph.add_node("tavily_tool", tavily_tool_node)

def choose_tool(state):
    decision = state.get("decision", "")
    if "tool_call:rag" in decision:
        return "rag_tool"
    elif "tool_call:tavily" in decision:
        return "tavily_tool"
    else:
        return END

graph.add_conditional_edges("reasoning", choose_tool)
graph.add_edge("rag_tool", END)
graph.add_edge("tavily_tool", END)
graph.set_entry_point("reasoning")

app = graph.compile()
