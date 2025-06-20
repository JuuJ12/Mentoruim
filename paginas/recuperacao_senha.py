import streamlit as st
from auth.auth_firebase import recuperar_senha
def mostrar_recuperacao_senha():
    st.title("Recuperação de Senha")
    email = st.text_input("Digite seu e-mail:")
    if st.button("Enviar Link de Recuperação"):
        if not email:
            st.error("Por favor, insira um e-mail válido.")
            return
        else:
            if recuperar_senha(email):
                st.success("Link de recuperação enviado para o seu e-mail.")
            else:
                st.error("Erro ao enviar o link de recuperação.")