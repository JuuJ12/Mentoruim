import streamlit as st
import bcrypt
import json
import os
import re
import time


USUARIOS_FILE = 'usuarios.json'
ALLOWED_DOMAINS = ["gmail.com", "outlook.com", "hotmail.com"] 
MIN_PASSWORD_LENGTH = 6 
MAX_NAME_LENGTH = 100 

def is_valid_email_format(email_str):
    """Verifica o formato básico do e-mail e o domínio."""
    if not email_str:
        return False, "O pergaminho do e-mail não pode estar em branco."
    
    
    email_str = email_str.strip()

    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email_str):
        return False, "Esse não parece ser um pergaminho válido de comunicação. Verifique teu e-mail, jovem aprendiz." # CT-AUT-13

    domain = email_str.split('@')[1].lower()
    if domain not in ALLOWED_DOMAINS:
        return False, f"Este domínio não é reconhecido pelo Conselho Arcano. Use domínios como: {', '.join(ALLOWED_DOMAINS)}." # CT-AUT-22
    return True, email_str 

def is_strong_password(password_str):
    """Verifica a força da senha."""
    if not password_str:
        return False, "A senha não pode ser um feitiço vazio."
    if len(password_str) < MIN_PASSWORD_LENGTH:
        return False, f"Tua senha é frágil como pergaminho molhado. Fortaleça-a com mais símbolos místicos (mín. {MIN_PASSWORD_LENGTH} runas)." # CT-AUT-14
    return True, ""

def sanitize_full_name(name_str):
    """Sanitiza e trunca o nome completo."""
    if not name_str:
        return "", False 
    
    name_str = name_str.strip()
    name_str = re.sub(r'<script.*?>.*?</script>', '', name_str, flags=re.IGNORECASE)
    
    truncated = False
    if len(name_str) > MAX_NAME_LENGTH:
        name_str = name_str[:MAX_NAME_LENGTH]
        truncated = True 
    return name_str, truncated

def load_users():
    """Carrega usuários do arquivo JSON."""
    if not os.path.exists(USUARIOS_FILE) or os.path.getsize(USUARIOS_FILE) == 0:
        return {}
    try:
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except IOError:
        st.error("Falha ao acessar os registros arcanos (arquivo de usuários).")
        return {}


def save_users(users_data):
    """Salva usuários no arquivo JSON."""
    try:
        with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=4)
        return True
    except IOError: 
        return False



def verificar_login(email, senha):
    """Verifica as credenciais do usuário (e-mail como username)."""
    usuarios = load_users()
    email = email.strip() 
    
    if email in usuarios:
        user_data = usuarios[email]
    
        hashed_password_str = user_data['senha']
        if bcrypt.checkpw(senha.encode('utf-8'), hashed_password_str.encode('utf-8')):
            return True, usuarios[email].get("nome_completo", email) 
    return False, None


def registrar_usuario(nome_completo, email, senha):
    """Registra um novo usuário. Retorna (status_code, message_or_data)"""
    usuarios = load_users()

    
    email_original = email 
    is_valid, email_or_error_msg = is_valid_email_format(email)
    if not is_valid: 
        return "validation_error", email_or_error_msg
    email = email_or_error_msg 

    if email in usuarios:
        return "email_exists", "Este e-mail já está gravado nas runas do Mentorium. Tente fazer o login."

    nome_sanitizado, foi_truncado = sanitize_full_name(nome_completo)
    if not nome_sanitizado:
        return "validation_error", "O nome completo não pode ser vazio."

    
    senha_processada = senha.strip()
    if not is_strong_password(senha_processada)[0]:
         return "validation_error", is_strong_password(senha_processada)[1]


    hashed_password = bcrypt.hashpw(senha_processada.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    usuarios[email] = {
        'nome_completo': nome_sanitizado,
        'senha': hashed_password
        # Aqui seria um bom lugar para adicionar 'email_confirmado': False
        # e iniciar o fluxo de envio de e-mail de confirmação (CT-AUT-11)
    }

    if not save_users(usuarios):
        return "save_error", "As redes arcanas falharam ao tentar gravar teu nome. Tente novamente mais tarde."

    success_message = "Inscrição concluída! Teu nome foi gravado nos registros sagrados."
    if foi_truncado: 
        success_message += " (Observação: Teu nome foi abreviado para caber nos registros antigos.)"
    
    # Lógica de envio de e-mail de confirmação (CT-AUT-11) iria aqui:
    # send_confirmation_email(email, nome_sanitizado)

    return "success", success_message


def exibir_tela_login_registro():
    """Exibe a tela de login ou registro se o usuário não estiver autenticado."""
    
    if st.session_state.get('autenticado', False):
        return
    
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Login"
    
    if 'registration_errors' not in st.session_state:
        st.session_state.registration_errors = {}
    
    if 'registration_inputs' not in st.session_state:
        st.session_state.registration_inputs = {"nome": "", "email": "", "senha": "", "conf_senha": ""}


    if not st.session_state.get('autenticado', False):
        st.title("Login Mentorium")
        
        
        def on_tab_change():
            st.session_state.registration_errors = {}

        tab_login, tab_registro = st.tabs(["Login", "Registrar"])
                                        # on_change=on_tab_change) # on_change em tabs não existe assim

        with tab_login:
            if st.session_state.get("show_login_after_register"):
                st.success("Registro realizado com sucesso! Por favor, faça o login.")
                del st.session_state.show_login_after_register 

            with st.form("login_form"):
                
                email_login = st.text_input("E-mail", key="login_email")
                senha_login = st.text_input("Senha", type="password", key="login_senha")
                enviar_login = st.form_submit_button("Entrar")
                
                if enviar_login:
                    autenticado, nome_usuario_ou_email = verificar_login(email_login, senha_login)
                    if autenticado:
                        st.session_state.autenticado = True
                        st.session_state.usuario = nome_usuario_ou_email 
                        st.session_state.active_tab = "Login" 
                        st.session_state.registration_errors = {}
                        st.session_state.registration_inputs = {"nome": "", "email": "", "senha": "", "conf_senha": ""}
                        keys_to_delete = [
                            'active_tab', 
                            'registration_errors', 
                            'registration_inputs', 
                            'show_login_after_register'
                        ]
                        for key in keys_to_delete:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.rerun()
                    else:
                        st.error("E-mail ou senha incorretos. As runas não reconhecem esta combinação.")
        
        with tab_registro:
            st.subheader("Inscreva-se no Mentorium")
            
            
            nome_completo_reg = st.text_input("Nome Completo", 
                                            value=st.session_state.registration_inputs["nome"], 
                                            key="reg_nome")
            if "nome" in st.session_state.registration_errors:
                st.error(st.session_state.registration_errors["nome"])

            email_reg = st.text_input("E-mail de Invocação", 
                                    value=st.session_state.registration_inputs["email"], 
                                    key="reg_email",
                                    help=f"Domínios permitidos: {', '.join(ALLOWED_DOMAINS)}")
            if "email" in st.session_state.registration_errors:
                st.error(st.session_state.registration_errors["email"])

            senha_reg = st.text_input("Senha Arcana", type="password", 
                                    value=st.session_state.registration_inputs["senha"], 
                                    key="reg_senha",
                                    help=f"Mínimo {MIN_PASSWORD_LENGTH} caracteres.")
            if "senha" in st.session_state.registration_errors:
                st.error(st.session_state.registration_errors["senha"])

            confirmar_senha_reg = st.text_input("Confirmar Senha Arcana", type="password", 
                                                value=st.session_state.registration_inputs["conf_senha"],
                                                key="reg_conf_senha")
            if "conf_senha" in st.session_state.registration_errors:
                st.error(st.session_state.registration_errors["conf_senha"])

            
            st.session_state.registration_inputs["nome"] = nome_completo_reg
            st.session_state.registration_inputs["email"] = email_reg
            st.session_state.registration_inputs["senha"] = senha_reg
            st.session_state.registration_inputs["conf_senha"] = confirmar_senha_reg

            if st.button("Concluir Cadastro", key="btn_concluir_cadastro"):
                st.session_state.registration_errors = {} 

                
                if not nome_completo_reg.strip():
                    st.session_state.registration_errors["nome"] = "Até mesmo os magos precisam de um nome... Informe como deseja ser chamado em nossos grimórios."
                
                email_valido, msg_email = is_valid_email_format(email_reg)
                if not email_valido:
                    st.session_state.registration_errors["email"] = msg_email
                
                senha_valida, msg_senha = is_strong_password(senha_reg) 
                if not senha_valida:
                    st.session_state.registration_errors["senha"] = msg_senha
                elif senha_reg.strip() != confirmar_senha_reg.strip(): 
                     st.session_state.registration_errors["conf_senha"] = "As senhas não se alinham como as constelações."
                
                
                if not nome_completo_reg.strip() and not email_reg.strip() and not senha_reg: 

                    if not st.session_state.registration_errors.get("nome"):
                         st.session_state.registration_errors["nome"] = "O nome completo é necessário."
                    if not st.session_state.registration_errors.get("email"):
                         st.session_state.registration_errors["email"] = "O e-mail é necessário."
                    if not st.session_state.registration_errors.get("senha"):
                         st.session_state.registration_errors["senha"] = "A senha é necessária."


                if not st.session_state.registration_errors:
                    
                    with st.spinner("O Conselho está inscrevendo teu nome nos registros sagrados..."):
                        
                        time.sleep(1)
                        
                        
                        status_code, message = registrar_usuario(nome_completo_reg, email_reg, senha_reg)
                    
                    if status_code == "success":
                        st.success(message) 
                        time.sleep(2)
                        st.session_state.show_login_after_register = True
                        st.session_state.active_tab = "Login" 
                        st.session_state.registration_inputs = {"nome": "", "email": "", "senha": "", "conf_senha": ""} # Limpar form
                        st.session_state.registration_errors = {}
                        st.rerun()
                    elif status_code == "email_exists": 
                        st.error(message)
                        
                    elif status_code == "save_error": 
                        st.error(message) 
                        
                    else: 
                        st.error(f"Um contratempo mágico ocorreu: {message}")
                else:
                    st.rerun()
        
            st.stop()