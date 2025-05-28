import streamlit as st
import bcrypt
import json
import os
from dotenv import load_dotenv  
import os  
from groq import Groq  


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(
    page_title='Mentorium',
    layout="centered",
    initial_sidebar_state="expanded",
)


if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = None


def verificar_login(usuario, senha):
    """Verifica as credenciais do usuário"""
    if not os.path.exists('usuarios.json'):
        return False
    
    with open('usuarios.json', 'r') as f:
        try:
            usuarios = json.load(f)
            if usuario in usuarios:
                return bcrypt.checkpw(senha.encode('utf-8'), 
                                   usuarios[usuario]['senha'].encode('utf-8'))
        except:
            return False
    return False

def registrar_usuario(usuario, senha, email):
    """Registra um novo usuário"""
    usuarios = {}
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
    
    if usuario in usuarios:
        return False
    
    usuarios[usuario] = {
        'senha': bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'email': email
    }
    
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f)
    
    return True


if not st.session_state.autenticado:
    st.title("Login Mentorium")
    
    aba_login, aba_registro = st.tabs(["Login", "Registrar"])
    
    with aba_login:
        with st.form("login_form"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            enviar = st.form_submit_button("Entrar")
            
            if enviar:
                if verificar_login(usuario, senha):
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
    
    with aba_registro:
        with st.form("registro_form"):
            novo_usuario = st.text_input("Usuário")
            nova_senha = st.text_input("Senha", type="password")
            confirmar_senha = st.text_input("Confirmar senha", type="password")
            email = st.text_input("Email")
            enviar = st.form_submit_button("Registrar")
            
            if enviar:
                if nova_senha != confirmar_senha:
                    st.error("As senhas não coincidem")
                elif registrar_usuario(novo_usuario, nova_senha, email):
                    st.success("Registro realizado com sucesso! Faça login.")
                else:
                    st.error("Usuário já existe")
    
    st.stop()  


st.sidebar.text('Mentorium')
st.sidebar.success(f"Bem-vindo, {st.session_state.usuario}!")

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

logins_registro = st.Page(
    page="paginas/tela_login_e_cadastro.py",
    title="Login e Registro",
    icon='🔐',
    default=True
)


pag1 = st.Page(
    page= "paginas/page_1.py",
    title="Iniciando a Jornada",
    icon='🧙‍♂️',
)

pag2 = st.Page(
    page= "paginas/page_2.py",
    title="Alto Conselho do Mentorium",

)

paginas = st.navigation({
    "Jornada": [pag1],
    "Àgora": [pag2],
})
    }

    icon='🧙‍♂️'

)

paginas = st.navigation({
    "Jornada": [pag1],
    "Àgora": [pag2],
})

paginas.run()