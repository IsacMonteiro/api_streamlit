#Importando bibliotecas
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sqlite3
import pandas as pd

default_args = {'owner': 'airflow'}



#Paths

#Path pasta data linux
path = "/home/isac/Documentos/api_streamlit/data"

#Path db
path_db_student = path + "/StudentsPerformance.db"

#Path db tratado
path_db_datawharehouse = path + "/StudentsPerformance_dw.db"

#Path csv
path_temp_csv = path + "/StudentsPerformance.csv"


dag = DAG(dag_id='data_pipeline',  default_args=default_args, schedule_interval='@daily', start_date=days_ago(0),)


def _extract():

    #Conectando a base de dados de produção.
    connect_db_StudentsPerformance = sqlite3.connect(path_db_student)

    #Selecionando os dados
    dataset_df = pd.read_sql_query(r"""
        SELECT * FROM Students;
            """, 
        connect_db_StudentsPerformance
        )
    
    #Exportando os dados para a area de stage (arquivo .csv)
    dataset_df.to_csv(path_temp_csv,   index=False)

    #Fechando a conexão com o banco de dados.
    connect_db_StudentsPerformance.close()


def _transform():
    
    dataset_df = pd.read_csv(path_temp_csv)

    #Transformando os dados dos atributos.
    dataset_df.gender.replace({'female': 0, 'male':1}, inplace=True)
    dataset_df.race_ethnicity.replace({'group A': 0, 'group B': 1, 'group C': 2, 'group D': 3, 'group E': 4 }, inplace=True)
    dataset_df["parental level of education"].replace({"bachelor's degree": 0, 'some college':1,"master's degree":2,"associate's degree":3,'high school':4, 'some high school':5, }, inplace=True)
    dataset_df.lunch.replace({'standard': 0, 'free/reduced':1}, inplace=True)
    dataset_df["test preparation course"].replace({'none': 0, 'completed':1}, inplace=True)


    #Limpando os registros.


    dataset_df.to_csv(path + "//StudentsPerformance.csv",  index=False)



def _load():
    #Conectando com o banco de dados Data Wharehouse.
    connect_db_StudentsPerformance_dw = sqlite3.connect(path_db_datawharehouse)
    
    #Lendo os dados a partir dos arquivos csv.
    dataset_df = pd.read_csv(path_temp_csv)

    #Carregando os dados no banco de dados no arquivo _dw.db.
    dataset_df.to_sql("StudentsPerformance", connect_db_StudentsPerformance_dw, if_exists="replace",index=False)




extract_task = PythonOperator(task_id="extract", python_callable=_extract, dag=dag)

transform_task = PythonOperator(task_id="transform", python_callable=_transform, dag=dag)

load_task = PythonOperator(task_id="load", python_callable=_load, dag=dag)


#ETL 
extract_task >> transform_task >> load_task
