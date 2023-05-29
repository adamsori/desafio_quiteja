import csv
import zipfile
from datetime import datetime

# 1. Descompactar o arquivo dados.zip no mesmo diretório
with zipfile.ZipFile('dados.zip', 'r') as zip_reference:
    zip_reference.extractall()

# 2. Ler os arquivos descompactados (origem-dados.csv e tipos.csv)
origem_dados = []
with open('origem-dados.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    origem_dados = list(csv_reader)


tipos = {}
with open('tipos.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        tipos[row['id']] = row['nome']


# 3. Filtrar dados identificados como "CRITICO" na coluna status do arquivo origem-dados.csv
dados_criticos = [row for row in origem_dados if row['status'] == 'CRITICO']


# 4. Ordenar pelo campo created_at as informações filtradas
dados_criticos = sorted(dados_criticos, key=lambda x: datetime.strptime(
    x['created_at'], '%Y-%m-%d %H:%M:%S'))

# 5. Incluir novo campo "nome_tipo" baseado nos dados carregados do arquivo tipos.csv
for row in dados_criticos:
    row['nome_tipo'] = tipos.get(row['tipo'], '')

# 6. Gerar arquivo insert-dados.sql com os inserts (SQL) dos dados filtrados
with open('insert-dados.sql', 'w') as file:
    for row in dados_criticos:
        values = ', '.join([f"'{v}'" for v in row.values()])
        file.write(
            f"INSERT INTO dados_finais ({', '.join(row.keys())}) VALUES ({values});\n")

# 7. Montar query para retornar a quantidade de itens por dia agrupados pelo tipo
query = "SELECT DATE(created_at) AS data, nome_tipo, COUNT(*) AS quantidade " \
        "FROM dados_finais " \
        "GROUP BY DATE(created_at), nome_tipo;"

print(query)
