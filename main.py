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

css_file_path = "style/style.css"
try:
    with open(css_file_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Erro: O arquivo CSS '{css_file_path}' não foi encontrado. Verifique o caminho.")
except UnicodeDecodeError:
    st.error(f"Erro de codificação ao ler o arquivo CSS '{css_file_path}'. Verifique se ele está salvo como UTF-8.")


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