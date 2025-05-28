import streamlit as st

if "pagina" not in st.session_state or st.session_state.pagina != "principal":
    st.switch_page("paginas/tela_login_e_cadastro.py")

from Agents.conselho_dos_magos import chat
from Agents.conselho_dos_magos import respostass

st.title('Alto Conselho do Mentorium')
st.write('''
    O Alto Conselho do Mentorium é um grupo de mentores experientes e sábios que se reúnem para discutir e orientar os usuários em suas jornadas de aprendizado e desenvolvimento. Eles são os guardiões do conhecimento e da sabedoria, e estão sempre prontos para ajudar aqueles que buscam crescer e evoluir.
         
''')


defaults = {
    'assunto': '',
    'respostas_agentes': []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
st.session_state.assunto = st.text_input('Assunto',  help='Escreva o que você deseja, uma duvida, um problema, qualquer coisa !',value=st.session_state.assunto)
button = st.button('Iniciar Conversa')

if button:
    # Resetar respostas antigas
    st.session_state.respostas_agentes = []


    with st.spinner('Aguarde um momento, os agentes estão batendo um papo 🗣...'):
        for resultado in chat(st.session_state.assunto):
            with st.chat_message('🧙‍♂️'):
                st.write(resultado)

if 'respostas_agentes' in st.session_state and st.session_state.respostas_agentes:
    st.subheader("💬 Respostas anteriores dos agentes:")
    for resposta in st.session_state.respostas_agentes:
        st.write(f"**{resposta['nome']}** (modelo: {resposta['modelo']})")
        st.write(f"🗣 Resposta: {resposta['resposta']}")
        st.markdown("---")

# st.write(respostass(st.session_state.assunto))