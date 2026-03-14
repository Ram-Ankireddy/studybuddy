import os
import tempfile
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from ingest import ingest_pdf

load_dotenv()

def load_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return vectorstore

def get_qa_chain(vectorstore):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 6}
    )
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful study assistant. Use the context below to answer the question.

    If the question asks for a summary, summarize all the provided context thoroughly.
    If the question asks something specific, answer based only on the context.
    If the answer is truly not in the context, say "I don't find that information in the document."

    Context: {context}

    Question: {question}
    """)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

# Streamlit UI
st.title("📄 StudyBuddy")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file:
    if st.session_state.get("uploaded_filename") != uploaded_file.name:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
        with st.spinner("Processing PDF..."):
            ingest_pdf(temp_file_path)
        st.session_state.uploaded_filename = uploaded_file.name
        if "chain" in st.session_state:
            del st.session_state.chain
        st.success("PDF processed! You can now ask questions.")

if "uploaded_filename" not in st.session_state:
    st.info("Please upload a PDF to get started.")
    st.stop()

st.subheader("Ask anything about your document")

if "chain" not in st.session_state and "uploaded_filename" in st.session_state:
    with st.spinner("Loading your document..."):
        vectorstore = load_vectorstore()
        st.session_state.chain = get_qa_chain(vectorstore)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = st.session_state.chain.invoke(prompt)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})