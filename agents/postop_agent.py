from .base_agent import BaseAgent
from rag.prompt_templates import POSTOP_SYSTEM_PROMPT
from langchain.schema import HumanMessage, SystemMessage


class PostOpAgent(BaseAgent):
    def __init__(self):
        super().__init__(POSTOP_SYSTEM_PROMPT)

    def generate_response(self, query: str, patient_id: str = None) -> str:
        # Build context based on query
        collections = ["patients", "guidelines", "notes", "literature"]
        if patient_id:
            query = f"Patient {patient_id}: {query}"

        context = self.retrieve_relevant_info(query, collections)

        # Prepare messages
        messages = [
            SystemMessage(content=self.system_prompt),
            *self.conversation_history[-6:],  # Last 3 exchanges for context
            HumanMessage(content=f"Context: {context}\n\nQuestion: {query}"),
        ]

        # Generate response
        response = self.llm.invoke(messages)

        # Update history
        self.add_to_history(HumanMessage(content=query))
        self.add_to_history(response)

        return response.content
