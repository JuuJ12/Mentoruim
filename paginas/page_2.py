import streamlit as st
from PIL import Image

# if "pagina" not in st.session_state or st.session_state.pagina != "principal":
#     st.switch_page("paginas/tela_login_e_cadastro.py")

from Agents.conselho_dos_magos import chat
from Agents.conselho_dos_magos import respostass

# Configurar imagem de fundo
image_url = "https://i.postimg.cc/jq1JFnR0/Gemini-Generated-Image-a19k06a19k06a19k.png"

page_bg_img = f"""
<style>
p {{
    color: #FFFFFF !important;
}}
.stApp {{
    background-image: url("{image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #FFFFFF;
}}
/* Aplicar cores brancas apenas ao conteúdo principal */
.main h1 {{
    color: #FFFFFF !important;
}}
.main h2 {{
    color: #FFFFFF !important;
}}
.main h3 {{
    color: #FFFFFF !important;
}}
.main .stMarkdown {{
    color: #FFFFFF !important;
}}
/* Texto em geral apenas na área principal */
.main p, .main div, .main span, .main .stWrite {{
    color: #FFFFFF !important;
}}
/* Label do campo de texto */
.main .stTextInput > label {{
    color: #FFFFFF !important;
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
    color: #000000;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title('Alto Conselho do Mentorium')
st.write('''
    O Alto Conselho do Mentorium é um grupo de mentores experientes e sábios que se reúnem para discutir e orientar os usuários em suas jornadas de aprendizado e desenvolvimento. Eles são os guardiões do conhecimento e da sabedoria, e estão sempre prontos para ajudar aqueles que buscam crescer e evoluir.
         
''')


defaults = {
    'assunto': '',
    'respostas_agentes': [],
    'respostas_mago1': [],
    'respostas_mago2': [],
    'respostas_mago3': []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
st.session_state.assunto = st.text_input('Assunto',  help='Escreva o que você deseja, uma duvida, um problema, qualquer coisa !',value=st.session_state.assunto)
button = st.button('Iniciar Conversa')

if button:
    # Resetar respostas antigas
    st.session_state.respostas_agentes = []
    st.session_state.respostas_mago1 = []
    st.session_state.respostas_mago2 = []
    st.session_state.respostas_mago3 = []

    # Carregar as imagens dos magos
    try:
        img_mago1 = Image.open("pictures/mago4.png")
        img_mago2 = Image.open("pictures/mago2.png")
        img_mago3 = Image.open("pictures/mago3.png")
    except FileNotFoundError:
        st.error("Imagens dos magos não encontradas!")
        img_mago1 = img_mago2 = img_mago3 = None

    # Criar 3 colunas para os magos
    col1, col2, col3 = st.columns(3)
    
    # Configurar as colunas com imagens e títulos
    with col1:
        st.subheader("🔮 Feiticeiro")
        if img_mago1:
            st.image(img_mago1, width=150)
        placeholder_mago1 = st.empty()
        
    with col2:
        st.subheader("📚 Wizard")
        if img_mago2:
            st.image(img_mago2, width=150)
        placeholder_mago2 = st.empty()
        
    with col3:
        st.subheader("🌙 Bruxo")
        if img_mago3:
            st.image(img_mago3, width=150)
        placeholder_mago3 = st.empty()

    with st.spinner('Aguarde um momento, os agentes estão batendo um papo 🗣...'):
        for resultado in chat(st.session_state.assunto):
            # Determinar qual mago está falando baseado no nome
            if "Feiticeiro" in resultado:
                st.session_state.respostas_mago1.append(resultado)
                with placeholder_mago1:
                    st.markdown("**Respostas:**")
                    for resposta in st.session_state.respostas_mago1:
                        st.write(resposta)
            elif "Wizard" in resultado:
                st.session_state.respostas_mago2.append(resultado)
                with placeholder_mago2:
                    st.markdown("**Respostas:**")
                    for resposta in st.session_state.respostas_mago2:
                        st.write(resposta)
            elif "Bruxo" in resultado:
                st.session_state.respostas_mago3.append(resultado)
                with placeholder_mago3:
                    st.markdown("**Respostas:**")
                    for resposta in st.session_state.respostas_mago3:
                        st.write(resposta)

# Exibir respostas anteriores se existirem
if ('respostas_mago1' in st.session_state and st.session_state.respostas_mago1) or \
   ('respostas_mago2' in st.session_state and st.session_state.respostas_mago2) or \
   ('respostas_mago3' in st.session_state and st.session_state.respostas_mago3):
    
    st.subheader("💬 Última conversa dos magos:")
    
    # Criar 3 colunas para exibir as respostas anteriores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔮 Feiticeiro")
        try:
            img_mago1 = Image.open("pictures/mago4.png")
            st.image(img_mago1, width=150)
        except FileNotFoundError:
            pass
        if 'respostas_mago1' in st.session_state:
            for resposta in st.session_state.respostas_mago1:
                st.write(resposta)
                
    with col2:
        st.subheader("📚 Wizard")
        try:
            img_mago2 = Image.open("pictures/mago2.png")
            st.image(img_mago2, width=150)
        except FileNotFoundError:
            pass
        if 'respostas_mago2' in st.session_state:
            for resposta in st.session_state.respostas_mago2:
                st.write(resposta)
                
    with col3:
        st.subheader("🌙 Bruxo")
        try:
            img_mago3 = Image.open("pictures/mago3.png")
            st.image(img_mago3, width=150)
        except FileNotFoundError:
            pass
        if 'respostas_mago3' in st.session_state:
            for resposta in st.session_state.respostas_mago3:
                st.write(resposta)

# st.write(respostass(st.session_state.assunto))