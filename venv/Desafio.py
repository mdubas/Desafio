import pandas as pd
from zipfile import ZipFile
from datetime import datetime

#1 Descompactando arquivo zip com a lib ZipFile
def Descompartar():
    with ZipFile('dados.zip','r') as zip:
        zip.extractall()
        zip.close()
Descompartar()

#2 Lendo ambos os arquivos com a lib pandas
df_dados = pd.read_csv('origem-dados.csv')
df_tipos = pd.read_csv('tipos.csv')

#3 Mapeamento dos valores do Tipo (de acordo com a documentação Pandas)
mapeamento = df_tipos.set_index('id')['nome'].to_dict()

#3.1 Adição do campo: nome_tipo no DataFrame dados
df_dados['nome_tipo'] = df_dados['tipo'].map(mapeamento)

#4 Filtro dos arquivos de dados e sort by data de criação
filtro = df_dados[df_dados.status == 'CRITICO'].sort_values('created_at')

#5 Gera um arquivo (insert-dados.sql)
with open('insert-dados.sql', 'w') as file:
    for _, row in filtro.iterrows():
        values = row.values.tolist()
        values = [f"'{value}'" if isinstance(value, str) else str(value) for value in values]  # Adiciona aspas a todos os campos string
        sql = f"INSERT INTO dados_finais VALUES ({', '.join(map(str, values))});\n"
        file.write(sql)

#6 Query de quantidade de itens agrupados por tipo /com pandas
filtro['created_at'] = pd.to_datetime(filtro['created_at']) #convertendo para tipo data
filtro['created_at'] = filtro['created_at'].dt.strftime('%Y-%m-%d')

query = filtro.groupby(['created_at', 'nome_tipo']).size().reset_index(name='quantidade')
print(query)