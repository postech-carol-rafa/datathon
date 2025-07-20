# Importando bibiotecas
import streamlit as st



st.title('Documentação')


st.write('''
---        
          
**Faculdade de Informática de Administração Paulista – FIAP**


*Pos Tech em Data Analytics*

Turma 7DTAT

Alunos:

* Caroline Yuri Noguti - RM 358779
* Rafael Nascimento Coutinho – RM 358930

          ''')

st.write('''
---     
#### **1.  Visão Geral do Projeto**

**Objetivo principal do projeto:**
 
Impulsionar a eficiência e redução do tempo do processo de recrutamento na empresa Decision, por meio de uma plataforma inteligente que aplica modelos preditivos baseados em dados históricos e comportamentais. A solução visa aumentar a assertividade nas contratações, automatizar etapas do processo seletivo, melhorar a experiência de candidatos e clientes, e fornecer insights gerenciais para aprimorar estratégias de captação e alocação de talentos. Com dashboards analíticos e IA aplicada ao match entre candidatos e vagas, a plataforma garante visibilidade operacional e posiciona a empresa como referência em recrutamento orientado por dados no setor de bodyshop.


**Problema ou oportunidade que será abordado:**

* Busca de candidatos: A empresa enfrenta dificuldade em localizar perfis ideais dentro do tempo necessário, mesmo utilizando múltiplas plataformas como LinkedIn, InfoJobs e grupos de WhatsApp.

* Entrevistas: Falta de padronização pode levar à perda de informações importantes. Além disso, há dificuldade em avaliar o engajamento dos candidatos, e por conta da pressão por agilidade, a etapa é frequentemente ignorada, comprometendo a qualidade da seleção.

* Seleção final: O desafio é garantir que o candidato selecionado possua as competências técnicas exigidas, se encaixe na cultura da empresa contratante e esteja realmente motivado para assumir a vaga.

**Escopo geral**

Desenvolver uma plataforma analítica e inteligente que permita à empresa Decision visualizar e avaliar dados relacionados a vagas de emprego, candidatos e empresas contratantes. A aplicação utiliza inteligência artificial para sugerir o melhor match entre candidato e vaga, ampliando a eficiência do processo de recrutamento e reduzindo o tempo do processo de contratação.

---

#### **2. Objetivos de Negócio**
* Otimizar o processo de recrutamento com base em dados históricos e comportamentais, aumentando a agilidade na triagem e na identificação de perfis aderentes às vagas abertas.

* Gerar insights gerenciais para aprimorar a alocação de talentos e estratégias de captação, usando análises preditivas para antecipar demandas e orientar decisões mais assertivas.

* Oferecer visibilidade sobre o desempenho das vagas, perfil dos candidatos e comportamento das empresas contratantes, permitindo diagnóstico preciso da operação de recrutamento.

* Automatizar o processo de recomendação de candidatos por vaga com o uso de Inteligência Artificial, promovendo o match preditivo entre perfis e oportunidades com base em critérios técnicos e comportamentais, reduzindo tempo e aumentando a assertividade nas contratações.

---

#### **3. Funcionalidades Gerais**

**Painel Principal:**

O Dashboard Principal tem como objetivo fornecer uma visão macro e consolidada da performance das operações de recrutamento, com foco em resultados, comportamento dos candidatos e demandas dos principais clientes. Voltado para acompanhamento gerencial, este painel permite decisões estratégicas com base em dados atualizados e visualmente intuitivos.
* **Candidatos contratados pela Hunting:**
Volume de profissionais captados diretamente via busca ativa e convertidos em contratação.
* **Candidatos contratados pela Decision:** 
Total de contratações originadas por vagas internas ou direcionadas ao time da Decision.
* **Candidatos que desistiram da vaga:** 
Número de profissionais que interromperam o processo seletivo por iniciativa própria.
* **Candidatos encaminhados ao requisitante:** 
Candidatos triados e enviados para avaliação da empresa contratante.
* **Candidatos não aprovados pelo cliente:** 
Perfis rejeitados após avaliação interna por parte do requisitante.
* **Candidatos sem interesse na vaga:** 
Total de profissionais que recusaram continuar no processo devido à vaga ofertada.
* **Gráfico de quantidade de vagas disponibilizada:**
Acompanha o ritmo de abertura de novas posições, sinalizando picos e sazonalidade da demanda.
* **Gráfico de divisão de vagas por região:** 
Permite analisar a distribuição geográfica das oportunidades, apoiando decisões de segmentação ou realocação de foco operacional.
* **Gráfico de evolução das requisições de vaga – Top 5 Clientes:**
Identifica os principais demandantes de vagas ao longo do tempo, revelando ciclos, crescimento de contas e foco comercial


**Dashboard:**

Visão estratégica do desempenho do processo de recrutamento da empresa Decision, permitindo o acompanhamento de vagas, volume de contratações realizadas, tempo médio de preenchimento e quantidade de vagas. A ferramenta também possibilita a análise dos indicadores, fornecendo subsídios analíticos para decisões gerenciais, otimização de esforços e aprimoramento contínuo da eficiência na alocação de talentos. 

* **Filtros campos: Unidade Decision, Cliente e Período (Ano e Trimestre).** 
Permitem segmentar os dados conforme a necessidade de análise e geram uma visualização personalizada e dinâmica para diferentes públicos ou contextos.
	
            Unidade Decision: Análise por operação/local.     
            Cliente: Foco em empresas contratantes específicas.
            Período: Limitar análise conforme data de referência.

* **Quantidade total de vagas**
Fornece uma visão clara do volume e estágio dos processos seletivos em curso, permitindo acompanhar o fluxo operacional e identificar possíveis gargalos ou etapas que exigem atenção da gestão.

* **Quantidade de contratações realizadas**
É um termômetro direto da produtividade do time de recrutamento. Ajuda a mensurar o impacto real das vagas conduzidas e serve como base para análise de conversão e desempenho.
* **Quantidade por status da vaga**
O indicador mostra quantas vagas estão em cada etapa do recrutamento (Encaminhado ao requisitante, não aprovado pelo cliente, desistiu, sem interesse na vaga, contratado pelo hunting e contratado pela decision). Essa análise ajuda a identificar gargalos e melhorar a gestão dos processos de seleção e planejamento de talentos.

* **Tempo médio de contratação, encaminhamento ao requisitante, dias para avaliação do RH e entrevista cliente**
Indica a agilidade do processo seletivo e sua eficiência operacional. Um tempo elevado pode refletir lentidão na triagem, baixa aderência dos candidatos ou atrasos internos, influenciando diretamente o custo e a satisfação do cliente

* **Top 5 vagas por perfil de área de atuação**
Destaca as cinco áreas com maior número de vagas abertas, permitindo entender quais perfis profissionais estão em alta demanda e orientar estratégias de recrutamento conforme a tendência do mercado.

* **Top 10 clientes por prioridade da vaga**
Apresenta os dez principais clientes que têm vagas com maior prioridade, ajudando a direcionar esforços para atender demandas mais urgentes e estratégicas.

* **Evolução diária das vagas por prioridade**
Monitora o crescimento ou redução diária das vagas de acordo com seu nível de prioridade (alta, média, baixa e não informado). Esse acompanhamento apoia a gestão ágil e a alocação assertiva de recursos de recrutamento.

* **Quantidade de vagas por área de atuação**
Permite entender a demanda por perfis técnicos ou áreas específicas. Isso apoia decisões de priorização, especialização da equipe e distribuição de esforço conforme o perfil das oportunidades contratantes. Exemplo: Vaga TI- Projetos, TI – SAP, TI – Infraestrutura...

* **Quantidade de vagas por nível do profissional**
Distribui o número de vagas conforme o nível de senioridade exigido (júnior, pleno, sênior, liderança, etc), fornecendo insights sobre o perfil profissional mais requisitado e auxiliando no alinhamento das ações de atração de talentos.


**Dashboard:**

Visão estratégica do desempenho do processo de recrutamento da empresa Decision, permitindo o acompanhamento de vagas, volume de contratações realizadas, tempo médio de preenchimento e quantidade de vagas. A ferramenta também possibilita a análise dos indicadores, fornecendo subsídios analíticos para decisões gerenciais, otimização de esforços e aprimoramento contínuo da eficiência na alocação de talentos. 


* **Filtros campos: Unidade Decision, Cliente e Período (Ano e Trimestre)**
Permitem segmentar os dados conforme a necessidade de análise e geram uma visualização personalizada e dinâmica para diferentes públicos ou contextos.
        Unidade Decision: Análise por operação/local.
        Cliente: Foco em empresas contratantes específicas.
        Período: Limitar análise conforme data de referência.

* **Quantidade total de vagas**
Fornece uma visão clara do volume e estágio dos processos seletivos em curso, permitindo acompanhar o fluxo operacional e identificar possíveis gargalos ou etapas que exigem atenção da gestão.

* **Quantidade de contratações realizadas**
É um termômetro direto da produtividade do time de recrutamento. Ajuda a mensurar o impacto real das vagas conduzidas e serve como base para análise de conversão e desempenho.
* **Quantidade por status da vaga**
O indicador mostra quantas vagas estão em cada etapa do recrutamento (Encaminhado ao requisitante, não aprovado pelo cliente, desistiu, sem interesse na vaga, contratado pelo hunting e contratado pela decision). Essa análise ajuda a identificar gargalos e melhorar a gestão dos processos de seleção e planejamento de talentos.

* **Tempo médio de contratação, encaminhamento ao requisitante, dias para avaliação do RH e entrevista cliente**
Indica a agilidade do processo seletivo e sua eficiência operacional. Um tempo elevado pode refletir lentidão na triagem, baixa aderência dos candidatos ou atrasos internos, influenciando diretamente o custo e a satisfação do cliente

* **Top 5 vagas por perfil de área de atuação**
Destaca as cinco áreas com maior número de vagas abertas, permitindo entender quais perfis profissionais estão em alta demanda e orientar estratégias de recrutamento conforme a tendência do mercado.

* **Top 10 clientes por prioridade da vaga**
Apresenta os dez principais clientes que têm vagas com maior prioridade, ajudando a direcionar esforços para atender demandas mais urgentes e estratégicas.

* **Evolução diária das vagas por prioridade**
Monitora o crescimento ou redução diária das vagas de acordo com seu nível de prioridade (alta, média, baixa e não informado). Esse acompanhamento apoia a gestão ágil e a alocação assertiva de recursos de recrutamento.

* **Quantidade de vagas por área de atuação**
Permite entender a demanda por perfis técnicos ou áreas específicas. Isso apoia decisões de priorização, especialização da equipe e distribuição de esforço conforme o perfil das oportunidades contratantes. Exemplo: Vaga TI- Projetos, TI – SAP, TI – Infraestrutura...

* **Quantidade de vagas por nível do profissional**
Distribui o número de vagas conforme o nível de senioridade exigido (júnior, pleno, sênior, liderança, etc), fornecendo insights sobre o perfil profissional mais requisitado e auxiliando no alinhamento das ações de atração de talentos.


**Dashboard Recrutamento Inteligente:**

Oferecer uma visão detalhada e analítica de cada vaga em andamento, integrando o desempenho do processo seletivo, perfil dos candidatos e recomendações automáticas geradas por Inteligência Artificial. O painel facilita o monitoramento estratégico da vaga, com foco na eficiência, assertividade e evolução do processo.

* **Filtros Campos: Cliente e Vaga**
Permitem segmentar os dados conforme a necessidade de análise e geram uma visualização personalizada e dinâmica para diferentes públicos ou contextos.
    Cliente: Foco em empresas contratantes específicas.
    Vaga: Segmentar por vaga disponíveis para contratação

* **Lista de candidatos: Nome, Objetivo profissional e % de match com a vaga**
Lista de candidatos recomendados para a vaga selecionada de acordo com o perfil, ordenado do maior para menor match.

* **Filtro para seleção do candidato**
Seleção de candidato dentre os recomendados, para detalhamento do perfil

* **Tokens – Palavras chaves**
Palavras que possuem intersecção entre o currículo do candidato com a descrição da vaga

* **Descrição da vaga**
Descrição completa da vaga contendo as principais atividades a serem desempenhadas e principais competências técnicas e comportamentais

* **Currículo do candidato**
Descrição do currículo do candidato com informações detalhadas do seu perfil profissional, habilidades, experiências, informações de estudos, entre outros...

**Dashboard KPI**

O dashboard de KPIs serve para ajudar a monitorar o desempenho do recrutamento,, permitindo que gestores visualizem dados sobre vagas, candidatos e clientes. Os KPIs são métricas que indicam se os processos estão alinhados aos objetivos estratégicos, tornando a gestão mais eficiente e baseada em dados

* **Filtros Campos: Recrutador, Unidade Decision, Periodo (Ano e Trimestre)**

Permitem segmentar os dados conforme a necessidade de análise e geram uma visualização personalizada e dinâmica para diferentes públicos ou contextos.
    Cliente: Foco em empresas contratantes específicas.
    Recrutador: Segmentar por recrutar responsável pela vaga.
    
**Unidade Decision: Análise por operação/local.**
    Cliente: Foco em empresas contratantes específicas.
    Período: Limitar análise conforme data de referência.

* Média de currículos encaminhado ao requisitante 
Este indicador mostra a média de candidatos apresentados por vaga ao responsável pela contratação, refletindo o volume e a assertividade da triagem realizada pelo time de recrutamento.

* Tempo médio entre requisição e última atualização em dias 
Mede quantos dias, em média, se passaram entre a abertura da vaga e sua última movimentação. Esse dado ajuda a identificar possíveis atrasos ou falta de engajamento no processo.

* Top 10 clientes por recrutador
Aponta os clientes mais recorrentes de cada recrutador, revelando onde há maior demanda, vínculo ou especialização, o que pode apoiar na gestão de carteiras e na alocação de esforços.


* Quantidade por status da vaga 
O indicador mostra quantas vagas estão em cada etapa do recrutamento (Prospect, encaminhado ao requisitante, não aprovado pelo cliente, desistiu, sem interesse na vaga, contratado pelo hunting, não aprovado pelo requisitante, entrevista com o cliente, contratado pela decision). Essa análise ajuda a identificar gargalos e melhorar a gestão dos processos de seleção e planejamento de talentos.

---


#### **4. Funcionalidade de Inteligência Artificial**

**Sistema de Match Inteligente:**

*	Análise preditiva de compatibilidade entre perfil de vaga e candidato.
*	Sugestão automática de candidatos com maior probabilidade de sucesso para cada vaga.

**Treinamento de Modelo de Machine Learning:**

*	Modelo alimentado com dados históricos de processos seletivos anteriores, feedbacks e taxas de sucesso.
*	Aprendizado contínuo com base em novos dados inseridos na aplicação.
*	Avaliação da performance do modelo.

---

#### **5. Requisitos Funcionais**

**Dashboard Principal**

*	Exibir indicadores como número de candidatos contratados pela hunting, contratados pela decision, candidatos que desistiram da vaga, candidatos encaminhados ao requisitante, candidato não aprovado pelo cliente e sem interesse na vaga.
*	Gráficos de quantidade de vagas disponibilizadas e vagas divididas por região
*	Gráfico com a evolução de requisição de vagas pelos 5 principais clientes.

**Dashboard gerencial**

*	Apresentar visão consolidada do desempenho das vagas por status
*	Gerar gráficos sobre tempo médio de contratação, taxa de sucesso e perfil das vagas.

**Dashboard Recrutamento**

*	Executar triagem inteligente de candidatos contendo recomendação automática de candidatos com base em algoritmos preditivos.
*	Exibir índice de compatibilidade por vaga e candidato.
*	Listar os candidatos recomendados ordenados por grau de aderência.

---

#### **6. Requisitos Não Funcionais**

*	Aplicação disponível no Streamlit
*	Armazenamento em arquivo csv
*	Arquivos disponíveis no github
*	Todos os gráficos gerados utilizando biblioteca do Plotly
*	Metadados das bases
*	Desenho Técnico da solução
*	Desenho de fluxo de dados

#### **7. Detalhamento Analítico**
'''
)

st.image('imagens/diagrama_prep_dados.png')

st.write(
    
    
    '''
    
**Leitura, Limpeza e transformação de dados**

Definição de métricas principais para o modelo:

*	Perfil da vaga e principais atividades e demais observações
*	Competências técnicas e comportamentais
*	Título da vaga
*	Objetivos Profissionais
*	Conhecimento técnico e certificações
*	Currículo

**Arquitetura de Dados do Processo de Recrutamento**

Fontes de dados:
*	Arquivo de cadastro de candidatos: Prospects.json (Possui todas as prospecções de vagas que é utilizado em conjunto com os dados dos arquivos vagas.json e apllicants.json)
*	Cadastro de vagas: Vagas.json (Dados referentes as vagas abertas com a decision divididas entre informações básicas, perfil da vaga e benefícios.)
*	Cadastro de candidatos por vaga: Apllicants.json (Dados referente aos candidatos que serão analisados para as vagas e estão divididos entre Informações básicas, pessoais, profissionais, formação e o currículo.)
Tipo de dados utilizados: 
*	Dados de entrada: não estruturado em formato .json
*	Métrica para o modelo: TF-IDF é uma métrica usada para medir o peso de uma palavra em um documento dentro de um conjunto de textos. Ela combina a frequência da palavra no documento (TF) com a raridade dessa palavra em todo o corpus (IDF), ajudando a identificar termos mais relevantes e distintivos em contextos específicos

Análise exploratória dos dados com estatísticas descritivas:
*	Investigação inicial dos dados para compreensão de padrões e distribuição: Após analise de todos os campos de todas as bases (Prospects, apllicants e vagas), foi possível compreender o padrão dos dados, conceito das bases, e seleção das métricas a serem utilizadas para execução do projeto e os dados que precisariam ser utilizados para a execução do modelo.

Técnicas de modelagem: 
*	Tipo Modelo: Classificação
*	Modelo utilizado: Modelo LGBMClassifier
*	Aplicação de algoritmos para prever aderência e potencial de contratação

Feature engineering e seleção de variáveis 

Treinamento e validação de modelos preditivos

Criação de painéis interativos com métricas de desempenho

---

#### **8. Detalhamento Técnico**

*	Linguagens: Python
*	Ferramentas: Streamlit, GitHub, Jupyter
*	Armazenamento: Arquivos no github
*	Camada de visualização: dashboards com filtros dinâmicos no Streamlit
*	Dados de entrada: Arquivos no formato json
*	Dados de Saída: Arquivos no formato csv
*	Aplicação: Deploy no Streamlit

    
    '''
)

st.image('imagens/diagrama_princ.png')

st.write(
    '''

#### **9. Resultados do Modelo de Recomendação de Recrutamento Inteligente**

Em  nossa analise das métricas o modelo identifica bem quem será contratado, com bom recall (80%) e precisão (81%) — ou seja, erra pouco e perde poucos candidatos bons. 
Além disso, o F1-score está alto, o que mostra que o modelo está com uma métrica considerável

*	Recall (Revocação ou Sensibilidade): 0.78 → Dos exemplos que realmente eram da classe 0, 78% foram corretamente identificados. 
*	F1-score: 0.77 → Média harmônica entre precisão e recall. 
*	Support: 437 → Total de exemplos reais da classe 0. Classe 1 
*	Precision: 0.81 Recall: 0.80 F1-score: 0.80 
*	Support: 513 
*	Métricas gerais Accuracy: 0.79 → 79% das previsões   
 
 ---   

#### **10. Link**

**Notebook do projeto**
    '''
)
st.page_link("https://colab.research.google.com/drive/10wNPJjZ2LAxs-DkGqRph1IeVvmlGffdH?usp=sharing", label="Link para Notebook", icon="🔗")


st.write(
    
    '''
---

#### **11. Referências**

* Streamlit:    https://docs.streamlit.io/

* regex:    https://docs.python.org/3/library/re.html

* nltk: https://www.nltk.org/

* spacy:    https://spacy.io/

* Scikit-Learn Métricas:  https://scikit-learn.org/stable/api/sklearn.metrics.html   

* Scikit-Learn Pré-processamento: https://scikit-learn.org/stable/api/sklearn.preprocessing.html#module-sklearn.preprocessing

* Scikit-Learn TfidfVectorizer: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

* TfidfVectorizer: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

* LGBMClassifier:   https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html

* FIAP: Módulo 5 - Conteúdo de Dados Gerados por Humanos - Professores: Ana Raquel e Dheny Fernandes

* Alura: Curso de NLP: aplicando processamento de linguagem natural para análise de sentimentos - Professora: Valquíria Alencar
    
'''
)






