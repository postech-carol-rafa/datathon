# Importando bibiotecas
import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.sparse import hstack, csr_matrix
import joblib
import re
import unicodedata
import string
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')

# Stop Words
stop_pt = pd.read_csv('data/stop_words_portugues_spacy.csv')
stop_words_portugues_spacy = stop_pt['stop_word'].tolist()

stop_en = pd.read_csv('data/stop_words_ingles_spacy.csv')
stop_words_ingles_spacy = stop_pt['stop_word'].tolist()

stop_arquivo_incluidos = pd.read_csv('data/stop_words_incluidos.csv')
stop_incluidos = stop_arquivo_incluidos['stop_word'].tolist()
stop_words_portugues_spacy = stop_words_portugues_spacy + stop_incluidos

token_arquivo_hard = pd.read_csv('data/hard.csv')
token_hard = token_arquivo_hard['hard'].tolist()

token_arquivo_soft = pd.read_csv('data/soft.csv')
token_soft = token_arquivo_soft['soft'].tolist()


# Funções
def str_lower(text):
  return text.lower()

def remove_extra_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def replace_empty(text, text_empty_replace):
    if text is None or text == '':
        return text_empty_replace
    return text

def remove_numbers_id_text(text):
    return re.sub(r'\b\d+\b', '', text)

def replace_hyphens(text,text_empty_replace):
  return text_empty_replace if text == '-' else text

def replace_null(text,text_empty_replace):
    return text_empty_replace if pd.isna(text) else text

def normalize_accents(text):
  return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")

def remove_punctuation(text):
  punctuations = string.punctuation
  table = str.maketrans({key: " " for key in punctuations})
  text = text.translate(table)
  return text

def ReplaceVazio(df,campo,valor):
  df[campo] = df[campo].replace('', valor)
  
  
def tokenizar_texto(text):
    if isinstance(text, str) and text.strip():
        return word_tokenize(text)
    return []

def aplicar_stopwords_portugues(tokens):
    if isinstance(tokens, list):
        return [palavra for palavra in tokens if palavra not in stop_words_portugues_spacy]
    return []

def aplicar_stopwords_ingles(tokens):
    if isinstance(tokens, list): 
        return [palavra for palavra in tokens if palavra not in stop_words_ingles_spacy]
    return []

def pipeline(text,text_empty_replace, steps=[]):
    for step in steps:
        if step == replace_empty or step == replace_hyphens or step == replace_null:
            text = step(text, text_empty_replace)
        else:
            text = step(text)
    return text



# Carregando Dataframe
df_para_ml_treinado = pd.read_csv("data/df_para_ml_treinado.csv")
df_vagas_filtrado = pd.read_csv("data/df_vagas_filtrado.csv")
df_applicants_filtrado = pd.read_csv("data/df_applicants_filtrado.csv")
df_curriculos_applicants = pd.read_csv("data/df_applicants_streamlit_IA.csv")


# Dataframe Resumidos
vagas = df_para_ml_treinado.id_vaga.unique()
df_selecionar_cliente = df_vagas_filtrado[["id_vaga","informacoes_basicas_cliente","informacoes_basicas_titulo_vaga"]][df_vagas_filtrado["id_vaga"].isin(vagas)]


# Listas
status_aprovado = [
     'Contratado pela Decision'
    ,'Aprovado'
    ,'Contratado como Hunting'
]

colunas_id = ['id_vaga', 'codigo', 'id_applicants']


# Carregar Modelos
tfidf_atividades = joblib.load('modelos/tfidf_atividades.joblib')
tfidf_competencias = joblib.load('modelos/tfidf_competencias.joblib')
tfidf_observacoes = joblib.load('modelos/tfidf_observacoes.joblib')
tfidf_titulo = joblib.load('modelos/tfidf_titulo.joblib')
tfidf_objetivo = joblib.load('modelos/tfidf_objetivo.joblib')
tfidf_conhecimentos = joblib.load('modelos/tfidf_conhecimentos.joblib')
tfidf_certificacoes = joblib.load('modelos/tfidf_certificacoes.joblib')
tfidf_cv = joblib.load('modelos/tfidf_cv.joblib')

clf = joblib.load('modelos/modelo_prever_candidato.joblib')

# CORPO DA PÁGINA
st.subheader("Agentes de Inteligência Artificial para Recrutamento 🧠")

st.write('')
st.write("##### **1. Análise de Match da Vaga com o Candidato**")

opcao_cliente = st.selectbox(
        "Selecione o Cliente:",
        ["Selecione o Cliente"] + df_selecionar_cliente["informacoes_basicas_cliente"].unique().tolist()
)

if opcao_cliente != "Selecione o Cliente":
    
    opcao_vaga = st.selectbox(
        "Selecione a Vaga:",
        df_selecionar_cliente[df_selecionar_cliente["informacoes_basicas_cliente"] == opcao_cliente]["informacoes_basicas_titulo_vaga"].unique().tolist()
    )
        
    vaga_selecionada = df_selecionar_cliente[df_selecionar_cliente["informacoes_basicas_titulo_vaga"] == opcao_vaga]["id_vaga"].iloc[0]

        
    # 1. Filtrar os dados da vaga desejada
    df_applicants_vaga = df_para_ml_treinado[df_para_ml_treinado['id_vaga'] == vaga_selecionada].copy()
    df_applicants_vaga['situacao_candidado_target'] = df_applicants_vaga['situacao_candidado'].apply(lambda x: 1 if x in status_aprovado else 0)
    df_applicants_vaga = df_applicants_vaga.drop('situacao_candidado', axis=1)
        
    
    # 2. Armazenar os IDs que serão usados depois
    ids_vaga = df_applicants_vaga['id_vaga'].values
    ids_applicants = df_applicants_vaga['id_applicants'].values
    
    
    ### - debug ### 
    # st.write('debug')
    # type_counts = df_applicants_vaga['perfil_vaga_competencia_tecnicas_e_comportamentais'].apply(type).value_counts()
    # st.table(type_counts)
    ### - fim debug ###
    
    df_applicants_vaga['perfil_vaga_competencia_tecnicas_e_comportamentais'] = df_applicants_vaga['perfil_vaga_competencia_tecnicas_e_comportamentais'].astype(str)

    
    # 3. Dropar os IDs antes de passar para o modelo
    df_applicants_vaga['perfil_vaga_principais_atividades'] = df_applicants_vaga['perfil_vaga_principais_atividades'].apply(lambda x: ' '.join(x))
    df_applicants_vaga['perfil_vaga_competencia_tecnicas_e_comportamentais'] = df_applicants_vaga['perfil_vaga_competencia_tecnicas_e_comportamentais'].apply(lambda x: ' '.join(x))
    df_applicants_vaga['perfil_vaga_demais_observacoes'] = df_applicants_vaga['perfil_vaga_demais_observacoes'].apply(lambda x: ' '.join(x))
    df_applicants_vaga['informacoes_basicas_titulo_vaga_resumido'] = df_applicants_vaga['informacoes_basicas_titulo_vaga_resumido'].apply(lambda x: ' '.join(x))

    df_applicants_vaga['infos_basicas_objetivo_profissional'] = df_applicants_vaga['infos_basicas_objetivo_profissional'].apply(lambda x: ' '.join(x))
    df_applicants_vaga['informacoes_profissionais_conhecimentos_tecnicos'] = df_applicants_vaga['informacoes_profissionais_conhecimentos_tecnicos'].apply(lambda x: ' '.join(x))
    df_applicants_vaga['informacoes_profissionais_outras_certificacoes'] = df_applicants_vaga['informacoes_profissionais_outras_certificacoes'].apply(lambda x: ' '.join(x))
    df_applicants_vaga['cv_pt'] = df_applicants_vaga['cv_pt'].apply(lambda x: ' '.join(x))
    
    # 4. Cria as matrizes esparsas TF-IDF
    X_atividades = tfidf_atividades.transform(df_applicants_vaga['perfil_vaga_principais_atividades'])
    X_competencias = tfidf_competencias.transform(df_applicants_vaga['perfil_vaga_competencia_tecnicas_e_comportamentais'])
    X_observacoes = tfidf_observacoes.transform(df_applicants_vaga['perfil_vaga_demais_observacoes'])
    X_titulo = tfidf_titulo.transform(df_applicants_vaga['informacoes_basicas_titulo_vaga_resumido'])

    X_objetivo = tfidf_objetivo.transform(df_applicants_vaga['infos_basicas_objetivo_profissional'])
    X_conhecimentos = tfidf_conhecimentos.transform(df_applicants_vaga['informacoes_profissionais_conhecimentos_tecnicos'])
    X_certificacoes = tfidf_certificacoes.transform(df_applicants_vaga['informacoes_profissionais_outras_certificacoes'])
    X_cv = tfidf_cv.transform(df_applicants_vaga['cv_pt'])

    df_applicants_vaga = df_applicants_vaga.drop(columns=colunas_id)

    df_applicants_vaga.drop(columns=['infos_basicas_objetivo_profissional'
    , 'informacoes_profissionais_conhecimentos_tecnicos'
    , 'informacoes_profissionais_outras_certificacoes'
    , 'cv_pt'
                                        ], inplace=True)

    df_applicants_vaga.drop(columns=[
    'perfil_vaga_principais_atividades'
    ,'perfil_vaga_competencia_tecnicas_e_comportamentais'
    ,'perfil_vaga_demais_observacoes'
    ,'informacoes_basicas_titulo_vaga_resumido'
                                ], inplace=True)

    X_numerico = csr_matrix(df_applicants_vaga.drop(columns=['situacao_candidado_target']).values)

    X_applicants = hstack([
        X_atividades,
        X_competencias,
        X_observacoes,
        X_titulo,
        X_objetivo,
        X_conhecimentos,
        X_certificacoes,
        X_cv,
        X_numerico
    ])
        
    # 5. Fazer a previsão com o modelo
    y_proba = clf.predict_proba(X_applicants)[:, 1]
    
    
    # 6. Criar um DataFrame com os resultados e reanexar os IDs
    df_resultado = pd.DataFrame({
        'id_vaga': ids_vaga,
        'id_applicants': ids_applicants,
        'Match': y_proba
    })
    
    
    df_resultado_final = pd.merge(
                                    df_resultado.sort_values(by='Match', ascending=False),
                                    df_applicants_filtrado[['id_applicants', 'informacoes_pessoais_nome', 'infos_basicas_objetivo_profissional']],
                                    on='id_applicants',
                                    how='inner'
                                )
    
    df_resultado_final = df_resultado_final.rename(columns={
        'informacoes_pessoais_nome': 'Nome Candidato',
        'infos_basicas_objetivo_profissional': 'Objetivo Profissional'})

        
    # 7. Exibe o resultado na página
    st.data_editor(
    df_resultado_final[['Match', 'Nome Candidato', 'Objetivo Profissional']],
    column_config={
        "Match": st.column_config.ProgressColumn(
            label="Match",
            width="small",
            format="%.2f%%", 
            min_value=0,
            max_value=1
        ),
        "Nome Candidato": st.column_config.Column(
            label="Nome Candidato",
            width="medium"
        ),
        "Objetivo Profissional": st.column_config.Column(
            label="Objetivo Profissional",
            width="large"
        ),
    },
    use_container_width=True,
    hide_index=True
)
    
    
    st.write('')
    st.write('---')
    st.write("##### **2. Avaliar o Candidato**")
    
    # 8. Lista com os candidados da vaga e filtro para selecionar candidato
    lista_candidatos_match = (df_resultado_final["Match"].apply(lambda x: f"{x:.2%}") + " - " + df_resultado_final["Nome Candidato"]).tolist()
    
    opcao_candidato = st.selectbox(
        "Selecione o Candidato:",
        ["Selecione o Candidato"] + lista_candidatos_match
    )
    
    if opcao_candidato != "Selecione o Candidato":
          
        nome_candidato_chave = opcao_candidato.split(" - ", 1)[1]        
        
        df_curriculos_applicants = df_curriculos_applicants[df_curriculos_applicants['informacoes_pessoais_nome'] == nome_candidato_chave]
        
        df_vaga_focada = df_vagas_filtrado[df_vagas_filtrado["id_vaga"] == vaga_selecionada]
        
         # 9. Extrai palavras e faz regex do texto para exibir as palavras que são iguais em vagas e no candidato
        
        steps = [str_lower, normalize_accents, remove_punctuation, replace_empty, remove_extra_spaces, remove_numbers_id_text, tokenizar_texto, aplicar_stopwords_portugues, aplicar_stopwords_ingles]
        df_vaga_focada['perfil_vaga_principais_atividades_token'] = df_vaga_focada['perfil_vaga_principais_atividades'].apply(pipeline
                                            ,text_empty_replace='', steps=steps)
        
        df_vaga_focada['perfil_vaga_competencia_tecnicas_e_comportamentais_token'] = df_vaga_focada['perfil_vaga_competencia_tecnicas_e_comportamentais'].apply(pipeline
                                            ,text_empty_replace='', steps=steps)
        
        df_curriculos_applicants['cv_pt_token'] = df_curriculos_applicants['cv_pt'].astype(str).apply(pipeline
                                            ,text_empty_replace='', steps=steps)
        
        
        valores_applicants  = df_curriculos_applicants['cv_pt_token']
        
        valores_vaga_ativ = df_vaga_focada['perfil_vaga_principais_atividades_token'] 
        
        valores_vaga_comp = df_vaga_focada['perfil_vaga_competencia_tecnicas_e_comportamentais_token'] 
        
        
        set_vagas_ativ = set([item for sublist in valores_vaga_ativ for item in sublist])
        set_vagas_comp = set([item for sublist in valores_vaga_comp for item in sublist])
        set_apllicants = set([item for sublist in valores_applicants for item in sublist])

        # Interseção
        interseccao_applicants_vaga_ativ = list(set_vagas_ativ & set_apllicants)
        interseccao_applicants_vaga_comp = list(set_vagas_comp & set_apllicants)
        intersecao_final = list(set(interseccao_applicants_vaga_ativ) | set(interseccao_applicants_vaga_comp))

        
        
        badges_final = " ".join([f":green-badge[{':material/check:'} {item}]" for item in intersecao_final])
        
        
        
        st.write('---')
        st.write('**Comparativo de Tokens do Currículo com Principais Atividades, Competência Técnicas e Comportamentais da Vaga:**')
        st.markdown(badges_final)
        
        interseccao_hard = list(set(intersecao_final) & set(token_hard))
        interseccao_soft = list(set(intersecao_final) & set(token_soft))
        
        qtde_hard = len(interseccao_hard)
        qtde_soft =len(interseccao_soft)
        
        data_skill_vaga = {
                    'skill': ['Hard Skill', 'Soft Skill'],
                    'quantidade': [qtde_hard, qtde_soft]
                }

        df_skill_vaga = pd.DataFrame(data_skill_vaga)
        df_skill_vaga['categoria'] = 'Skills'
        # Gráfico de Skill
        fig = px.bar(
            df_skill_vaga,
            x='quantidade',
            y='categoria',          
            color='skill',          
            orientation='h',
            text='quantidade',
            color_discrete_map={
                    'Hard Skill': '#3390E0',  
                    'Soft Skill': '#FF5E5E'   
            },
            title= None
        )

        fig.update_traces(
            textposition='inside',
            textfont=dict(size=16, color='white'),
            insidetextanchor='middle',
            marker_line_width=0,
            selector=dict(type='bar'),
            hoverinfo='skip',
            hovertemplate=''
        )
        fig.update_layout(
            barmode='stack',
            bargap=0,
            height=150,  
            margin=dict(l=60, r=60, t=60, b=40),
            showlegend=False,
            yaxis=dict(showticklabels=False, title=''),
            xaxis=dict(
                showticklabels=False,  
                showgrid=False,
                zeroline=False,
                title=''
            )
        )

        if qtde_hard and qtde_hard > 0:
            fig.add_annotation(
                x=qtde_hard / 2,
                y=0,
                text="Hard Skill",
                showarrow=False,
                font=dict(size=16, color='#FFFFFF'),
                xanchor='center',
                yanchor='bottom'
            )

        if qtde_soft and qtde_soft > 0:
            fig.add_annotation(
                x=qtde_hard + qtde_soft / 2,
                y=0,
                text="Soft Skill",
                showarrow=False,
                font=dict(size=16, color='#FFFFFF'),
                xanchor='center',
                yanchor='bottom'
            )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        
        col10, col20 = st.columns(2)
        
        with col10:
            st.markdown("<span style='color:#0068C9;'>Hard Skill</span>", unsafe_allow_html=True)
            badges_hard = " ".join([f":blue-badge[{':material/check:'} {item}]" for item in interseccao_hard])
            st.markdown(badges_hard)
        with col20:
            st.markdown("<span style='color:#FF2B2B;'>Soft Skill</span>", unsafe_allow_html=True)
            badges_soft = " ".join([f":red-badge[{':material/check:'} {item}]" for item in interseccao_soft])
            st.markdown(badges_soft)  
        
        
        
        # Exibe dados da vaga e do candidato (currículo)
        st.write('---')
        st.write('### **Vaga**')
        st.write('**Principais Atividades da Vaga:**')
        st.markdown(df_vaga_focada['perfil_vaga_principais_atividades'].iloc[0])
        
        st.write('**Principais Competência Técnicas e Comportamentais:**')
        st.markdown(df_vaga_focada['perfil_vaga_competencia_tecnicas_e_comportamentais'].iloc[0])
        st.write('---')
        st.write('### **Candidato**')
        st.write('**Currículo**')
        st.markdown(df_curriculos_applicants['cv_pt'].iloc[0])
        st.write('---')
        st.write('#### **Entrar em contato com o Candidato**')
        
        col30, col40 = st.columns([3,10])
                
        match = re.search(r"telefone[:\-\s]*([\d\s\(\)\-]{7,20})", df_curriculos_applicants['cv_pt'].iloc[0], re.IGNORECASE)
        
        if match:
            valor_telefone_loc = match.group(1)
            telefone_localizado = re.sub(r"\D", "", valor_telefone_loc)
            telefone_localizado = '55' + telefone_localizado
        else:
            telefone_localizado = ''
            

        with col30:
            telefone = st.text_input("Celular com WhatsApp (aperte Enter para confirmar)", max_chars=15, value = telefone_localizado)

        
        url_whatsapp = f"https://wa.me/{telefone}"

        button_html = f'''
        <a href="{url_whatsapp}" target="_blank">
            <button style="
                background-color: #25D366;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;">
                Abrir WhatsApp
            </button>
        </a>
        '''

        st.markdown(button_html, unsafe_allow_html=True)
        
        
        
        
        

        
    
        
    
