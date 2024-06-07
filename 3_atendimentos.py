import streamlit as st
import pandas as pd

# Texto explicativo
st.markdown('# Análise de Atendimentos')
st.divider()
st.markdown('''Essa seção é destinada para análise dos atendimentos do hospital.''')

df_comorbidades = pd.read_csv('comorbidades.csv', decimal=',', index_col=0)

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
situacao_pac = pd.DataFrame(df_atendimentos["SITUACAO"].value_counts().index)
situacao_pac = st.sidebar.selectbox("SITUACAO", situacao_pac)
df_atendimentos = df_atendimentos[(df_atendimentos["SITUACAO"] == situacao_pac)]

# Atendimentos: Tabelas importantes
mes = pd.DataFrame(df_atendimentos.groupby("MES")["MES"].count())
mes = mes.rename(columns={'': 'mes', 'MES': 'Quantidade'})
st.subheader('N° de Atendimentos por Mês')
st.bar_chart(mes)

risco = pd.DataFrame(df_atendimentos.groupby("RISCO")["RISCO"].count())
risco = risco.rename(columns={'': 'risco', 'RISCO': 'Quantidade'})
st.subheader('N° de Atendimentos por Classificação de Risco')
st.bar_chart(risco)

st.subheader('N° de Atendimentos por Tipo de Alta')
col1, col2 = st.columns(2)
tipo = pd.DataFrame(df_atendimentos.groupby("TIPO_ALTA")["TIPO_ALTA"].count())
tipo = tipo.rename(columns={'': 'tipo', 'TIPO_ALTA': 'Quantidade'})
col1.bar_chart(tipo)
col2.dataframe(tipo.sort_values(by=["Quantidade"], ascending=False).head())

st.subheader('N° de Atendimentos por Grupo de Sintomas')
col1, col2 = st.columns(2)
sintomas = pd.DataFrame(df_atendimentos.groupby("GRUPO_SINTOMA")["GRUPO_SINTOMA"].count())
sintomas = sintomas.rename(columns={'': 'tipo', 'GRUPO_SINTOMA': 'Quantidade'})
col1.bar_chart(sintomas)
col2.dataframe(sintomas.sort_values(by=["Quantidade"], ascending=False).head())