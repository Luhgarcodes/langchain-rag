from api.db_utils import insert_application_logs
from fastapi import FastAPI
from api.db_utils import get_chat_history
import uuid
import logging

from api.langchain_utils import get_rag_chain
from pydantic import QueryResponse, QueryInput

app = FastAPI()


@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id
    logging.info(
        f"Session ID: {session_id}, User Query:{query_input.question}, Model: {query_input.model.value}    Query received: {query_input}"
    )
    if not session_id:
        session_id = str(uuid.uuid4())

    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(query_input.model.value)
    answer = rag_chain.invoke(
        {"input": query_input.question, "chat_history": chat_history}
    )["answer"]

    insert_application_logs(
        session_id, query_input.question, answer, query_input.model.value
    )
    logging.info(f"session ID: {session_id} AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)


from fastapi import UploadFile, File, HTTPException
import os
import shutil
