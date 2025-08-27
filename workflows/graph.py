from langgraph.graph import StateGraph, END
from .nodes import retrieval_node, generation_node

# Define the state structure
from typing import TypedDict, List, Optional


class GraphState(TypedDict):
    query: str
    phase: str
    collections: List[str]
    context: Optional[str]
    response: Optional[str]
    system_prompt: str


def create_workflow():
    """Create a LangGraph workflow for the surgical assistant"""
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("retrieve", retrieval_node)
    workflow.add_node("generate", generation_node)

    # Define edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


# Create the workflow instance
surgical_workflow = create_workflow()
