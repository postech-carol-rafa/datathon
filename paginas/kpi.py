# Importando bibiotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Carregando DF
df_prospects_filtrado = pd.read_csv('data\df_prospects_filtrado.csv')
df_vagas_filtrado = pd.read_csv('data\df_vagas_filtrado.csv')

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

prioridade = {
   'alta: 3 a 5 dias': 'Alta',
   'média: 6 a 10 dias': 'Média',
   'baixa: 11 a 30 dias': 'Baixa',
   'nao informado': 'Não Informado'
}

# Incluindo colunas Data
df_vagas_filtrado['informacoes_basicas_data_requicisao'] = pd.to_datetime(df_vagas_filtrado['informacoes_basicas_data_requicisao'], format="%Y-%m-%d")
df_vagas_filtrado['informacoes_basicas_ano_requicisao'] = df_vagas_filtrado['informacoes_basicas_data_requicisao'].dt.year
df_vagas_filtrado['informacoes_basicas_mes_requicisao'] = df_vagas_filtrado['informacoes_basicas_data_requicisao'].dt.month
df_vagas_filtrado['informacoes_basicas_mes_nome_requicisao'] = df_vagas_filtrado['informacoes_basicas_mes_requicisao'].map(meses_nome)


df_vagas_filtrado['informacoes_basicas_ano_mes_nome_requicisao'] = (
    df_vagas_filtrado['informacoes_basicas_mes_nome_requicisao'] + '/' +
    df_vagas_filtrado['informacoes_basicas_ano_requicisao'].astype(str)
)

df_vagas_filtrado['data'] = pd.to_datetime(
    df_vagas_filtrado['informacoes_basicas_ano_requicisao'].astype(str) + '-' +
    df_vagas_filtrado['informacoes_basicas_mes_requicisao'].astype(str).str.zfill(2) + '-01',
    format='%Y-%m-%d'
)


df_vagas_filtrado['informacoes_basicas_trimestre_requicisao'] = df_vagas_filtrado['informacoes_basicas_mes_requicisao'].apply(
    lambda x: (
        '1º Trimestre' if 1 <= x <= 3 else
        '2º Trimestre' if 4 <= x <= 6 else
        '3º Trimestre' if 7 <= x <= 9 else
        '4º Trimestre'
    )
)

df_prospects_filtrado['ultima_atualizacao'] = pd.to_datetime(df_prospects_filtrado['ultima_atualizacao'], format="%Y-%m-%d")
df_prospects_filtrado['ultima_atualizacao_ano'] = df_prospects_filtrado['ultima_atualizacao'].dt.year
df_prospects_filtrado['ultima_atualizacao_mes'] = df_prospects_filtrado['ultima_atualizacao'].dt.month

df_prospects_filtrado['ultima_atualizacao_trimestre'] = df_prospects_filtrado['ultima_atualizacao_mes'].apply(
    lambda x: (
        '1º Trimestre' if 1 <= x <= 3 else
        '2º Trimestre' if 4 <= x <= 6 else
        '3º Trimestre' if 7 <= x <= 9 else
        '4º Trimestre'
    )
)

# Mapeando colunas
df_vagas_filtrado['informacoes_basicas_empresa_divisao'] = df_vagas_filtrado['informacoes_basicas_empresa_divisao'].map(divisao)

df_vagas_filtrado['informacoes_basicas_prioridade_vaga'] = df_vagas_filtrado['informacoes_basicas_prioridade_vaga'].map(prioridade)

# Variáveis
recrutadores_prospects = df_prospects_filtrado.recrutador.unique()
recrutadores = list(set(recrutadores_prospects))
recrutadores.sort()

ano_valores = np.sort(df_vagas_filtrado['informacoes_basicas_ano_requicisao'].unique())[::-1].tolist() 

#dataset merge
df_prospects_filtrado = pd.merge(df_prospects_filtrado, df_vagas_filtrado[[
    'id_vaga', 
    'informacoes_basicas_cliente', 
    'informacoes_basicas_data_requicisao', 
    'informacoes_basicas_ano_requicisao', 
    'informacoes_basicas_prioridade_vaga', 
    'perfil_vaga_areas_atuacao', 
    'informacoes_basicas_titulo_vaga_resumido', 
    'informacoes_basicas_empresa_divisao', 
    'informacoes_basicas_trimestre_requicisao', 
    'perfil_vaga_nivel_profissional'
    ]], on='id_vaga', how='left')

df_prospects_filtrado['dias_requisicao_ultima_atualizacao'] = (df_prospects_filtrado['ultima_atualizacao'] - df_prospects_filtrado['informacoes_basicas_data_requicisao']).dt.days

# CORPO DA PÁGINA


## Filtros da página
col11, col12, col13, col14 = st.columns([2,1,1,1])

with col11:
    recrutador = st.selectbox("Selecione o recrutador:", recrutadores)

with col12:
    unidade = st.selectbox('Selecione a unidade', ['Todas', 'Campinas', 'São Paulo'])

with col13:
    ano = st.selectbox('Selecione o ano', ano_valores)

with col14:
    trimestre = st.selectbox('Selecione o trimestre', ['1º Trimestre', '2º Trimestre', '3º Trimestre', '4º Trimestre'])


## Dataset filtrado
df_prospect_filtro = df_prospects_filtrado[df_prospects_filtrado['recrutador'] == recrutador]



## Intervalo de datas com base nos dados do recrutador selecionado
min_data_media = df_prospect_filtro['ultima_atualizacao'].min()
max_data_media = df_prospect_filtro['ultima_atualizacao'].max()

## Calculamos a média dos recrutadores no período do filtro
df_filtrado_geral = df_prospects_filtrado[
    (df_prospects_filtrado['situacao_candidado'] == 'Encaminhado ao Requisitante') & 
    (df_prospects_filtrado['ultima_atualizacao'] >= min_data_media) & 
    (df_prospects_filtrado['ultima_atualizacao'] <= max_data_media)
]

df_counts = df_filtrado_geral.groupby(
    ['recrutador', 'ultima_atualizacao_ano', 'ultima_atualizacao_trimestre']
).size().reset_index(name='quantidade')

df_media_periodo = df_counts.groupby(
    ['ultima_atualizacao_ano', 'ultima_atualizacao_trimestre']
)['quantidade'].mean().reset_index(name='media_recrutadores')

media_geral = df_media_periodo['media_recrutadores'].mean()


df_media_periodo['periodo'] = df_media_periodo.apply(
    lambda row: f"{row['ultima_atualizacao_trimestre'].replace('º Trimestre', 'º Tri')}/{int(row['ultima_atualizacao_ano'])}",
    axis=1
)


df_recrut_enc_req = df_prospect_filtro[
    df_prospect_filtro['situacao_candidado'] == 'Encaminhado ao Requisitante'
].groupby(['ultima_atualizacao_ano', 'ultima_atualizacao_trimestre']).size().reset_index(name='quantidade')


if df_recrut_enc_req.shape[0] == 0:     
        st.warning('Sem dados disponíveis de Encaminhado ao Requisitante')
else: 


    df_recrut_enc_req['periodo'] = df_recrut_enc_req.apply(
        lambda row: f"{row['ultima_atualizacao_trimestre'].replace('º Trimestre', 'º Tri')}/{int(row['ultima_atualizacao_ano'])}",
        axis=1
    )

    ## Gráfico Encaminhados ao Requisitante por Trimestre
    fig = px.bar(
        df_recrut_enc_req,
        x='periodo',
        y='quantidade',
        text='quantidade',
        title='Encaminhados ao Requisitante por Trimestre',
        labels={'quantidade': 'Quantidade de Candidatos', 'periodo': 'Período'}
    )

    fig.update_traces(textposition='auto', textfont_size=16, hovertemplate='Período: %{x}<br><b>Quantidade: %{y} </b><extra></extra>')
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        yaxis=dict(showticklabels=False, showgrid=False),
        showlegend=False,
        height=300
    )

    fig.add_hline(
        y=media_geral,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média Geral: {media_geral:.1f}",
        annotation_position="top left",
        annotation_font_size=14
    )

    st.plotly_chart(fig, use_container_width=True)


    ## Filtramos os dados para o gráfico de Tempo médio até o recrutador realizar o encaminhamento ao cliente dos cv

    df_filtrado_geral = df_prospects_filtrado[
        (df_prospects_filtrado['situacao_candidado'] == 'Encaminhado ao Requisitante') & 
        (df_prospects_filtrado['ultima_atualizacao'] >= min_data_media) & 
        (df_prospects_filtrado['ultima_atualizacao'] <= max_data_media)
    ]

    df_dias_geral = df_filtrado_geral.groupby(
        ['recrutador', 'ultima_atualizacao_ano', 'ultima_atualizacao_trimestre']
    )['dias_requisicao_ultima_atualizacao'].mean().reset_index(name='media_recrutador')

    df_media_dias_periodo = df_dias_geral.groupby(
        ['ultima_atualizacao_ano', 'ultima_atualizacao_trimestre']
    )['media_recrutador'].mean().reset_index(name='media_recrutadores')

    media_geral_dias = df_media_dias_periodo['media_recrutadores'].mean()

    df_media_dias_periodo['periodo'] = df_media_dias_periodo.apply(
        lambda row: f"{row['ultima_atualizacao_trimestre'].replace('º Trimestre', 'º Tri')}/{int(row['ultima_atualizacao_ano'])}",
        axis=1
    )

    df_recrut_dias = df_prospect_filtro[
        df_prospect_filtro['situacao_candidado'] == 'Encaminhado ao Requisitante'
    ].groupby(['ultima_atualizacao_ano', 'ultima_atualizacao_trimestre'])[
        'dias_requisicao_ultima_atualizacao'
    ].mean().reset_index(name='media_recrutador')

    df_recrut_dias['periodo'] = df_recrut_dias.apply(
        lambda row: f"{row['ultima_atualizacao_trimestre'].replace('º Trimestre', 'º Tri')}/{int(row['ultima_atualizacao_ano'])}",
        axis=1
    )

    # Gráfico de linha do tempo referente ao tempo médio
    fig = px.line(
        df_recrut_dias,
        x='periodo',
        y='media_recrutador',
        markers=True,
        title='Tempo Médio entre Requisição e Última Atualização (Dias)',
        labels={'media_recrutador': 'Média (dias)', 'periodo': 'Período'},
        
    )

    fig.update_traces(line=dict(color='blue', width=3), marker=dict(size=8), hovertemplate='Período: %{x}<br><b> Média: %{y:.1f} dias </b><extra></extra>')
    fig.update_layout(
        height=300,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )


    fig.add_hline(
        y=media_geral_dias,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média Geral: {media_geral_dias:.1f} dias",
        annotation_position="top left",
        annotation_font_size=14
    )

    st.plotly_chart(fig, use_container_width=True)


    ## Agrupando quantidade de clientes por recrutador
    df_cliente_recrutador = df_prospect_filtro.groupby('informacoes_basicas_cliente').size().reset_index(name='quantidade')

    df_cliente_recrutador = df_cliente_recrutador.sort_values('quantidade', ascending=False)


    ## Gráfico de clientes
    fig = px.bar(
        df_cliente_recrutador.head(10),
        x='quantidade',
        y='informacoes_basicas_cliente',
        color='informacoes_basicas_cliente',
        orientation='h',
        text='quantidade',
        labels={'quantidade': 'Quantidade', 'informacoes_basicas_cliente': 'Cliente'},
        title='Top 10 Clientes por Recrutador'
    )

    fig.update_traces(
        textposition='outside',
        hovertemplate='Cliente: %{y}<br><b> Quantidade: %{x} </b><extra></extra>'
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        height=500,
        showlegend=False,
        xaxis=dict(showticklabels=False)
    )

    st.plotly_chart(fig, use_container_width=True)


# Cards com a quantidade de situação de vagas por recrutador
card_nome_cliente = df_prospect_filtro.situacao_candidado.value_counts().keys().tolist()
card_valores_cliente = df_prospect_filtro.situacao_candidado.value_counts().values.tolist()
qtde_card_clientes = len(card_nome_cliente)
cols = st.columns(qtde_card_clientes)
cards_por_linha = 8
for i in range(0, qtde_card_clientes, cards_por_linha):
    cols = st.columns(cards_por_linha)
    for j in range(cards_por_linha):
        if i + j < qtde_card_clientes:
            with cols[j]:
                card_html = f"""
                <div style="
                    background-color: #1f77b4;
                    padding: 2px 2px;
                    border-radius: 6px;
                    color: white;
                    text-align: center;
                    max-width: 150px;
                    margin: 10px auto;
                    min-height: 80px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="font-size: 12px; margin-bottom: 2px;">{card_nome_cliente[i + j]}</div>
                    <div style="font-size: 36px; font-weight: bold; line-height: 1;">{card_valores_cliente[i + j]}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

