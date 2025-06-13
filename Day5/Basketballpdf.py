import os
import streamlit as st
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="PDF Q&A with MiniLMv6 + Gemini", page_icon="📄")
st.title("📄 Ask Questions from a PDF using MiniLMv6 + Gemini")
st.markdown("Upload a PDF, and ask questions based on its content. Powered by **RAG + MiniLMv6 + Gemini**.")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_pdf_path = tmp_file.name

    try:
        # Step 1: Load and split PDF
        loader = PyMuPDFLoader(temp_pdf_path)
        documents = loader.load()

        splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        docs = splitter.split_documents(documents)

        # Step 2: MiniLMv6 Embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        # Step 3: Gemini LLM (for answering)
        GOOGLE_API_KEY = "AIzaSyAqcBTXNby8fUtg4dsDFZt_9ac228kgUU4"  # Replace with your actual key
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3
        )

        # Step 4: RAG Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        st.success("PDF processed successfully! You can now ask questions.")
        query = st.text_input("Enter your question:")

        if st.button("Get Answer"):
            if not query.strip():
                st.warning("Please enter a question.")
            else:
                result = qa_chain.invoke({"query": query})

                st.markdown("### 🧠 Answer:")
                st.write(result["result"])

                with st.expander("🔍 Source Document Snippets"):
                    for doc in result["source_documents"]:
                        st.text(doc.page_content[:300] + "...")
    except Exception as e:
        st.error(f"Failed to process PDF: {e}")
else:
    st.info("Please upload a PDF to begin.")