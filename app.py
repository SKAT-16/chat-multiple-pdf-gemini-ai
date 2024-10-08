import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        if pdf is not None:
            try:
                # Read and wrap the PDF bytes in BytesIO
                pdf_bytes = pdf.read()
                pdf_reader = PdfReader(BytesIO(pdf_bytes))
                for page in pdf_reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text
            except Exception as e:
                st.error(f"Error processing {pdf.name}: {e}")
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details,
    if the answer is not in the provided context just say, "answer is not available in the context",
    dont provide the wrong answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
    except Exception as e:
        st.error(f"Error loading vector store: {e}")
        return

    chain = get_conversational_chain()

    try:
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        st.write("Reply: ", response["output_text"])
    except Exception as e:
        st.error(f"Error generating response: {e}")

def main():
    # Set page configuration with a custom theme
    st.set_page_config(
        page_title="Chat PDF",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS styles
    st.markdown("""
        <style>
            /* Header customization */
            .css-18e3th9 {
                background-color: #4CAF50;
                color: white;
            }
            /* Sidebar customization */
            .css-1d391kg {
                background-color: #2196F3;
                color: white;
            }
            /* Main content customization */
            .css-1cpxqw2 {
                background-color: #f0f0f0;
            }
        </style>
    """, unsafe_allow_html=True)

    st.header("Chat with multiple PDFs using Gemini AI 👋")

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload your PDF files and click on the Submit button.", accept_multiple_files=True, type=["pdf"])
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("PDF processed successfully!")
                    else:
                        st.error("No text extracted from the uploaded PDFs.")
            else:
                st.error("No PDF files uploaded.")

    user_question = st.text_input("Ask a question about the PDFs: ")

    if user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()
