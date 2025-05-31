import pyrebase 

firebaseConfig = {
  'apiKey': "AIzaSyBk1drWLWXFgotq4-BJLyAYSNiPEcSC9TQ",
  'authDomain': "mentorium-41748.firebaseapp.com",
  'projectId': "mentorium-41748",
  'storageBucket': "mentorium-41748.firebasestorage.app",
  'databaseURL': "https://mentorium-41748-default-rtdb.firebaseio.com",
  'messagingSenderId': "688533356703",
  'appId': "1:688533356703:web:1331886027db349ba8e2aa",
  'measurementId': "G-5W8GZCZVDT"
}

def cadastro(email : str, senha:int) -> bool:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    try:
        auth.create_user_with_email_and_password(email, senha)
        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False

def login(email: str, senha: int) -> bool:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    try:
        auth.sign_in_with_email_and_password(email, senha)
        return True
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return False
    
email = "testando@gmail.com"
senha = "123456"
