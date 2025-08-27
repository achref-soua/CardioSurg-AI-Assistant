from abc import ABC, abstractmethod
from typing import List
from langchain_groq import ChatGroq
from langchain.schema import BaseMessage
import os
from rag.retriever import chroma_retriever


class BaseAgent(ABC):
    def __init__(self, system_prompt: str):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.7,
        )
        self.system_prompt = system_prompt
        self.conversation_history = []

    def add_to_history(self, message: BaseMessage):
        """Add a message to conversation history"""
        self.conversation_history.append(message)

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def retrieve_relevant_info(self, query: str, collections: List[str]) -> str:
        """Retrieve relevant information from specified collections"""
        context = ""

        for collection in collections:
            results = chroma_retriever.query_collection(collection, query)
            if results:
                context += f"\n\n--- Information from {collection} ---\n"
                for i, result in enumerate(results[:3]):  # Top 3 results per collection
                    context += f"\n{result['document']}\n"

        return context

    @abstractmethod
    def generate_response(self, query: str, patient_id: str = None) -> str:
        """Generate a response to the query (to be implemented by subclasses)"""
        pass
