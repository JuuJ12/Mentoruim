import pyrebase 

firebaseConfig = {
    'apiKey': "AIzaSyBk1drWLWXFgotq4-BJLyAYSNiPEcSC9TQ",
    'authDomain': "mentorium-41748.firebaseapp.com",
    'projectId': "mentorium-41748",
    'storageBucket': "mentorium-41748.firebasestorage.app",
    'databaseURL': "https://mentorium-41748-default-rtdb.firebaseio.com",
    'messagingSenderId': "688533356703",
    'appId': "1:688533356703:web:1331886027db349ba8e2aa",
    'measurementId': "G-5W8GZCZVD1"
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