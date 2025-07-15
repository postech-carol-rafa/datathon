import streamlit as st
st.set_page_config(layout="wide")

# Definindo as páginas diretamente
home = st.Page(
    'paginas/home.py',
    title="Home",
    icon='🏠',
    default=True
)

storytelling = st.Page(
    'paginas/recrutamento.py',
    title="Recrutamento",
    icon='🧑‍💼',
    default=False
)

dashboard = st.Page(
    'paginas/dashboard.py',
    title="Dashboard",
    icon='📊',
    default=False
)

predicao = st.Page(
    'paginas/predicao.py',
    title="KPI",
    icon='📈',
    default=False
)

dados = st.Page(
    'paginas/dados.py',
    title="Documentação",
    icon='📘',
    default=False
)

# Criando a navegação com st.navigation
pg = st.navigation(
    {
        "Selecione uma Opção": [home, storytelling, dashboard, predicao, dados],
    }
)

st.logo("imagens/logo1.png", size= "large") 


# Iniciar navegação
pg.run()