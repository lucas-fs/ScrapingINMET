"""
Autor: Lucas Ferreira da Silva
Email: lferreira@inf.ufsm.br

Descricao: Script para download dos dados referentes a cada estacao metereologica
           e criacao de uma pequena "base de dados" em formato JSON referente a
           todas as estacoes

Execucao (comando): python3 geraBase.py

Saida: Arquivo JSON (estacoes.json) contendo dados de todas as estacoes
       metereologicas do INMET

"""
import requests
import json
import bs4
import re

# URL base para Scraping das estacoes
url_map = "http://www.inmet.gov.br/sonabra/maps/pg_mapa.php"

res = requests.get (url_map)
res.raise_for_status()

# Separacao das estacoes
list_markers = (res.text).split("//************* ESTACÃO ")
del list_markers[0]

# Inicializacao da lista de dados das estacoes para posterior tratamento
list_stations = []

# Scraping dos dados mais brutos de cada estacao
for i in list_markers:
    st = (i.split("var imagem",maxsplit=1))[0].split("var ")

    # Capturar id da estação
    station_id = str((st[0].split(maxsplit=1))[0])

    # Capturar label da estacao
    station_label = re.search(r"(?<=')[^']+(?=')", str(st[-1])).group(0)

    # Capturar html da estacao
    station_html = str(st[2].split("html = ", maxsplit=1)[1])

    # Criacao de dicionario auxiliar de dados de cada estacao
    station_info = {}
    station_info['id'] = station_id
    station_info['label'] = station_label
    station_info['html'] = station_html

    list_stations.append(station_info)

# Inicializacao do dicionario de estacoes
stations = {}

# Scraping refinado dos dados de cada estacao
for x in list_stations:
    soup = bs4.BeautifulSoup(x['html'], 'html.parser')

    # Captura o link da tabela de dados
    link = ""
    for a in soup.find_all('a'):
        l = a.get('href')
        if (l.find("pg_dspDadosCodigo_sim.php?", 32) != -1):
            link = l
            break

    aux = (x['html'].split("<b><b>", maxsplit=1))[1].split("<table ", maxsplit=1)

    # Captura lista dos dados geograficos
    localization = ((aux[1].split("</table>", maxsplit=1))[1].split("</font>", maxsplit=1)[0]).split("<br>")

    # Captura demais dados da estacao
    data_aux = ((aux[0].replace("<b>", "")).replace("</b>","")).split("<br>")
    data = []

    for d in data_aux:
        if (d.find("<a ", 0, 4) == -1) and (d.find("</a>", 0, 4) == -1) and (len(d) > 0):
            data.append(d)

    # Criacao do objeto estacao para o JSON
    station_data = {}
    details = {}

    details['estacao'] = data[0].split(": ")[1]
    details['codigo_omm'] = data[1].split(": ")[1]

    if (len(data) > 2):
        details['registro'] = data[2].split(": ")[1]
        details['temp_max'] = (data[3].split(": ")[1]).replace("º","")
        details['temp_min'] = (data[4].split(": ")[1]).replace("º","")
        details['umidade'] = data[5].split(": ")[1]
        details['pressao'] = data[6].split(": ")[1]
        details['precipitacao'] = data[7].split(": ")[1]
        details['vento_dir'] = (data[8].split(": ")[1]).replace("º","graus")
        details['vento_vel'] = data[9].split(": ")[1]

    station_data['label'] = x['label']
    station_data['url'] = link
    station_data['latitude'] = (localization[1].split(": ")[1]).replace("º","")
    station_data['longitude'] = (localization[2].split(": ")[1]).replace("º","")
    station_data['altitude'] = localization[3].split(": ")[1]
    station_data['abertura'] = localization[0].split(": ")[1]
    station_data['detalhes'] = details

    stations[str(x['id'])] = station_data

# Escrita dos dados em arquivo JSON
with open('estacoes.json', 'w') as fp:
    json.dump(stations, fp, indent=4, ensure_ascii=False, sort_keys=True)

print("Database successfully generated!")
