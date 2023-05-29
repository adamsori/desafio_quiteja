import csv
import zipfile
from datetime import datetime

# 1. Descompactar o arquivo dados.zip
with zipfile.ZipFile('dados.zip', 'r') as zip_ref:
    zip_ref.extractall()

# 2. Ler o arquivo descompactado (origem-dados.csv)
data = []
with open('origem-dados.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = list(csv_reader)

# 3. Filtrar dados identificados como "CRÍTICO" na coluna status
dados_criticos = [row for row in data if row['status'] == 'CRITICO']

# 4. Ordenar pelo campo created_at
dados_criticos = sorted(dados_criticos, key=lambda x: datetime.strptime(
    x['created_at'], '%Y-%m-%d %H:%M:%S'))

# 5. Ler o arquivo tipos.csv e criar um dicionário com as informações de nome_tipo
tipos = {}
with open('tipos.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        tipos[row['id']] = row['nome']

# 6. Incluir novo campo "nome_tipo" baseado nos dados carregados do arquivo tipos.csv
for row in dados_criticos:
    row['nome_tipo'] = tipos.get(row['tipo'], '')

# 7. Gerar arquivo insert-dados.sql com os inserts (SQL) dos dados filtrados
with open('insert-dados.sql', 'w') as file:
    for row in dados_criticos:
        values = ', '.join([f"'{v}'" for v in row.values()])
        file.write(
            f"INSERT INTO dados_finais ({', '.join(row.keys())}) VALUES ({values});\n")

# 8. Montar query para retornar a quantidade de itens por dia agrupados pelo tipo
count_by_day = {}
for row in dados_criticos:
    created_at = datetime.strptime(
        row['created_at'], '%Y-%m-%d %H:%M:%S').date()
    tipo = row['tipo']
    count_by_day.setdefault(created_at, {}).setdefault(tipo, 0)
    count_by_day[created_at][tipo] += 1

query = ""
for date, counts in count_by_day.items():
    for tipo, count in counts.items():
        query += f"Data: {date}, Tipo: {tipo}, Quantidade: {count}\n"

# 9. Montar  uma sql query para retornar a quantidade de itens por dia agrupados pelo tipo
sql_query = "SELECT DATE(created_at) AS data, nome_tipo, COUNT(*) AS quantidade " \
    "FROM dados_finais " \
    "GROUP BY DATE(created_at), nome_tipo;"


print(f'SQL query para executar no banco de dados:\n\n{sql_query}\n')

print(f'Quantidade de itens agrupados por tipo:\n\n{query}')
