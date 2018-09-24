
"""
Autor: Lucas Ferreira da Silva
Email: lferreira@inf.ufsm.br

Descricao: Script para download dos dados das estacoes metereologicas do INMET
           de uma data inicial até uma data final

Execucao (comando): python3 capturaDados.py

Entrada: O script usa como entrada o arquivo "entrada.txt" que contem todas as
         estacoes das quais se deseja extrair os dados

Saida: Arquivos .csv de cada estacao referentes as tabelas de dados do periodo
       fornecido

"""
import requests
import base64
import json
import bs4
import csv
import os

# Funcao responsavel por capturar o numero codificado do captive
def getImgNumber(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    
    hidden_tags = soup.find_all("input", type="hidden")

    
    return [(soup.img.get("src")).split("imgNum=", maxsplit=1)[1],
            (str(hidden_tags[0]).split("value=", maxsplit=1)[1][1:-3]),
            (str(hidden_tags[1]).split("value=", maxsplit=1)[1][1:-3]),
            (str(hidden_tags[2]).split("value=", maxsplit=1)[1][1:-3])]

# Funcao responsavel por retornar o numero do captive decodificado
def decodeNumber(num):
    return str(base64.b64decode(num), 'utf-8')

# Funcao responsavel por capturar os dados da tabela gerada
#  pela pagina da estacao e transformar em arquivo CSV
def generateCSV(html, station):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Definicao do cabecaclho do csv
    csv_head  = ["data", "hora", "temp_inst", "temp_max", "temp_min", "umid_inst",
    "umid_max", "umid_min", "pto_orvalho_inst", "pto_orvalho_max", "pto_orvalho_min",
    "pressao", "pressao_max", "pressao_min", "vento_direcao", "vento_vel",
    "vento_rajada", "radiacao", "precipitacao"]

    #table_head = soup.find("thead")
    table_body = soup.find("tbody")

    rows = table_body.find_all('tr')
    csv_body = []
    for row in rows:
    	csv_line = []
    	cols = row.find_all('td')
    	for data in cols:
            # Captura o dado de cada celula
            dt = (str(data).split("<span class=\"texto\">", maxsplit=1)[1]).split("</span>", maxsplit=1)[0]

            # Subtiitui as barras de auxencia de dados por uma celula do csv vazia
            if "////" in dt:
                dt = ""
            csv_line.append(dt)
    	csv_body.append(csv_line)

    csv_name = os.path.join("Tabelas", station + ".csv")
    # Escreve dados no arquivo csv
    with open(csv_name, 'w') as csvfile:
    	filewriter = csv.writer(csvfile, delimiter=',')
    	filewriter.writerow(csv_head)
    	filewriter.writerows(csv_body)

# Com o tempo, para ser usado na automacao dos boletins, basta migrar a entrada para parametros do script
day_start = int(input("Data de inicio dos dados (DIA ex: 01): "))
month_start = int(input("Data de inicio dos dados (MÊS ex: 01): "))
year_start = int(input("Data de inicio dos dados (ANO ex: 2017): "))

# String com a data de inicio no formato dd/mm/yyyy
date_start = str(day_start)+"/"+str(month_start)+"/"+str(year_start)

day_end = int(input("\nData final dos dados (DIA ex: 01): "))
month_end = int(input("Data final dos dados (MÊS ex: 01): "))
year_end = int(input("Data final dos dados (ANO ex: 2017): "))

# String com a data de fim no formato dd/mm/yyyy
date_end = str(day_end)+"/"+str(month_end)+"/"+str(year_end)

# Carrega dados das estacoes a partir da base
with open('estacoes.json') as stations_file:
    data = json.load(stations_file)

# Carrega todas as estacoes que se deseja fazer o download dos dados
with open('entrada.txt') as input_file:
    input_stations =  input_file.readlines()

os.makedirs("Tabelas", exist_ok=True)

# Pega os ids das estacoes
stations_id = []
for s in input_stations:
     stations_id.append((s.split("-")[1])[:-1])

# Realiza as requisicoes para cada pagina
for cod in stations_id:
    url = data[cod]['url']
    station_name = data[cod]['detalhes']['estacao']

    # Prepara um dicionario com os dados para o submmit do   formulario
    form = {}
    form["dtaini"] = date_start
    form["dtafim"] = date_end

    # Cria uma sessao para persistencia de informacoes entre requests
    session = requests.Session()
    r = session.get(url).text
    
    img_number = getImgNumber(r)[0]
    form["aleaValue"] = img_number
    form["xaleaValue"] = getImgNumber(r)[2]
    form["xID"] = getImgNumber(r)[3]
    form["aleaNum"] = decodeNumber(img_number)

    # Recebe o redirecionamento para a tabela de dados da estacao
    res = session.post(url, data=form).text

    # Gera o csv de dados da estacao
    generateCSV(res, station_name)

    print("Station "+ station_name +" download success...")
