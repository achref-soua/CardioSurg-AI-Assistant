from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()


class QueryRouter:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.1,
        )

    def extract_patient_id(self, query: str) -> str:
        """Extract patient ID from query if mentioned"""
        patient_patterns = [
            r"patient\s+([Pp]\d{3})",
            r"([Pp]\d{3})",
            r"pt\s+([Pp]\d{3})",
            r"case\s+([Pp]\d{3})",
        ]

        for pattern in patient_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).upper()  # Standardize to uppercase

        return None

    def route_query(self, query: str) -> Dict[str, Any]:
        """Route a query to determine phase, relevant collections, and patient context"""
        # Extract patient ID if mentioned
        patient_id = self.extract_patient_id(query)

        prompt = ChatPromptTemplate.from_template("""
        You are a medical AI assistant specializing in cardiac surgery. Analyze the following query and determine:
        1. Which surgical phase it relates to (pre-op, intra-op, or post-op)
        2. Which knowledge collections are most relevant to answer it
        3. Whether this query is about a specific patient
        
        Available collections:
        - patients: Patient records and medical history
        - devices: Medical device specifications and instructions
        - guidelines: Clinical practice guidelines
        - literature: Medical research literature
        - notes: Clinical notes from various phases
        
        Query: {query}
        
        Respond with a JSON object in this exact format:
        {{
            "phase": "pre-op|intra-op|post-op",
            "collections": ["collection1", "collection2", ...],
            "patient_specific": true|false,
            "reasoning": "Brief explanation of your routing decision"
        }}
        """)

        chain = prompt | self.llm
        response = chain.invoke({"query": query})

        # Parse response
        try:
            # Try to extract JSON from response
            json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())

                # If we found a patient ID in the query, mark as patient_specific
                if patient_id:
                    result["patient_specific"] = True
                    result["patient_id"] = patient_id
                    result["reasoning"] += (
                        f" Query specifically mentions patient {patient_id}."
                    )

                return result
            else:
                return self._fallback_routing(query, patient_id)
        except json.JSONDecodeError:
            return self._fallback_routing(query, patient_id)

    def _fallback_routing(self, query: str, patient_id: str = None) -> Dict[str, Any]:
        """Fallback routing logic if LLM parsing fails"""
        query_lower = query.lower()

        # Phase detection
        if any(
            term in query_lower
            for term in [
                "pre-op",
                "preoperative",
                "planning",
                "assessment",
                "selection",
                "evaluate",
                "suitable",
            ]
        ):
            phase = "pre-op"
            reasoning = "Query relates to preoperative planning or assessment"
        elif any(
            term in query_lower
            for term in [
                "intra-op",
                "intraoperative",
                "surgery",
                "procedure",
                "deployment",
                "step",
                "during",
                "how to",
            ]
        ):
            phase = "intra-op"
            reasoning = "Query relates to intraoperative procedures or guidance"
        elif any(
            term in query_lower
            for term in [
                "post-op",
                "postoperative",
                "recovery",
                "follow-up",
                "discharge",
                "complication",
                "after surgery",
            ]
        ):
            phase = "post-op"
            reasoning = "Query relates to postoperative care or follow-up"
        else:
            phase = "pre-op"
            reasoning = "Defaulting to pre-op for general queries"

        # Collection detection - always include patients
        collections = ["patients"]

        if any(
            term in query_lower
            for term in ["device", "stent", "graft", "implant", "sizing", "delivery"]
        ):
            collections.append("devices")
        if any(
            term in query_lower
            for term in [
                "guideline",
                "protocol",
                "standard",
                "recommend",
                "best practice",
            ]
        ):
            collections.append("guidelines")
        if any(
            term in query_lower
            for term in [
                "study",
                "literature",
                "research",
                "trial",
                "evidence",
                "outcome",
            ]
        ):
            collections.append("literature")
        if any(
            term in query_lower
            for term in ["note", "record", "history", "previous", "prior"]
        ):
            collections.append("notes")

        # Check if patient-specific
        patient_specific = patient_id is not None
        if patient_specific:
            reasoning += f" Query specifically mentions patient {patient_id}."

        result = {
            "phase": phase,
            "collections": collections,
            "patient_specific": patient_specific,
            "reasoning": reasoning,
        }

        if patient_specific:
            result["patient_id"] = patient_id

        return result
