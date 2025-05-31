import streamlit as st
import bcrypt
import json
import os
from dotenv import load_dotenv  
import os  
from groq import Groq  
from auth.auth import exibir_tela_login_registro

load_dotenv()

st.set_page_config(
    page_title='Mentorium',
    layout="centered",
    initial_sidebar_state="expanded",
)


if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = None

exibir_tela_login_registro()

st.sidebar.text('Mentorium')
if st.session_state.get('usuario'):
    st.sidebar.success(f"Bem-vindo, {st.session_state.usuario}!")
else:
    st.sidebar.info("Usuário não identificado.")

if st.sidebar.button("Logout"):
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.rerun()


pag1 = st.Page(
    page= "paginas/page_1.py",
    title="Iniciando a Jornada",
    icon='🧙‍♂️',
    default=True
)

pag2 = st.Page(
    page= "paginas/page_2.py",
    title="Alto Conselho do Mentorium",
    icon='🧙‍♂️'
)

paginas = st.navigation({
    "Jornada": [pag1],
    "Àgora": [pag2],
})

paginas.run()

# logins_registro = st.Page(
#     page="paginas/tela_login_e_cadastro.py",
#     title="Login e Registro",
#     icon='🔐',
#     default=True
# )
