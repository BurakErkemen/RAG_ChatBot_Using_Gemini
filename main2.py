import streamlit as st
import pdfplumber
import random 
import time


# PDF İçeriğini alma
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text



# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    return response


# Main Metodu
def main():
    st.title("RAG Tabanlı Gemini Chat Bot")

    # Sohbet geçmişini başlatma
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Uygulama yeniden çalıştırıldığında geçmişteki sohbet mesajlarını görüntüleme
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcı girdisini kabul et
    if prompt := st.chat_input("What is up?"):
        # Sohbet geçmişine kullanıcı mesajı ekleme
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Sohbet mesajı kabında kullanıcı mesajını görüntüle
        with st.chat_message("user"):
            st.markdown(prompt)

        # Sohbet mesajı kapsayıcısında asistan yanıtını görüntüleme
        with st.chat_message("assistant"):
            response = response_generator()
            st.write(response)

        #  Sohbet geçmişine asistan yanıtı ekle
        st.session_state.messages.append({"role": "assistant", "content": response})
        

    # Sidebar PDF Yükleme
    st.sidebar.title("PDF Dosyası Yükle")

    uploaded_file = st.sidebar.file_uploader("PDF dosyasını yükleyin", type="pdf")

    if uploaded_file is not None:
        print()



if __name__ == "__main__":
    main()
