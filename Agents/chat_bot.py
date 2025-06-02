import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Inicialize o modelo
llamaChatModel = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

def chat_bot():
    st.title("Chatbot dos Magos 🧙‍♂️")

    # Histórico de mensagens na sessão
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Você é um mago supremo que guiará o usuário na jornada dele. Fale de forma sábia e amigável."}
        ]

    # Caixa de entrada do usuário
    user_input = st.chat_input("Digite sua mensagem:")

    if  user_input:
        # Adiciona mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Prepara mensagens para o modelo
        messages_for_model = [
            (msg["role"], msg["content"]) for msg in st.session_state.messages
        ]

        # Chama o modelo
        response = llamaChatModel.invoke(messages_for_model)
        st.session_state.messages.append({"role": "assistant", "content": response.content})

    # Exibe o histórico do chat
    for msg in st.session_state.messages[1:]:
            if msg["role"] == "user":
                with st.chat_message('👤'):
                    st.markdown(f"**Você:** {msg['content']}")
            else:
                with st.chat_message('🧙‍♂️'):
                    st.markdown(f"**Mago:** {msg['content']}")