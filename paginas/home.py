# Importando bibiotecas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import timedelta


# Carregando Dataframe

df_vagas_filtrado = pd.read_csv("data/df_vagas_filtrado.csv")
df_vagas_filtrado['informacoes_basicas_data_requicisao'] = pd.to_datetime(df_vagas_filtrado['informacoes_basicas_data_requicisao'], format="%Y-%m-%d")
df_vagas_filtrado['informacoes_basicas_ano_requicisao'] = df_vagas_filtrado['informacoes_basicas_data_requicisao'].dt.year
df_vagas_filtrado['informacoes_basicas_mes_requicisao'] = df_vagas_filtrado['informacoes_basicas_data_requicisao'].dt.month


df_prospects_filtrado = pd.read_csv("data/df_prospects_filtrado.csv")
df_prospects_filtrado['ultima_atualizacao'] = pd.to_datetime(df_prospects_filtrado['ultima_atualizacao'], format="%Y-%m-%d")
df_prospects_filtrado['ultima_atualizacao_ano'] = df_prospects_filtrado['ultima_atualizacao'].dt.year
df_prospects_filtrado['ultima_atualizacao_mes'] = df_prospects_filtrado['ultima_atualizacao'].dt.month



# Dicionários
meses_nome = {
    1: 'Jan',
    2: 'Fev',
    3: 'Mar',
    4: 'Abr',
    5: 'Mai',
    6: 'Jun',
    7: 'Jul',
    8: 'Ago',
    9: 'Set',
    10: 'Out',
    11: 'Nov',
    12: 'Dez'
}

divisao = {
   'Decision Campinas': 'Campinas',
   'Decision São Paulo': 'São Paulo'
}


# Dataframe Resumidos
meses_filtro = (df_vagas_filtrado['informacoes_basicas_data_requicisao'].max() - timedelta(days=12*30)).replace(day=1)

df_agrupado_meses = df_vagas_filtrado[
    df_vagas_filtrado['informacoes_basicas_data_requicisao'] >= meses_filtro
].groupby(
    ['informacoes_basicas_ano_requicisao', 'informacoes_basicas_mes_requicisao','informacoes_basicas_empresa_divisao', 'informacoes_basicas_cliente']
).size().reset_index(name='quantidade')

df_agrupado_meses['informacoes_basicas_mes_nome_requicisao'] = df_agrupado_meses['informacoes_basicas_mes_requicisao'].map(meses_nome)
df_agrupado_meses['informacoes_basicas_empresa_divisao'] = df_agrupado_meses['informacoes_basicas_empresa_divisao'].map(divisao  )


df_agrupado_meses['informacoes_basicas_ano_mes_nome_requicisao'] = (
    df_agrupado_meses['informacoes_basicas_mes_nome_requicisao'] + '/' + 
    df_agrupado_meses['informacoes_basicas_ano_requicisao'].astype(str)
)

df_agrupado_meses['data'] = pd.to_datetime(
    df_agrupado_meses['informacoes_basicas_ano_requicisao'].astype(str) + '-' +
    df_agrupado_meses['informacoes_basicas_mes_requicisao'].astype(str).str.zfill(2) + '-01',
    format='%Y-%m-%d'
)



df_prospect_agrupado = df_prospects_filtrado[df_prospects_filtrado['ultima_atualizacao'] >= meses_filtro].groupby('situacao_candidado').size().reset_index(name='quantidade')


# Corpo da página


col1, col2 = st.columns([8,2])

with col1:
    st.markdown('#### **PAINEL PRINCIPAL -** *últimos 12 meses* 🧑‍💻')

with col2:
    st.image("imagens/logo2.png", width=120)
    

st.write("")

    
situacao_candidato_selecionados = ['Contratado como Hunting', 'Contratado pela Decision', 'Desistiu', 'Encaminhado ao Requisitante', 'Não Aprovado pelo Cliente', 'Sem interesse nesta vaga']

df_prospects_filtrados = df_prospect_agrupado[df_prospect_agrupado['situacao_candidado'].isin(situacao_candidato_selecionados)]


# Cards
titulos = df_prospects_filtrados['situacao_candidado'].tolist()
valores = df_prospects_filtrados['quantidade'].tolist()

cols = st.columns(6)

for i, col in enumerate(cols):
    card_html = f"""
    <div style="
        background-color: #1f77b4;
        padding: 2px 2px;
        border-radius: 6px;
        color: white;
        text-align: center;
        max-width: 150px;
        margin: 0 auto;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <div style="font-size: 12px; margin-bottom: 2px;">{titulos[i]}</div>
        <div style="font-size: 36px; font-weight: bold; line-height: 1;">{valores[i]}</div>
    </div>
    """
    col.markdown(card_html, unsafe_allow_html=True)

col1, col2 = st.columns([5,2])

with col1:
   df_fig1 = df_agrupado_meses.groupby(['data','informacoes_basicas_ano_mes_nome_requicisao'])['quantidade'].sum().reset_index(name='quantidade')
   fig1 = px.bar(
      df_fig1,
      x='informacoes_basicas_ano_mes_nome_requicisao',
      y='quantidade',
      title='Quantidade de Vagas Disponibilizadas',
      text='quantidade', 
      color_discrete_sequence=['#1f77b4']
   )

   fig1.update_traces(
      textfont=dict(
         size=13,    ),
         hoverinfo='skip',          
      hovertemplate=None 
   )

   fig1.update_layout(
      xaxis_title=None, 
      yaxis_title=None,
      uniformtext_minsize=10,
      yaxis=dict(
         showticklabels=False,
         showgrid=False
      ),
      
      
   )

   st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
 
 
 

with col2:
   total = df_agrupado_meses['quantidade'].sum()

   fig2 = px.pie(
         df_agrupado_meses,
         names='informacoes_basicas_empresa_divisao',
         values='quantidade',
         color_discrete_sequence=['#1f77b4', '#3c8dbc'],
         title='Vagas por Divisão'
      )
   
   fig2.update_layout(
      showlegend=False, 
      annotations=[dict(
        text=f'{total}',          
        x=0.5, 
        y=0.5,             
        font_size=20,
        showarrow=False
        )]
      )


   fig2.update_traces(textinfo='percent+value+label', hole=0.4, textposition='outside')  # hole=0.4 para Rosca

   st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
 


top_clientes = (
    df_agrupado_meses
    .groupby('informacoes_basicas_cliente')['quantidade']
    .sum()
    .nlargest(5)
    .index
)

df_top5 = df_agrupado_meses[df_agrupado_meses['informacoes_basicas_cliente'].isin(top_clientes)]

fig = px.line(
    df_top5.sort_values('data'),
    x='informacoes_basicas_ano_mes_nome_requicisao',
    y='quantidade',
    color='informacoes_basicas_cliente',
    markers=True,
    title='Evolução de Requisições de vagas dos 5 principais clientes'
)

fig.update_traces(meta=df_top5['informacoes_basicas_cliente'])

fig.update_layout(
    xaxis_title='',  
    yaxis_title='',  
    legend_title='Clientes',
    legend=dict(
        orientation='h',   
        y=-0.2,          
        x=0,
        xanchor='left',
        yanchor='top',
    )
)

fig.update_traces(
    hovertemplate=(
        'Cliente: <b>%{meta}</b><br>' +  
        'Quantidade: <b>%{y}</b><extra></extra>'
    )
)

fig.update_xaxes(
    dtick="M1",    
)

st.plotly_chart(fig, use_container_width=True)


 

# cores_azuis = ['#1f77b4', '#3c8dbc'] '#6baed6']


 
