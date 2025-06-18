import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

image_url = "https://i.postimg.cc/BnT8fsYy/livro-fundo.png"

page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #000000;
}}
h1 {{
    color: #1C1C1C !important;
}}
body, .stApp, .stMarkdown, .stChatFloatingInputContainer {{
    color: #000000 !important;
}}
/* Remove fundo da barra superior */
header, [data-testid="stHeader"], [data-testid="stToolbar"] {{
    background: rgba(0,0,0,0);
}}

/* Remove fundo da barra inferior */
.st-emotion-cache-128upt6 {{
    background: rgba(0,0,0,0) !important;
}}

/* Container da entrada de texto */
.stChatInputContainer {{
    background-color: rgba(0, 0, 0, 0.0) !important;
}}

/* Campo de texto */
.stTextInput > div > div > input {{
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 10px;
    padding: 10px;
}}

/* Centralizar o conteúdo */
[data-testid="stAppViewContainer"] > .main {{
    display: flex;
    justify-content: center;
}}

.block-container {{
    max-width: 800px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}}
</style>
"""

llamaChatModel = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

def chat_bot():
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Chatbot dos Magos 🧙‍♂️")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Você é um mago supremo que guiará o usuário na jornada dele. Fale de forma sábia e amigável."}
        ]

    user_input = st.chat_input("Digite sua mensagem:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        messages_for_model = [
            (msg["role"], msg["content"]) for msg in st.session_state.messages
        ]
        response = llamaChatModel.invoke(messages_for_model)
        st.session_state.messages.append({"role": "assistant", "content": response.content})

    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            with st.chat_message('👤'):
                st.markdown(f"**Você:** {msg['content']}")
        else:
            with st.chat_message('🧙‍♂️'):
                st.markdown(f"**Mago:** {msg['content']}")

if __name__ == "__main__":
    chat_bot()
