from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
# https://github.com/rssanders3/airflow-zip-operator-plugin
#from airflow.operators.zip_operator_plugin import UnzipOperator
from airflow.utils.dates import days_ago
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,

}

#Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
    'AA_practica_2',
    default_args=default_args,
    description='Grafo de la práctica 2',
    schedule_interval=None,
)
#https://unix.stackexchange.com/questions/318579/delete-folder-if-it-exists/318581
BorraCarpetaSiExiste = BashOperator(
    task_id='BorraCarpetaSiExiste',
    depends_on_past=False,
    bash_command='if [ -d /tmp/p2_gbv/ ]; then rm -rf /tmp/p2_gbv/ ; fi',
    dag=dag,
)

PrepararEntorno = BashOperator(
    task_id='PrepararEntorno',
    depends_on_past=True,
    bash_command='mkdir -p /tmp/p2_gbv/',
    dag=dag,
)

CapturaDatosHumidity = BashOperator(
    task_id='CapturaDatosHumidity',
    depends_on_past=True,
    bash_command='wget https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip -O /tmp/p2_gbv/humidity.zip',
    dag=dag,
)

CapturaDatosTemperature = BashOperator(
    task_id='CapturaDatosTemperature',
    depends_on_past=True,
    bash_command='wget https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip -O /tmp/p2_gbv/temperature.zip',
    dag=dag,
)

DescomprimirHumedad = BashOperator(
    task_id='DescomprimirHumedad',
    depends_on_past=True,
    bash_command='unzip /tmp/p2_gbv/humidity.zip -d /tmp/p2_gbv/v1/Datos',
    dag=dag,
)

DescomprimirTemperatura = BashOperator(
    task_id='DescomprimirTemperatura',
    depends_on_past=True,
    bash_command='unzip /tmp/p2_gbv/temperature.zip -d /tmp/p2_gbv/v1/Datos',
    dag=dag,
)

DescomprimirHumedad2 = BashOperator(
    task_id='DescomprimirHumedad2',
    depends_on_past=True,
    bash_command='unzip /tmp/p2_gbv/humidity.zip -d /tmp/p2_gbv/v2/Datos',
    dag=dag,
)

DescomprimirTemperatura2 = BashOperator(
    task_id='DescomprimirTemperatura2',
    depends_on_past=True,
    bash_command='unzip /tmp/p2_gbv/temperature.zip -d /tmp/p2_gbv/v2/Datos',
    dag=dag,
)

BorrarComprimidos = BashOperator(
    task_id='BorrarComprimidos',
    depends_on_past=True,
    bash_command='rm /tmp/p2_gbv/*.zip',
    dag=dag,
)

ClonarV2 = BashOperator(
    task_id='ClonarV2',
    depends_on_past=True,
    bash_command='git clone https://github.com/guillergood/CC-Repo-V2.git /tmp/p2_gbv/v2',
    dag=dag,
)

ClonarV1 = BashOperator(
    task_id='ClonarV1',
    depends_on_past=True,
    bash_command='git clone https://github.com/guillergood/CC-Repo-V1.git /tmp/p2_gbv/v1',
    dag=dag,
)

PrepareDockerCompose = BashOperator(
    task_id='PrepareDockerCompose',
    depends_on_past=True,
    bash_command='cp /tmp/p2_gbv/v1/docker-compose.yml /tmp/p2_gbv/',
    dag=dag,
)

# https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md y reiniciar para quitar sudo
ComposeUp = BashOperator(
    task_id='ComposeUp',
    depends_on_past=True,
    bash_command='docker-compose -f /tmp/p2_gbv/docker-compose.yml up -d --build',
    dag=dag,
)

CargarDB = BashOperator(
    task_id='CargarDB',
    depends_on_past=True,
    bash_command='cd /tmp/p2_gbv/v1/ && python3 capturaDatos.py',
    dag=dag,
)

CargarDB2 = BashOperator(
    task_id='CargarDB2',
    depends_on_past=True,
    bash_command='cd /tmp/p2_gbv/v2/ && python3 capturaDatos.py',
    dag=dag,
)

CrearModelo = BashOperator(
    task_id='CrearModelo',
    depends_on_past=True,
    bash_command='cd /tmp/p2_gbv/v1/ && python3 crearModelo.py',
    dag=dag,
)

CrearModelo2 = BashOperator(
    task_id='CrearModelo2',
    depends_on_past=True,
    bash_command='cd /tmp/p2_gbv/v2/ && python3 crearModelo.py',
    dag=dag,
)

UnitTestsV2 = BashOperator(
    task_id='UnitTestsV2',
    depends_on_past=True,
    bash_command='cd /tmp/p2_gbv/v2/ && python3 tests.py',
    dag=dag,
)

UnitTestsV1 = BashOperator(
    task_id='UnitTestsV1',
    depends_on_past=True,
    bash_command='cd /tmp/p2_gbv/v1/ && python3 tests.py',
    dag=dag,
)

CrearContenedoresFinales = BashOperator(
    task_id='CrearContenedoresFinales',
    depends_on_past=True,
    bash_command='docker-compose -f /tmp/p2_gbv/docker-compose.yml build',
    dag=dag,
)

#Dependencias - Construcción del grafo DAG
BorraCarpetaSiExiste >> PrepararEntorno
PrepararEntorno >> [CapturaDatosHumidity, CapturaDatosTemperature, ClonarV1, ClonarV2] 
[CapturaDatosHumidity, ClonarV1] >> DescomprimirHumedad
[CapturaDatosTemperature, ClonarV1] >> DescomprimirTemperatura
[CapturaDatosHumidity, ClonarV2] >> DescomprimirHumedad2
[CapturaDatosTemperature, ClonarV2] >> DescomprimirTemperatura2
[DescomprimirHumedad,DescomprimirTemperatura,DescomprimirHumedad2,DescomprimirTemperatura2] >> BorrarComprimidos
[DescomprimirHumedad, DescomprimirTemperatura,DescomprimirHumedad2,DescomprimirTemperatura2, ClonarV1, ClonarV2] >> PrepareDockerCompose
PrepareDockerCompose >> ComposeUp
ComposeUp >> CargarDB
ComposeUp >> CargarDB2
CargarDB >> CrearModelo
CargarDB2 >> CrearModelo2
CrearModelo >> UnitTestsV1
CrearModelo2 >> UnitTestsV2
[UnitTestsV1,UnitTestsV2] >> CrearContenedoresFinales
