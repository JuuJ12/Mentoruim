import pyrebase 
import os
from dotenv import load_dotenv
load_dotenv()
firebaseConfig = {
    'apiKey': os.getenv("FIREBASE_API_KEY"),
    'authDomain': os.getenv("AUTH_DOMAIN"),
    'projectId': os.getenv("PROJECT_ID"),
    'storageBucket': os.getenv("STORAGE_BUCKET"),
    'databaseURL': os.getenv("DATABASE_URL"),
    'messagingSenderId': os.getenv("MESSAGING_SENDER_ID"),
    'appId': os.getenv("APP_ID"),
    'measurementId': os.getenv("MEASUREMENT_ID")
}

def cadastro(email: str, senha: str) -> tuple[bool, str]:
    """
    Cadastra um novo usuário no Firebase Authentication usando Pyrebase.
    Retorna True e uma mensagem de sucesso em caso de sucesso,
    ou False e uma mensagem de erro.
    """
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    try:
        auth.create_user_with_email_and_password(email, senha)
        return True, "Cadastro realizado com sucesso!"
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            return False, "Este e-mail já está em uso por outro feiticeiro."
        elif "WEAK_PASSWORD" in error_message:
            return False, "A senha é muito fraca. Escolha uma senha mais forte (mínimo 6 caracteres)."
        elif "INVALID_EMAIL" in error_message:
            return False, "Formato de e-mail inválido. Verifique o pergaminho."
        else:
            print(f"Erro inesperado ao cadastrar usuário: {e}")
            return False, f"Ocorreu um erro arcano ao tentar cadastrar: {error_message}"

def login(email: str, senha: str) -> tuple[bool, str | None]:
    """
    Tenta autenticar um usuário no Firebase usando Pyrebase.
    Retorna True e o email do usuário em caso de sucesso,
    ou False e None (ou uma mensagem de erro).
    """
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    try:
        user_info = auth.sign_in_with_email_and_password(email, senha)
        return True, email
    except Exception as e:
        error_message = str(e)
        if "INVALID_LOGIN_CREDENTIALS" in error_message or "EMAIL_NOT_FOUND" in error_message or "INVALID_PASSWORD" in error_message:
            return False, "E-mail ou senha incorretos. As runas não reconhecem esta combinação."
        else:
            print(f"Erro inesperado ao fazer login: {e}")
            return False, None


def recuperar_senha(email: str) -> tuple[bool, str]:
    """
    Envia um e-mail de recuperação de senha para o usuário.
    Retorna True e uma mensagem de sucesso em caso de sucesso,
    ou False e uma mensagem de erro.
    """
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    try:
        auth.send_password_reset_email(email)
        return True, "E-mail de recuperação enviado com sucesso!"
    except Exception as e:
        error_message = str(e)
        if "EMAIL_NOT_FOUND" in error_message:
            return False, "Este e-mail não está registrado no grimório."
        else:
            print(f"Erro inesperado ao enviar e-mail de recuperação: {e}")
            return False, f"Ocorreu um erro arcano ao tentar enviar o e-mail: {error_message}"