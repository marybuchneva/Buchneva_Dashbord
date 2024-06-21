import pandas as pd
import openpyxl
import json

df_Employment_MSP = pd.read_excel('data/Занятость_МСП_обработанные_данные.xlsx', engine='openpyxl')
df_Employment_MSP_districts = pd.read_excel('data/Занятость_МСП_округа_обработанные_данные.xlsx', engine='openpyxl')
all_districts=df_Employment_MSP['Округ'].unique()
all_central_regions=df_Employment_MSP[(df_Employment_MSP['Округ'] =='Центральный федеральный округ')]
all_central_regions_unique = all_central_regions['Субъект'].unique()

df_Employment=pd.read_excel('data/Занятость_обработанные_данные.xlsx', engine='openpyxl')
df_Employment_district=pd.read_excel('data/Занятость_округа_обработанные_данные.xlsx', engine='openpyxl')
age_types=df_Employment['Возраст'].unique()

df_Unemployment=pd.read_excel('data/Безработица_обработанные_данные.xlsx', engine='openpyxl')
df_Unemployment_district=pd.read_excel('data/Безработица_округа_обработанные_данные.xlsx', engine='openpyxl')

df_Population=pd.read_excel('data/Численность_обработанные_данные.xlsx', engine='openpyxl')
df_Population_district=pd.read_excel('data/Численность_округа_обработанные_данные.xlsx', engine='openpyxl')
Population_types=df_Population_district['Вид'].unique()

with open('data/russia copy.geojson', 'r', encoding='UTF-8') as response:
   counties = json.loads(response.read())
