from app.api_utils import list_documents
from app.api_utils import upload_document
import streamlit as st


def display_sidebar():
    # sidebar: model selection
    model_options = ["gpt-4o", "gpt-4o-mini"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # sidebar:upload document
    st.sidebar.header("Upload Document")
    upload_file = st.sidebar.file_uploader(
        "choose a file", type=["pdf", "docx", "html"]
    )
    if upload_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("uploading...."):
                upload_response = upload_document(upload_file)
                if upload_response:
                    st.sidebar.success(
                        f"file '{upload_file.name}' uploaded successfully with ID {upload_response.get('file_id')}"
                    )
                    st.session_state.documents = list_documents()

    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("refresh document list"):
        with st.spinner("refreshing...."):
            st.session_state.documents = list_documents()

    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(
                f"{doc.file_name} (ID: {doc['id']}, Uploaded: {doc['uploaded_timestamp']})"
            )

            selected_file_id = st.sidebar.selectbox(
                "Select a document to delete",
                options=[doc["id"] for doc in documents],
                format_func=lambda x: next(
                    doc["filename"] for doc in documents if doc["id"] == x
                ),
            )
