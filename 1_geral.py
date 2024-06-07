import streamlit as st 
import pandas as pd 

# Configurar da estrutura da página
st.set_page_config(
    layout="wide",
    page_title="Dashboard"
)

# Texto explicativo
st.markdown('# Análise de Perfil de Pacientes')
st.divider()
st.markdown('''A base de dados inicial foi dividida em três bases: Atendimentos, Pacientes e Comorbidades. Essa parte é dedicada a uma análise do perfil dos pacientes atendidos no hospital no período em questão. Desenvolvido por: Bruno Marinho Oliva de Assis''')

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
situacao_pac = pd.DataFrame(df_pacientes["SITUACAO"].value_counts().index)
situacao_pac = st.sidebar.selectbox("SITUACAO", situacao_pac)


# Atendimentos: Tabelas importantes
# N° Pacientes
num_pac = df_pacientes[(df_pacientes["SITUACAO"] == situacao_pac)]
metrica_num_pac = num_pac["SITUACAO"].value_counts()
# N° Internações
num_int = num_pac["TOTAL_INTERNACOES"].sum()
int_por_pac = num_int/metrica_num_pac
# Print
col1, col2, col3 = st.columns(3)
col1.metric(label="N° Pacientes", value=metrica_num_pac)
col2.metric(label="N° Internações", value=num_int)
col3.metric(label="N° Internações médio por paciente", value=round(int_por_pac,2))

# Qtd Pacientes x Grau Ensino
ensino = pd.DataFrame(num_pac.groupby("GRAU_INS")["GRAU_INS"].count())
ensino = ensino.rename(columns={'': 'Ensino', 'GRAU_INS': 'Quantidade'})
st.subheader('N° de Pacientes por Grau de Ensino')
st.bar_chart(ensino)

# Qtd Pacientes x Cidade
cidade = pd.DataFrame(num_pac.groupby("CIDADE")["CIDADE"].count())
cidade = cidade.rename(columns={'': 'Cidade', 'CIDADE': 'Quantidade'})
st.subheader('N° de Pacientes por Cidade')
st.dataframe(cidade.sort_values(by=['Quantidade'], ascending=False))

# Quantidade de pacientes por N° internações
st.subheader('Quantidade de pacientes por N° internações')
internacao = pd.DataFrame(num_pac.groupby("TOTAL_INTERNACOES")["TOTAL_INTERNACOES"].count())
internacao = internacao.rename(columns={'': 'Total de Internações', 'TOTAL_INTERNACOES': 'Quantidade'})
st.bar_chart(internacao)

# Qtd Pacientes x Idade
idade = pd.DataFrame(num_pac.groupby("IDADE")["IDADE"].count())
idade = idade.rename(columns={'': 'Idade', 'IDADE': 'Quantidade'})
# Qtd Pacientes x Total de Internações
total_int = pd.DataFrame(df_pacientes.groupby("TOTAL_INTERNACOES")["TOTAL_INTERNACOES"].count())
total_int = total_int.rename(columns={'': 'Total de Internações', 'TOTAL_INTERNACOES': 'Quantidade'})

st.subheader('Quantidade de Pacientes por Idade')
st.scatter_chart(idade)
st.subheader('Quantidade de Internações por Idade')
st.scatter_chart(pd.DataFrame(num_pac.groupby("IDADE").sum("TOTAL_INTERNACOES")))