import streamlit as st


st.set_page_config(
    page_title='Mentorium',
    layout="centered",
    initial_sidebar_state="expanded",
       
)

st.sidebar.text('Mentorium')


pag1 = st.Page(
    page= "paginas/page_1.py",
    title="Iniciando a Jornada",
    icon='🧙‍♂️',
    default= True
)


pag2=st.Page(
    page= "paginas/page_2.py",
    title="Alto Conselho do Mentorium",
    icon= '🧙‍♂️'
)


paginas= st.navigation({
        "Jornada":[pag1],
        "Àgora":[pag2],

    }
)

paginas.run()

