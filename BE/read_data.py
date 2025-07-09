import requests
import pandas as pd
import statistics
import math
import json
from io import StringIO

excel_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTPcG07qg-ObrL0eG0cq-8XumKyvoQqYrcznxuFa1ROgT-QJZgBj3keHWiied9ifD3kYJiQf2WGClV1/pub?output=csv'

def read_excel_data(url):
    request_excel = requests.get(url)
    if request_excel.status_code != 200:
        raise Exception(f"❌ Error: Failed to fetch Excel data. Status code: {request_excel.status_code}")
    
    csv_content = StringIO(request_excel.text)
    data_frame = pd.read_csv(csv_content, header=1)
    data_frame = data_frame.dropna(how='all')              # Elimina filas vacías
    data_frame = data_frame.dropna(axis=1, how='all')      # Elimina columnas vacías
    data_frame.dropna(subset=['Nombre'], inplace=True)     # Elimina si 'Nombre' es NaN
    data_frame['Fecha'] = pd.to_datetime(data_frame['Fecha'], format='%d-%m-%y', errors='coerce')
    data_frame['Nota'] = pd.to_numeric(data_frame['Nota'], errors='coerce')
    
    return data_frame


def get_student_assesment_grade(df, name, assessment):
    filtered = df.loc[(df['Nombre'] == name) & (df['Evaluacion'] == assessment)]
    if filtered.empty:
        return json.dumps({"message": "No se encontraron datos."})
    return json.dumps(filtered.to_dict(orient='records'), default=str, indent=2)


def get_student_average(df, name):
    notas = df.loc[df['Nombre'] == name, 'Nota']
    if notas.empty:
        return json.dumps({"message": "No hay notas para este estudiante."})
    promedio = statistics.mean(notas)
    return json.dumps({
        "Nombre": name,
        "PromedioExacto": promedio,
        "PromedioRedondeado": math.trunc(promedio)
    }, indent=2)


def get_student_type_assesment_grade(df, name, tipo):
    filtered = df.loc[(df['Nombre'] == name) & (df['Tipo de Evaluacion'] == tipo)]
    if filtered.empty:
        return json.dumps({"message": "No se encontraron evaluaciones de este tipo para el estudiante."})
    return json.dumps(filtered.to_dict(orient='records'), default=str, indent=2)


def get_general_average(df):
    frontend = df[df['Modulo'] == 'Frontend']
    if frontend.empty:
        return json.dumps({"message": "No hay datos del módulo Frontend."})
    promedio = frontend['Nota'].mean()
    return json.dumps({
        "Modulo": "Frontend",
        "PromedioExacto": promedio,
        "PromedioRedondeado": math.trunc(promedio)
    }, indent=2)


def get_all_student_average(df):
    grouped = df.groupby('Nombre')['Nota'].mean().reset_index()
    if grouped.empty:
        return json.dumps({"message": "No hay datos para calcular promedios."})
    grouped['Nota'] = grouped['Nota'].apply(lambda x: math.trunc(x))
    return json.dumps(grouped.to_dict(orient='records'), indent=2)


def get_all_student_average_sorted(df, ascending=True):
    grouped = df.groupby('Nombre')['Nota'].mean().reset_index().sort_values(by='Nota', ascending=ascending)
    if grouped.empty:
        return json.dumps({"message": "No hay datos para ordenar promedios."})
    grouped['Nota'] = grouped['Nota'].apply(lambda x: math.trunc(x))
    return json.dumps(grouped.to_dict(orient='records'), indent=2)
df = read_excel_data(excel_url)


print(get_student_assesment_grade(df, 'Pepe Viyuela', 'Quiz 2'))
print(get_student_average(df, 'Pepe Viyuela'))
print(get_student_type_assesment_grade(df, 'Pepe Viyuela', 'Quiz'))
print(get_general_average(df))
print(get_all_student_average(df))
print(get_all_student_average_sorted(df, ascending=False))
