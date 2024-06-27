import streamlit as st 
import pandas as pd 

# Configurar da estrutura da página
st.set_page_config(
    layout="wide",
    page_title="Dashboard"
)

# Texto explicativo
st.markdown('# Perfil dos Pacientes')
st.divider()
st.markdown('''A base de dados inicial foi dividida em três bases: Atendimentos, Pacientes e Comorbidades. Essa parte é dedicada a uma análise do perfil dos pacientes atendidos no hospital no período em questão.''')

# Manter dados na session para poder usar em outras páginas
if not 'dados' in st.session_state:
    # Importando banco de dados
    df_atendimentos = pd.read_csv('atendimentos.csv', decimal=',', index_col=0)
    df_pacientes = pd.read_csv('pacientes.csv', decimal=',', index_col=0)
    df_comorbidades = pd.read_csv('comorbidades.csv', decimal=',', index_col=0)
    dados = {'df_atendimentos': df_atendimentos,
             'df_pacientes': df_pacientes,
             'df_comorbidades': df_comorbidades}
    st.session_state['dados'] = dados

df_atendimentos = st.session_state['dados']['df_atendimentos']
df_pacientes = st.session_state['dados']['df_pacientes']
df_comorbidades = st.session_state['dados']['df_comorbidades']

# Filtros Sidebar
df_pacientes["REINTERNADO"] = df_pacientes["TOTAL_INTERNACOES"] > 1
df_reinternacao = pd.DataFrame(df_pacientes["REINTERNADO"].value_counts().index)
df_reinternacao = st.sidebar.selectbox("REINTERNADO", df_reinternacao)
df_reinternacao = df_pacientes[(df_pacientes["REINTERNADO"] == df_reinternacao)]

# Atendimentos: Tabelas importantes
# N° Pacientes
metrica_num_pac = df_reinternacao["REINTERNADO"].value_counts()
# N° Internações
num_int = df_reinternacao["TOTAL_INTERNACOES"].sum()
int_por_pac = num_int/metrica_num_pac
# N° Óbitos
df_mortes = df_reinternacao[(df_reinternacao["SITUACAO"] == "ÓBITO")]
num_mortes = int(df_mortes["SITUACAO"].value_counts())
# N° Vivos
df_vivos = df_reinternacao[(df_reinternacao["SITUACAO"] == "VIVO")]
num_vivos = int(df_vivos["SITUACAO"].value_counts())

# Print
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="N° Pacientes", value=metrica_num_pac)
col2.metric(label="N° Sobreviventes", value=num_vivos)
col3.metric(label="N° Óbitos", value=num_mortes)
col4.metric(label="Taxa de Óbitos (%)", value=round(num_mortes*100/num_vivos,1))

st.subheader('N° de Pacientes por Sexo e por Grau de Ensino')
col1, col2 = st.columns(2)
# Qtd Pacientes x Sexo
sexo = pd.DataFrame(df_reinternacao.groupby("SEXO")["SEXO"].count())
sexo = sexo.rename(columns={'': 'SEXO', 'SEXO': 'Quantidade'})
col1.bar_chart(sexo)

# Qtd Pacientes x Grau de Ensino
ensino = pd.DataFrame(df_reinternacao.groupby("GRAU_INS")["GRAU_INS"].count())
ensino = ensino.rename(columns={'': 'Ensino', 'GRAU_INS': 'Quantidade'})
col2.bar_chart(ensino)

# Qtd Pacientes x Cidade
cidade = pd.DataFrame(df_reinternacao.groupby("CIDADE")["CIDADE"].count())
cidade = cidade.rename(columns={'': 'Cidade', 'CIDADE': 'Quantidade'})
st.subheader('N° de Pacientes por Cidade')
st.bar_chart(cidade)

# Qtd Pacientes x Idade
idade = pd.DataFrame(df_reinternacao.groupby("IDADE")["IDADE"].count())
idade = idade.rename(columns={'': 'Idade', 'IDADE': 'Quantidade'})
st.subheader('N° de Pacientes por Idade')
st.bar_chart(idade)

st.markdown('# Análise de Internações')
# Print
internacao = df_reinternacao["TOTAL_INTERNACOES"]
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Máximo", value=internacao.max())
col2.metric(label="Média", value=round(int_por_pac,2))
col3.metric(label="Desvio Padrão", value=internacao.std().__round__(2))
col4.metric(label="Mediana", value=internacao.median())

# Quantidade de pacientes por N° internações
st.subheader('Quantidade de pacientes por N° internações')
internacao = pd.DataFrame(df_reinternacao.groupby("TOTAL_INTERNACOES")["TOTAL_INTERNACOES"].count())
internacao = internacao.rename(columns={'': 'Total de Internações', 'TOTAL_INTERNACOES': 'Quantidade'})
st.bar_chart(internacao)

# Quantidade de internações por idade
st.subheader('Quantidade de Internações por Idade')
internacao_idade = pd.DataFrame(df_reinternacao.groupby("IDADE")["TOTAL_INTERNACOES"].sum())
internacao_idade = internacao_idade.rename(columns={'IDADE': 'IDADE', 'TOTAL_INTERNACOES': 'Quantidade'})
st.bar_chart(internacao_idade)
