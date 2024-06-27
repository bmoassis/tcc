import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib as plt 
from graphviz import Source
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz

# Sessions
df_atendimentos = st.session_state['dados']['df_atendimentos']
df_pacientes = st.session_state['dados']['df_pacientes']
df_comorbidades = st.session_state['dados']['df_comorbidades']

# Tratando base de dados
df_pacientes["REINTERNADO"] = df_pacientes["TOTAL_INTERNACOES"] > 1
df_pacientes = pd.get_dummies(df_pacientes, columns=['SITUACAO'], drop_first=True)
comorb = pd.DataFrame(df_comorbidades.groupby("CD_PACIENTE")["COMORBIDADES"].count())
df_final = pd.merge(df_pacientes, comorb, on='CD_PACIENTE')

df_final = df_final.iloc[:, [1, 6 ]]

# Treinando o modelo 
X = df_final.drop('REINTERNADO', axis=1)
y = df_final['REINTERNADO']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.80, random_state=101)

dtree = DecisionTreeClassifier()
dtree.fit(X_train, y_train)

predictions = dtree.predict(X_test)

st.markdown('# Árvore de Decisão')
st.markdown('''Essa seção é destinada para análise da árvore de decisão construída para analisar as reinternações.''')
tree = export_graphviz(dtree)
st.graphviz_chart(tree)

st.markdown('# Classification Report')
st.dataframe(classification_report(y_test, predictions, output_dict=True))
st.markdown('# Confusion Matrix')
st.dataframe(confusion_matrix(y_test, predictions))
