import streamlit as st
import pandas as pd

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
num_pac = df_reinternacao["REINTERNADO"].value_counts()

# Qtd Pacientes x Comorbidades
comorb = pd.DataFrame(df_comorbidades.groupby("CD_PACIENTE")["COMORBIDADES"].count())
df_reinternacao = pd.merge(df_reinternacao, comorb, on='CD_PACIENTE')

comorb = df_reinternacao['COMORBIDADES']

st.markdown('# Análise de Comorbidades')
st.markdown('''Aqui foi realizado uma análise prévia das comorbidades dos pacientes, onde foi calculado o máximo de comorbidades em um paciente, a media e a mediana do conjunto de dados. Além disso, foi listado os Top 10 pacientes com mais comorbidades e os Top 10 pacientes com mais internações. Por fim, foram analisadas algumas correlações entre os cojunto de dados''')
col1, col2, col3 = st.columns(3)
col1.metric(label="Máximo", value=comorb.max())
col1.metric(label="Média", value=comorb.mean().round(2))
col1.metric(label="Mediana", value=comorb.median())
col1.metric(label="Desvio Padrão", value=comorb.std().__round__(2))
col2.dataframe(df_reinternacao.sort_values(by=['COMORBIDADES'], ascending=False).iloc[:, [5, 8]].head(10))

int_comorb = df_reinternacao.sort_values(by=['TOTAL_INTERNACOES'], ascending=False).iloc[:, [5, 8]]
col3.dataframe(int_comorb.head(10))

int_comorb = df_reinternacao.groupby("COMORBIDADES")["TOTAL_INTERNACOES"].sum()

st.subheader('Quantidade de Comorbidades por N° de Internações')
st.bar_chart(int_comorb)

idade_comorb = df_reinternacao.groupby("IDADE")["COMORBIDADES"].sum()
st.subheader('Quantidade de Comorbidades por Idade')
st.bar_chart(idade_comorb)

col1, col2 = st.columns(2)

# Comorbidades mais frequentes 
col1.subheader('Comorbidades mais frequentes')
internacao = df_reinternacao["REINTERNADO"]
df_comorbidades = pd.merge(df_comorbidades, internacao, on='CD_PACIENTE')
freq_comorb = df_comorbidades.groupby("COMORBIDADES")["COMORBIDADES"].count()
col1.dataframe(freq_comorb.sort_values(ascending=False).head(50))

# Reinternações por Comorbidade
col2.subheader('Reinternações por Comorbidade')
col2.dataframe(df_comorbidades.groupby("COMORBIDADES")["REINTERNADO"].sum().sort_values(ascending=False))
