import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import pdfplumber
import os
import random
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.ai.generativelanguage as glm
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from streamlit_chat import message
from langchain_google_genai import GoogleGenerativeAIEmbeddings 

import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Set the Google API key for Gemini
genai.api_key = os.getenv('AIzaSyC_NFugLx75aVxxu8m0uuiFaIa7WvD64kA')
# Sidebar
with st.sidebar:
    st.title("FU BOT")
    st.markdown('''
##About
                This app is an LLM-powered chatbot built using:
                - [Streamlit](https://streamlit.io/)
                - [LangChain](https://python.langchain.com/)
                - [Google AI](https://platform.openai.com/docs/models) 
                - LLM model
                
''')
    
    add_vertical_space(5)

st.write("""
# 'FU BOT' Belongs to Fırat University Faculty of Technology Software Engineering
""")
# Initialize LangChain LLM and Memory
llm = genai.GenerativeModel('gemini-pro')


pinecone.init(      
    api_key='02c6541b-2b28-496d-a81e-5bd1ab3fafb1',      
    environment='gcp-starter'      
)      
index = pinecone.Index('chatbot')


# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return pages

# Function to embed and store text
def embed_and_store(pages, embeddings_model):
    docsearch = pinecone.from_texts(pages, embeddings_model, index_name="chatbot")
    return docsearch

# Function to check if PDF has been processed
def has_been_processed(file_name):
    processed_files = set()
    if os.path.exists("processed_files.txt"):
        with open("processed_files.txt", "r") as file:
            processed_files = set(file.read().splitlines())
    return file_name in processed_files

# Function to mark PDF as processed
def mark_as_processed(file_name):
    with open("processed_files.txt", "a") as file:
        file.write(file_name + "\n")

# Function to handle user input
def handle_enter():
    if 'retriever' in st.session_state:
        user_input = st.session_state.user_input
        if user_input:
            if len(user_input.split()) > 4097:
                st.warning("Girdi çok uzun! Lütfen daha kısa bir soru sorun.")
                return
            st.session_state.chat_history.append(("You", user_input))
            with st.spinner("Please wait..."):
                try:
                    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=st.session_state.retriever)
                    bot_response = qa.run(user_input)
                    st.session_state.chat_history.append(("Bot", bot_response))
                except Exception as e:
                    st.session_state.chat_history.append(("Bot", f"Error - {e}"))
            st.session_state.user_input = ""

# Main function

def main():
    st.title("Ask a PDF Questions")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    uploaded_file = st.file_uploader("Upload your PDF here", type="pdf")

    if uploaded_file:
        file_name = uploaded_file.name
        if not has_been_processed(file_name):
            with st.spinner("Processing PDF..."):
                pages = extract_text_from_pdf(uploaded_file)
                embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyC_NFugLx75aVxxu8m0uuiFaIa7WvD64kA")
                vectordb = embed_and_store(pages, embeddings_model)
                st.session_state.retriever = vectordb.as_retriever()
                mark_as_processed(file_name)
                st.success("PDF Processed and Stored!")
                st.session_state.pdf_processed = True
        else:
            if 'retriever' not in st.session_state:
                with st.spinner("Loading existing data..."):
                    index_name = "chatbot"
                    embeddings = GoogleGenerativeAIEmbeddings(google_api_key="AIzaSyC_NFugLx75aVxxu8m0uuiFaIa7WvD64kA")  # Use GoogleEmbeddings for Gemini
                    docsearch = Pinecone.from_existing_index(index_name, embeddings)
                    st.session_state.retriever = docsearch.as_retriever()
                st.info("PDF already processed. Using existing data.")
                st.session_state.pdf_processed = True
    
    if st.session_state.pdf_processed:
        for idx, (speaker, text) in enumerate(st.session_state.chat_history):
            if speaker == "Bot":
                message(text, key=f"msg-{idx}")
            else:
                message(text, is_user=True, key=f"msg-{idx}")

        st.text_input("Enter your question here:", key="user_input", on_change=handle_enter)

        if st.session_state.user_input:
            handle_enter()
if __name__ == "__main__":
    main()
