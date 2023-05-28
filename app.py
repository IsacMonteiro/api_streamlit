#Importando bibliotecas.
import pandas as pd
import streamlit as st
#from pycaret.regression import *
import joblib


# Carregando o modelo treinado.
model = joblib.load('model/modelo-final-LR.pkl')


#Carregando uma amostra dos dados.
dataset = pd.read_csv('data/StudentsPerformance.csv') 
#classifier = pickle.load(pickle_in)

#Título
st.title("Data App - Predição de Notas de Matemática")

#Subtítulo
st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learning para o problema de predição de notas de Matemática de alunos.")


st.sidebar.subheader("Defina os atributos do aluno para predição das notas de Matemática")



#Mapeando dados do usuário para cada atributo
gender = st.sidebar.selectbox("Gênero",("Masculino","Feminino"))
preparation_course = st.sidebar.selectbox("Teste de Curso Preparatório",("Completo","Não possui"))


#Transformando o dado de entrada em valor binário
gender = 1 if gender == "Masculino" else 0
preparation_course = 1 if preparation_course == "Completo" else 0



race_ethnicity = st.sidebar.selectbox("Grupos de Cotas",(
                            "Grupo A"
                            ,"Grupo B"
                            ,"Grupo C"
                            ,"Grupo D",
                            "Grupo E"
                            )
                        )


if race_ethnicity == "Grupo A":
    race_ethnicity = 1
if race_ethnicity == "Grupo B":
    race_ethnicity = 2
if race_ethnicity == "Grupo C":
    race_ethnicity = 3
if race_ethnicity == "Grupo D":
    race_ethnicity = 4
if race_ethnicity == "Grupo E":
    race_ethnicity = 5




parental_level_of_education = st.sidebar.selectbox("Nível Educacional de Parentes",(
                            "Bacharelado"
                            ,"Alguma Faculdade"
                            ,"Mestrado"
                            ,"Graduação"
                            ,"Ensino Médio",
                            "Algum Ensino Médio"
                            )
                        )


if parental_level_of_education == "Bacharelado": 
    parental_level_of_education = 1
if parental_level_of_education == "Alguma Faculdade": 
    parental_level_of_education = 2
if parental_level_of_education == "Mestrado": 
    parental_level_of_education = 3
if parental_level_of_education == "Graduação": 
    parental_level_of_education = 4
if parental_level_of_education == "Ensino Médio": 
    parental_level_of_education = 5
if parental_level_of_education == "Algum Ensino Médio": 
    parental_level_of_education = 6



reading_score = st.sidebar.number_input("Notas de Leitura", value=dataset["reading score"].mean())
writing_score = st.sidebar.number_input("Notas de Escrita", value=dataset["writing score"].mean())


#Inserindo um botão na tela
btn_predict = st.sidebar.button("Realizar Predição")


#Verifica se o botão foi acionado
if btn_predict:
    data_teste = pd.DataFrame()

    data_teste["gender"] =	[gender]
    data_teste["race_ethnicity"] = [race_ethnicity]
    data_teste["parental level of education"] =	[parental_level_of_education]    
    data_teste["test preparation course"] =	[preparation_course]
    data_teste["reading score"] = [reading_score]
    data_teste["writing score"] = [writing_score]



    #Imprime os dados de teste    
    print(data_teste)

    #Realiza a predição
    result = model.predict(data_teste)
    
    st.subheader("A nota de matemática prevista para o aluno é:")
    result = str(round(result[0],2))
    
    st.write(result)