import streamlit as st
from app.sidebar import display_sidebar


def main():
    st.title("Langchain RAG")

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    # Display the sidebar
    display_sidebar()


if __name__ == "__main__":
    main()

