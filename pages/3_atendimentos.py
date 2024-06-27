import streamlit as st
import pandas as pd

# Texto explicativo
st.markdown('# Análise de Atendimentos')
st.divider()
st.markdown('''Essa seção é destinada para análise dos atendimentos do hospital.''')

df_atendimentos = st.session_state['dados']['df_atendimentos']
df_pacientes = st.session_state['dados']['df_pacientes']
df_comorbidades = st.session_state['dados']['df_comorbidades']

# Filtros Sidebar
df_pacientes["REINTERNADO"] = df_pacientes["TOTAL_INTERNACOES"] > 1
df_reinternacao = pd.DataFrame(df_pacientes["REINTERNADO"].value_counts().index)
df_reinternacao = st.sidebar.selectbox("REINTERNADO", df_reinternacao)
df_reinternacao = df_pacientes[(df_pacientes["REINTERNADO"] == df_reinternacao)]

atendimentos = pd.merge(df_atendimentos, df_reinternacao, on='CD_PACIENTE')

# Atendimentos: Tabelas importantes
mes = pd.DataFrame(atendimentos.groupby("MES")["MES"].count())
mes = mes.rename(columns={'': 'mes', 'MES': 'Quantidade'})
st.subheader('N° de Atendimentos por Mês')
st.bar_chart(mes)

hora = pd.DataFrame(atendimentos.groupby("HORA")["HORA"].count())
hora = hora.rename(columns={'': 'HORA', 'HORA': 'Quantidade'})
st.subheader('N° de Atendimentos por Hora')
st.scatter_chart(hora)

risco = pd.DataFrame(atendimentos.groupby("RISCO")["RISCO"].count())
risco = risco.rename(columns={'': 'risco', 'RISCO': 'Quantidade'})
st.subheader('N° de Atendimentos por Classificação de Risco')
st.bar_chart(risco)

st.subheader('N° de Atendimentos por Tipo de Alta')
tipo = pd.DataFrame(atendimentos.groupby("TIPO_ALTA")["TIPO_ALTA"].count())
tipo = tipo.rename(columns={'': 'tipo', 'TIPO_ALTA': 'Quantidade'})
st.bar_chart(tipo)
st.dataframe(tipo.sort_values(by=["Quantidade"], ascending=False))

st.subheader('N° de Atendimentos por Grupo de Sintomas')
sintomas = pd.DataFrame(atendimentos.groupby("GRUPO_SINTOMA")["GRUPO_SINTOMA"].count())
sintomas = sintomas.rename(columns={'': 'tipo', 'GRUPO_SINTOMA': 'Quantidade'})
st.bar_chart(sintomas)
st.dataframe(sintomas.sort_values(by=["Quantidade"], ascending=False))
