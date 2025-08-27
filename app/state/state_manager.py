import streamlit as st
from agents.orchestrator import Orchestrator


class StateManager:
    def __init__(self):
        if "orchestrator" not in st.session_state:
            st.session_state.orchestrator = Orchestrator()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "current_patient" not in st.session_state:
            st.session_state.current_patient = None

        if "current_phase" not in st.session_state:
            st.session_state.current_phase = "pre-op"

    def get_orchestrator(self) -> Orchestrator:
        return st.session_state.orchestrator

    def add_message(self, role: str, content: str):
        st.session_state.messages.append({"role": role, "content": content})

    def get_messages(self):
        return st.session_state.messages

    def clear_messages(self):
        st.session_state.messages = []
        st.session_state.orchestrator.clear_history()

    def set_patient(self, patient_id: str):
        st.session_state.current_patient = patient_id

    def get_patient(self) -> str:
        return st.session_state.current_patient

    def set_phase(self, phase: str):
        st.session_state.current_phase = phase
        st.session_state.orchestrator.set_phase(phase)

    def get_phase(self) -> str:
        return st.session_state.current_phase


# Singleton instance
state_manager = StateManager()
