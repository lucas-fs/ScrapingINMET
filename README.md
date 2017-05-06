# Scraping das estações do INMET
Conjunto de Scripts para Web Scraping dos dados das estações metereológicas do INMET.

## Script para captura de dados sobre estações
**Script:** geraBase.py

**Descricao:** Script para download dos dados referentes a cada estação metereológica e criação de uma pequena "base de dados" em formato JSON referente a todas as estações.

**Execução (comando):**
```
python3 geraBase.py
```

**Saída:** Arquivo JSON (estacoes.json) contendo dados de todas as estações metereológicas do INMET.

## Script para captura dos dados metereológicos de cada estação
**Script:** capturaDados.py

**Descricao:** Script para download dos dados das estações metereológicas do INMET de uma data inicial até uma data final.

**Execução (comando):**
```
python3 capturaDados.py
```
**Entrada:** O script usa como entrada o arquivo ["entrada.txt"](/entrada.txt) que contem todas as estações das quais se deseja extrair os dados

**Entrada (usuário):** Ao executar o script é necessário informar as datas de inicio e fim do período que se deseja capturar os dados

**Saída:** Arquivos .csv de cada estação referentes as tabelas de dados do período fornecido. Os arquivos .csv serão gerados dentro da pasta "Tabelas"

## Dependências para a execução
Como  os scripts foram desenvolvidos na linguagem de programação Python 3, é necessário ter o interpretador da linguagem instalado no computador, abaixo o modo de instalação no Windows e Linux Debian ou derivados:

**Windows:** Basta fazer o download em [Python download](https://www.python.org/downloads/windows/) e instalar

**Linux Debian ou derivados:** Provavelmente o Python 3 já estará instalado no sistema, caso não estiver basta executar o comando no terminal:
```
sudo apt-get install python3
```

Biblioteca de scraping para Python 3, modo de instalação abaixo:
```
pip3 install beautifulsoup4
```
