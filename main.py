import streamlit as st


st.set_page_config(
    page_title='Mentorium',
    layout="centered",
    initial_sidebar_state="expanded",
       
)

st.sidebar.text('Mentorium')


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


pag2=st.Page(
    page= "paginas/page_2.py",
    title="Alto Conselho do Mentorium",
    icon= '🧙‍♂️'
)

paginas = st.navigation({
    "Login e Registro": [logins_registro],
    "Jornada": [pag1],
    "Àgora": [pag2],
})

paginas= st.navigation({
        "Jornada":[pag1],
        "Àgora":[pag2],

    }
)

paginas.run()

