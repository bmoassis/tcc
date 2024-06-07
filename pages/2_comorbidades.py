import streamlit as st
import pandas as pd

df_atendimentos = st.session_state['dados']['df_atendimentos']
df_pacientes = st.session_state['dados']['df_pacientes']
df_comorbidades = st.session_state['dados']['df_comorbidades']

# Filtros Sidebar
situacao_pac = pd.DataFrame(df_pacientes["SITUACAO"].value_counts().index)
situacao_pac = st.sidebar.selectbox("SITUACAO", situacao_pac)

# Atendimentos: Tabelas importantes
# N° Pacientes
num_pac = df_pacientes[(df_pacientes["SITUACAO"] == situacao_pac)]

# Qtd Pacientes x Comorbidades
comorb = pd.DataFrame(df_comorbidades.groupby("CD_PACIENTE")["COMORBIDADES"].count())
num_pac = pd.merge(num_pac, comorb, on='CD_PACIENTE')

comorb = num_pac['COMORBIDADES']

st.markdown('# Análise de Comorbidades')
st.markdown('''Aqui foi realizado uma análise prévia das comorbidades dos pacientes, onde foi calculado o máximo de comorbidades em um paciente, a media e a mediana do conjunto de dados. Além disso, foi listado os Top 10 pacientes com mais comorbidades e os Top 10 pacientes com mais internações.''')
col1, col2, col3 = st.columns(3)
col1.metric(label="Máximo", value=comorb.max())
col1.metric(label="Média", value=comorb.mean().round(2))
col1.metric(label="Mediana", value=comorb.median())
col1.metric(label="Desvio Padrão", value=comorb.std().__round__(2))
col2.dataframe(num_pac.sort_values(by=['COMORBIDADES'], ascending=False).iloc[:, [5, 7]].head(10))

df_pacientes = pd.merge(df_pacientes, comorb, on='CD_PACIENTE')
int_comorb = df_pacientes.sort_values(by=['TOTAL_INTERNACOES'], ascending=False).iloc[:, [5, 7]]
col3.dataframe(int_comorb.head(10))

st.subheader('Quantidade de Comorbidades por N° de Internações')
st.scatter_chart(x='TOTAL_INTERNACOES', y='COMORBIDADES', data=int_comorb)
st.subheader('Quantidade de Internações por N° de Comorbidades')
st.scatter_chart(x='COMORBIDADES', y='TOTAL_INTERNACOES', data=int_comorb)