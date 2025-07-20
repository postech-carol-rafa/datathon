# Importando bibiotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Carregando DF
df_prospects_filtrado = pd.read_csv('data/df_prospects_filtrado.csv')
df_vagas_filtrado = pd.read_csv('data/df_vagas_filtrado.csv')

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

cores_prioridade = {
        'alta: 3 a 5 dias': '#d62728',     
        'média: 6 a 10 dias': '#ff7f0e',    
        'baixa: 11 a 30 dias': '#43a047',
        'nao informado': '#a9a9a9'
    }

prioridade = {
   'alta: 3 a 5 dias': 'Alta',
   'média: 6 a 10 dias': 'Média',
   'baixa: 11 a 30 dias': 'Baixa',
   'nao informado': 'Não Informado'
}

# Incluindo colunas Data

## Vagas_filtrado
df_vagas_filtrado['informacoes_basicas_data_requicisao'] = pd.to_datetime(
df_vagas_filtrado['informacoes_basicas_data_requicisao'], format="%Y-%m-%d")
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

## Prospects_filtrado
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


# Colunas Mapeadas
df_vagas_filtrado['informacoes_basicas_empresa_divisao'] = df_vagas_filtrado['informacoes_basicas_empresa_divisao'].map(divisao)
df_vagas_filtrado['informacoes_basicas_prioridade_vaga_resumido'] = df_vagas_filtrado['informacoes_basicas_prioridade_vaga'].map(prioridade)


# Variáveis
ano_valores = np.sort(df_vagas_filtrado['informacoes_basicas_ano_requicisao'].unique())[::-1].tolist()
clientes = df_vagas_filtrado.informacoes_basicas_cliente.unique().tolist()

# Merge e criação de coluna
df_prospects_filtrado = pd.merge(df_prospects_filtrado, df_vagas_filtrado[[
    'id_vaga', 
    'informacoes_basicas_cliente', 
    'informacoes_basicas_data_requicisao', 
    'informacoes_basicas_ano_requicisao', 
    'informacoes_basicas_prioridade_vaga',
    'informacoes_basicas_prioridade_vaga_resumido', 
    'perfil_vaga_areas_atuacao', 
    'informacoes_basicas_titulo_vaga_resumido', 
    'informacoes_basicas_empresa_divisao', 
    'informacoes_basicas_trimestre_requicisao', 
    'perfil_vaga_nivel_profissional'
    ]], on='id_vaga', how='left')

df_prospects_filtrado['dias_requisicao_ultima_atualizacao'] = (
    df_prospects_filtrado['ultima_atualizacao'] - df_prospects_filtrado['informacoes_basicas_data_requicisao']).dt.days


# CORPO DA PÁGINA

tab1, tab2 = st.tabs(["📈 Visão Geral", "🏢 Clientes"])

## Página de Visão Geral
with tab1:
    ### Filtros da página
    col1, col2, col3 = st.columns(3)
    with col1:
        unidade = st.selectbox('Selecione a unidade', ['Todas', 'Campinas', 'São Paulo'])
    with col2:
        ano = st.selectbox('Selecione o ano', ano_valores)
    with col3:
        trimestre = st.selectbox('Selecione o trimestre', ['1º Trimestre', '2º Trimestre', '3º Trimestre', '4º Trimestre'])
        
    if unidade.lower() == 'todas':
        df_vagas_filtro = df_vagas_filtrado[
            (df_vagas_filtrado['informacoes_basicas_ano_requicisao'] == ano) &
            (df_vagas_filtrado['informacoes_basicas_trimestre_requicisao'] == trimestre)
        ]
    else:
        df_vagas_filtro = df_vagas_filtrado[
            (df_vagas_filtrado['informacoes_basicas_empresa_divisao'] == unidade) &
            (df_vagas_filtrado['informacoes_basicas_ano_requicisao'] == ano) &
            (df_vagas_filtrado['informacoes_basicas_trimestre_requicisao'] == trimestre)
        ]

    if unidade.lower() == 'todas':
        df_prospect_filtro = df_prospects_filtrado[
            (df_prospects_filtrado['ultima_atualizacao_ano'] == ano) &
            (df_prospects_filtrado['ultima_atualizacao_trimestre'] == trimestre)
        ]
    else:
        df_prospect_filtro = df_prospects_filtrado[
            (df_prospects_filtrado['informacoes_basicas_empresa_divisao'] == unidade) &
            (df_prospects_filtrado['ultima_atualizacao_ano'] == ano) &
            (df_prospects_filtrado['ultima_atualizacao_trimestre'] == trimestre)
        ]

    ### Variáveis com os valores dos cards
    qtde_vagas = df_vagas_filtro.shape[0]
    qtde_contratado_decision = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Contratado pela Decision'].shape[0]
    qtde_contratado_hunting = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Contratado como Hunting'].shape[0]
    qtde_requisitante = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Encaminhado ao Requisitante'].shape[0]
    qtde_nao_aprovado_cliente = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Não Aprovado pelo Cliente'].shape[0]
    qtde_sem_interesse = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Sem interesse nesta vaga'].shape[0]
    qtde_nao_aprovado_req = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Não Aprovado pelo Requisitante'].shape[0]
    qtde_sem_int_vaga = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Sem interesse nesta vaga'].shape[0]
    qtde_nao_aprovado_rh = df_prospect_filtro[df_prospect_filtro['situacao_candidado'] == 'Não Aprovado pelo RH'].shape[0]

    ### Lista com nome dos cards
    titulos = ['Total de Vagas', 
               'Contratado pela Decision', 
               'Contratado como Hunting', 
               'Encaminhado ao Requisitante', 
               'Não Aprovado pelo Cliente', 
               'Sem interesse nesta vaga', 
               'Não Aprovado pelo Requisitante', 
               'Sem interesse nesta vaga', 
               'Não Aprovado pelo RH'
               ]
    ### Lista com os valores dos cards	
    valores	= [qtde_vagas, 
               qtde_contratado_decision, 
               qtde_contratado_hunting, 
               qtde_requisitante, 
               qtde_nao_aprovado_cliente, 
               qtde_sem_interesse, 
               qtde_nao_aprovado_req, 
               qtde_sem_int_vaga, 
               qtde_nao_aprovado_rh]
    
    ### Definindo o número de colunas para os cards    
    cols = st.columns(9)

    ### Laço de repetição para criar os cards com os valores e seus títulos usando as listas criadas
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
    
    ### Área com os gráficos de prioridade por cliente e Vagas por área
    col6, col7 = st.columns(2)

    with col6:
        #### Agrupamentos dos dados para o gráfico (sendo um com os dados somandos para ordenação e outro com os dados por prioridade da vaga)
        df_clientes_prioridade = df_vagas_filtro[df_vagas_filtro['informacoes_basicas_ano_requicisao'] == ano].groupby(
                ['informacoes_basicas_cliente', 'informacoes_basicas_prioridade_vaga']).size().reset_index(
                    name='quantidade').sort_values('quantidade', ascending=False)

        clientes_prioridade = df_vagas_filtro[df_vagas_filtrado['informacoes_basicas_ano_requicisao'] == ano].groupby(
                                            ['informacoes_basicas_cliente']).size().sort_values(ascending=False).index.tolist()[:10]
        
        #### Gráfico dos 10 clientes por prioridade
        fig = px.bar(
                df_clientes_prioridade[df_clientes_prioridade['informacoes_basicas_cliente'].isin(clientes_prioridade)],
                x='quantidade',
                y='informacoes_basicas_cliente',
                color='informacoes_basicas_prioridade_vaga',
                orientation='h',
                text='quantidade',
                title=f'Top 10 Clientes por Prioridade de Vaga em {ano}',
                labels={
                    'quantidade': 'Quantidade de Vagas',
                    'informacoes_basicas_cliente': 'Cliente',
                    'informacoes_basicas_prioridade_vaga': 'Prioridade'
                },
                hover_data={
                    'quantidade': True,
                    'informacoes_basicas_cliente': False, 
                    'informacoes_basicas_prioridade_vaga': True
                },
                color_discrete_map = cores_prioridade
            )
        fig.update_layout(
                barmode='stack',
                template='plotly_white',
                xaxis_title= None,
                yaxis_title= None,
                yaxis=dict(categoryorder='total ascending'), 
                legend_title='Prioridade',
                legend=dict(
                    orientation="h", 
                    yanchor="top",
                    y=-0.05,           
                    xanchor="center",
                    x=0.5
                ),
                 xaxis=dict(
                    showticklabels=False,  
                    ticks="",            
                    showgrid=False        
                )
            )
        fig.update_traces(
            hovertemplate='<span style="font-weight:normal;">Empresa: %{y}</span><br><b>Valor: %{x}</b><extra></extra>'
        )
        st.plotly_chart(fig, use_container_width=True) 
        
                


    with col7:
        #### Agrupamentos dos dados para o gráfico de vagas por área de atuação (usando as colunas binárias para extrair os valores)
        dummies_area_atuacao = df_vagas_filtro['perfil_vaga_areas_atuacao'].str.get_dummies(sep=' - ')
        dummies_area_atuacao.columns = dummies_area_atuacao.columns.str.rstrip('-')
        df_area_atuacao = dummies_area_atuacao.sum().reset_index()
        df_area_atuacao.columns = ['atuacao', 'quantidade']
        df_area_atuacao = df_area_atuacao.sort_values('quantidade', ascending=False).head(5)

        #### Gráfico Top 5 das áreas de atuação
        fig = px.bar(
            df_area_atuacao,
            x='atuacao',
            y='quantidade',
            text='quantidade',
            title='Top 5 Vagas por Área de Atuação',
            labels={'quantidade': 'Quantidade de Vagas', 'atuacao': 'Área de Atuação'}
        )
        fig.update_layout(
            xaxis_title=None,  
            yaxis_title=None, 
            xaxis=dict(tickfont=dict(size=12)),
            yaxis=dict(showticklabels=False, showgrid=False), 
            showlegend=False,
            height=500
        )
        fig.update_traces(
            textposition='auto',
            textfont_size=16,
            hovertemplate='<span style="font-weight:normal;">Área: %{x}</span><br><b>Valor: %{y}</b><extra></extra>'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    ### Área com os gráficos de evolução das vagas por prioridade  
    
    
    #### Agrupamento dos dados
    df_vagas_prioridade = df_vagas_filtro.groupby(
        ['informacoes_basicas_data_requicisao', 'informacoes_basicas_prioridade_vaga']).size().reset_index(
            name='quantidade').sort_values('informacoes_basicas_data_requicisao')
        
    
    #### Gráfico de evolução das vagas por prioridade
    fig = px.line(
            df_vagas_prioridade[['informacoes_basicas_data_requicisao', 'informacoes_basicas_prioridade_vaga','quantidade']].sort_values(
                'informacoes_basicas_data_requicisao'),
            x='informacoes_basicas_data_requicisao',
            y='quantidade',
            color='informacoes_basicas_prioridade_vaga',
            color_discrete_map=cores_prioridade,
            markers=False,
            title='Evolução das Vagas por Prioridade',
            labels={
                'informacoes_basicas_data_requicisao': 'Data de Requisição',
                'quantidade': 'Quantidade de Vagas',
                'informacoes_basicas_prioridade_vaga': 'Prioridade'
            }
        )
    fig.update_layout(
            height=400, 
            xaxis_title= None,
            yaxis_title='Quantidade',
            legend_title='Prioridade',
            hovermode='x unified',
            legend=dict(
                orientation='h',
                y=1.1,
                x=0,
                xanchor='left',
                yanchor='top',
            )
        )
    fig.update_xaxes(
            dtick="M1",
        )
    st.plotly_chart(fig, use_container_width=True)

## Página de Clientes
with tab2:
    
    ### Filtros da página
    col11, col12, col13, col14 = st.columns([2,1,1,1])
    with col11:
        cliente = st.selectbox("Selecione um cliente:", clientes)
    with col12:
        unidade2 = st.selectbox('Selecione a unidade', ['Todas', 'Campinas', 'São Paulo'],  key='unidade2')
    with col13:
        ano2 = st.selectbox('Selecione o ano', ano_valores, key='ano2')
    with col14:
        trimestre2 = st.selectbox('Selecione o trimestre', ['1º Trimestre', '2º Trimestre', '3º Trimestre', '4º Trimestre'], key='trimestre2')
    if unidade2.lower() == 'todas':
        df_prospect_filtro = df_prospects_filtrado[(df_prospects_filtrado['informacoes_basicas_cliente'] == cliente) &
                                            (df_prospects_filtrado['informacoes_basicas_ano_requicisao'] == ano2) &
                                            (df_prospects_filtrado['informacoes_basicas_trimestre_requicisao'] == trimestre2)
                                            ]
    else:
        df_prospect_filtro = df_prospects_filtrado[(df_prospects_filtrado['informacoes_basicas_cliente'] == cliente) &
                                            (df_prospects_filtrado['informacoes_basicas_empresa_divisao'] == unidade2) &
                                            (df_prospects_filtrado['informacoes_basicas_ano_requicisao'] == ano2) &
                                            (df_prospects_filtrado['informacoes_basicas_trimestre_requicisao'] == trimestre2)
                                            ]

    ### Caso não encontrar dados retorna que não há informações
    if df_prospect_filtro.shape[0] == 0:     
        st.warning('Sem dados disponíveis')
    else: 
        ### Filtrado dados em um novo dataset
        situacao_candidato_selecionados = ['Contratado como Hunting', 'Contratado pela Decision', 'Desistiu', 'Em avaliação pelo RH', 'Encaminhado ao Requisitante', 'Entrevista com Cliente', 'Não Aprovado pelo Cliente', 'Sem interesse nesta vaga']
        df_prospect_select = df_prospect_filtro[df_prospect_filtro['situacao_candidado'].isin(situacao_candidato_selecionados)]

        ### Separado os dados para o card (valores e títulos)
        df_valores_situacao = df_prospect_select['situacao_candidado'].value_counts()
        card_nome_cliente = df_valores_situacao.index.tolist()
        card_valores_cliente = df_valores_situacao.values.tolist()
        qtde_card_clientes = len(card_nome_cliente)
        cols = st.columns(qtde_card_clientes)
        
        ### Laço criando os card divido em colunas, agora a quantidade de coluna é condicional a quantidade de valores localizados
        for i, col in enumerate(cols):
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
                <div style="font-size: 12px; margin-bottom: 2px;">{card_nome_cliente[i]}</div>
                <div style="font-size: 36px; font-weight: bold; line-height: 1;">{card_valores_cliente[i]}</div>
            </div>
            """
            col.markdown(card_html, unsafe_allow_html=True)
 
        ###  Área com os gráficos vagas por nível e por área de atuação         
        col20, col21 = st.columns([2,2])
        
        #### Gráfico de nível profissional
        with col20: 
            df_area_nivel_prof_cliente = df_prospect_filtro.groupby('perfil_vaga_nivel_profissional').size().reset_index(name='quantidade')
            fig = px.bar(
                        df_area_nivel_prof_cliente,
                        x='quantidade',
                        y='perfil_vaga_nivel_profissional',
                        color='perfil_vaga_nivel_profissional',
                        orientation='h',
                        text='quantidade',
                        title=f'Vagas por Nível do Profissional',
                        labels={
                            'quantidade': 'Quantidade de Vagas',
                            'informacoes_basicas_cliente': 'Cliente',
                            'informacoes_basicas_prioridade_vaga_resumido': 'Prioridade'
                        },
                        hover_data={'quantidade': True, 'perfil_vaga_nivel_profissional': True}
                    )
            fig.update_layout(
                        height=300,
                        barmode='stack',
                        template='plotly_white',
                        xaxis_title= None,
                        yaxis_title= None,
                        yaxis=dict(categoryorder='total ascending'), 
                        showlegend=False
                    )
            fig.update_traces(
                      textfont_size=16,
                      textposition='auto',
                      hovertemplate='<span style="font-weight:normal;">%{label}</span><br><b>Valor: %{value}</b><extra></extra>'
                      ) 
            fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)

        #### Gráfico de vagas por área de atuação
        with col21: 
            df_area_atuacao_cliente = df_prospect_filtro.groupby('perfil_vaga_areas_atuacao').size().reset_index(name='quantidade')

            fig = px.bar(
                    df_area_atuacao_cliente,
                    x='perfil_vaga_areas_atuacao',
                    y='quantidade',
                    color='perfil_vaga_areas_atuacao',
                    text='quantidade',
                    title='Vagas por Área de Atuação',
                    labels={'quantidade': 'Quantidade de Vagas', 'atuacao': 'Área de Atuação'}
                )
            fig.update_layout(
                    xaxis_title=None,  
                    yaxis_title=None, 
                    xaxis=dict(
                        showticklabels=True,
                        tickangle=45,
                        tickfont=dict(size=11)
                    ),
                    yaxis=dict(showticklabels=False, showgrid=False), 
                    showlegend=False,
                    height=300                    
                )
            fig.update_traces(
                    textposition='auto',
                    textfont_size=16,
                    hovertemplate='<span style="font-weight:normal;">%{label}</span><br><b>Valor: %{value}</b><extra></extra>'     
                )
            st.plotly_chart(fig, use_container_width=True)


        #### Criamos pequenos df que verifica a primeira data que iniciou a movimentação da vaga no prospect e verificamos a média de dias que demorou para acionar o cliente em algumas situações das vagas
        df_pie_contratado = df_prospect_filtro[
                                (df_prospect_filtro['situacao_candidado'] == 'Contratado pela Decision') |
                                (df_prospect_filtro['situacao_candidado'] == 'Contratado como Hunting')
                            ].groupby('informacoes_basicas_prioridade_vaga_resumido')['dias_requisicao_ultima_atualizacao'].mean().round(0).reset_index()

        id_min_enc_req = df_prospect_filtro[
            (df_prospect_filtro['situacao_candidado'] == 'Encaminhado ao Requisitante')].groupby('id_vaga')['ultima_atualizacao'].idxmin()
        df_pie_enc_req = df_prospect_filtro.loc[id_min_enc_req].groupby('informacoes_basicas_prioridade_vaga_resumido')['dias_requisicao_ultima_atualizacao'].mean().round(0).reset_index()

        id_min_av_rh = df_prospect_filtro[
            (df_prospect_filtro['situacao_candidado'] == 'Em avaliação pelo RH')].groupby('id_vaga')['ultima_atualizacao'].idxmin()
        df_min_av_rh = df_prospect_filtro.loc[id_min_av_rh].groupby('informacoes_basicas_prioridade_vaga_resumido')['dias_requisicao_ultima_atualizacao'].mean().round(0).reset_index()

        id_min_ent_cli = df_prospect_filtro[
            (df_prospect_filtro['situacao_candidado'] == 'Entrevista com Cliente')].groupby('id_vaga')['ultima_atualizacao'].idxmin()
        df_min_ent_cli = df_prospect_filtro.loc[id_min_ent_cli].groupby('informacoes_basicas_prioridade_vaga_resumido')['dias_requisicao_ultima_atualizacao'].mean().round(0).reset_index()



        #### Lista com DataFrames e títulos
        graficos_info = [
            ("df_min_av_rh", df_pie_contratado, "Média de dias para Contratação"),
            ("df_pie_enc_req", df_pie_enc_req, "Média de dias Encaminhado ao Requisitante"),
            ("df_min_av_rh", df_min_av_rh, "Média de dias Avaliação RH"),
            ("df_min_ent_cli", df_min_ent_cli, "Média de dias Entrevista Cliente"),
        ]


        cols = st.columns(4)

        # Laço com os 4 gráfico de pizza
        for i, (df_nome, df, titulo) in enumerate(graficos_info):
            with cols[i]:
                if not df.empty:
                    fig = px.pie(
                        df,
                        names='informacoes_basicas_prioridade_vaga_resumido',
                        values='dias_requisicao_ultima_atualizacao',
                        hole=0.4,
                        title=titulo,
                        width=400, 
                        height=400
                    )
                    fig.update_traces(
                        texttemplate='%{label}: %{value} dias',
                        textinfo='text',
                        hovertemplate=
                            '<b>Prioridade:</b> %{label}<br>' +
                            '<b>Média de Dias:</b> %{value}<br>' +
                            '<b>Proporção:</b> %{percent}<extra></extra>'
                    )
                    fig.update_layout(showlegend=False, title_font_size=13)
                    st.plotly_chart(fig, use_container_width=True, key=f"grafico_pie_{i}")
                else:
                    st.markdown(
                            f"<div style='font-size:13px; font-weight:bold;'>&nbsp;</div>"
                            f"<div style='font-size:13px; font-weight:bold;'>&nbsp;</div>"
                            f"<div style='font-size:13px; font-weight:bold;'>{titulo}</div>"
                            f"<div style='font-size:12px; color:gray;'>Sem dados disponíveis.</div>",
                            unsafe_allow_html=True
        )

