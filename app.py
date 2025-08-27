import streamlit as st
from agents.orchestrator import SurgicalAssistant
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Cardiac Surgery Assistant",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App title and description
st.title("❤️ Cardiac Surgery Assistant")
st.caption("AI-powered support for cardiac surgery procedures")


# Initialize the assistant
@st.cache_resource
def get_assistant():
    return SurgicalAssistant()


assistant = get_assistant()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# Sidebar with controls
with st.sidebar:
    st.header("Controls")

    if st.button("Clear Conversation"):
        assistant.clear_history()
        st.session_state.messages = []
        st.session_state.current_patient = None
        st.rerun()

    st.session_state.show_debug = st.checkbox("Show Debug Info", value=False)

    # Display current patient if available
    if st.session_state.current_patient:
        st.info(f"**Current Patient**: {st.session_state.current_patient}")

    st.divider()
    st.info("""
    This AI assistant specializes in cardiac surgery support across:
    - **Pre-operative**: Planning, assessment, device selection
    - **Intra-operative**: Procedural guidance, device instructions
    - **Post-operative**: Recovery protocols, follow-up care
    
    **Tip**: Mention patient IDs (e.g., P003) to get patient-specific responses.
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show debug info if enabled
        if st.session_state.show_debug and message.get("debug_info"):
            with st.expander("Routing Details"):
                st.json(message["debug_info"])

# Chat input
if prompt := st.chat_input("Ask a question about cardiac surgery..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your question..."):
            response_data = assistant.generate_response(prompt)

        # Update current patient if this is a patient-specific query
        if response_data.get("patient_specific") and response_data.get("patient_id"):
            st.session_state.current_patient = response_data.get("patient_id")

        # Display the response
        st.markdown(response_data["response"])

        # Show phase and routing info if debug is enabled
        if st.session_state.show_debug:
            phase_display = {
                "pre-op": "🟢 Pre-operative",
                "intra-op": "🔵 Intra-operative",
                "post-op": "🟣 Post-operative",
            }

            st.info(
                f"**Phase**: {phase_display.get(response_data['phase'], response_data['phase'])}"
            )

            if response_data.get("patient_specific"):
                st.info(f"**Patient**: {response_data.get('patient_id', 'Unknown')}")

            st.caption(f"**Reasoning**: {response_data.get('reasoning', '')}")

            with st.expander("Retrieved Collections"):
                st.write(", ".join(response_data["collections"]))

    # Add assistant response to chat history with debug info
    debug_info = (
        {
            "phase": response_data["phase"],
            "collections": response_data["collections"],
            "patient_specific": response_data.get("patient_specific", False),
            "patient_id": response_data.get("patient_id"),
            "reasoning": response_data.get("reasoning", ""),
        }
        if st.session_state.show_debug
        else None
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_data["response"],
            "debug_info": debug_info,
        }
    )

# Footer
st.divider()
st.caption("""
**Note**: This is a decision support tool. Always verify critical information with clinical guidelines and colleagues.
The AI will automatically determine the appropriate surgical phase and information sources for your query.
""")
