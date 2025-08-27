# Define reusable nodes for LangGraph workflows
# These can be expanded for more complex workflows


def retrieval_node(state):
    """Node for retrieving relevant information"""
    query = state.get("query")
    collections = state.get("collections", ["patients", "devices", "guidelines"])

    # Import here to avoid circular imports
    from rag.retriever import chroma_retriever

    context = ""
    for collection in collections:
        results = chroma_retriever.query_collection(collection, query)
        if results:
            context += f"\n\n--- Information from {collection} ---\n"
            for i, result in enumerate(results[:3]):
                context += f"\n{result['document']}\n"

    return {"context": context}


def generation_node(state):
    """Node for generating responses based on context"""
    query = state.get("query")
    context = state.get("context", "")
    system_prompt = state.get("system_prompt", "")

    # Import here to avoid circular imports
    from langchain_groq import ChatGroq
    from langchain.schema import HumanMessage, SystemMessage
    import os

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.7,
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context: {context}\n\nQuestion: {query}"),
    ]

    response = llm.invoke(messages)
    return {"response": response.content}
