# 📄 Chat with Multiple PDFs using Google Gemini AI

This project is a Streamlit-based application that allows users to upload multiple PDFs, process the content, and ask questions about the uploaded files. The answers are generated using the Google Gemini AI with the LangChain framework.

## ✨ Features

- Upload multiple PDF files.
- Extract and process text from PDFs.
- Create vector stores using Google Generative AI embeddings.
- Ask questions about the PDF content and get detailed answers.
- Powered by Google Generative AI (Gemini) and LangChain.
- Friendly and interactive user interface built with Streamlit.

## 🛠️ Installation and Setup

To run the project locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chat-pdf-google-gemini.git
cd chat-pdf-google-gemini
```

### 2. Set up a virtual environment

It's recommended to use a virtual environment to manage your dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the required dependencies

Install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

**Required Libraries:**

- `streamlit`
- `PyPDF2`
- `langchain`
- `langchain-google-genai`
- `google-generativeai`
- `faiss-cpu`
- `python-dotenv`

### 4. Set up environment variables

Create a `.env` file in the root of the project with your Google Generative AI API key:

```
GOOGLE_API_KEY=your-google-api-key
```

Replace `your-google-api-key` with your actual API key.

### 5. Run the app

Launch the Streamlit app using the following command:

```bash
streamlit run app.py
```

## 🖼️ User Interface

- **PDF Upload:** Upload one or more PDF files from the sidebar.
- **Question:** Ask a question related to the uploaded PDFs, and the AI will provide a detailed answer.
- **Processing:** The app extracts text from the PDFs and creates vector embeddings for better semantic search.

## 🔧 How It Works

1. **PDF Upload:** Users can upload multiple PDF files from the sidebar.
2. **Text Extraction:** Text is extracted from the uploaded PDFs using `PyPDF2`.
3. **Text Chunks:** The text is split into smaller chunks using `RecursiveCharacterTextSplitter` to prepare for vectorization.
4. **Vector Store Creation:** The chunks are embedded using `GoogleGenerativeAIEmbeddings` and stored in a FAISS vector database.
5. **Question Answering:** Users can input questions, and the app uses LangChain's `load_qa_chain` and Google Gemini AI (`ChatGoogleGenerativeAI`) to answer the questions based on the uploaded PDF content.

## ⚠️ Important Notes

- Make sure to set the `allow_dangerous_deserialization` flag to `True` only when loading trusted vector stores created by your app to avoid security risks.
- Large PDFs or multiple PDFs might take a few moments to process, so be patient while the app works.

## 🌟 Future Enhancements

- Add support for other document formats (Word, Excel).
- Improve response time for large documents.
- Add more interactive features like document search and highlighting.
