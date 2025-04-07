import json
import datetime
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Listas de usuários e IPs para simulação
usuarios = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]
ips = [
    "192.168.1.10", "192.168.1.20", "192.168.1.30", "192.168.1.40", 
    "192.168.1.50", "192.168.1.60", "192.168.1.70", "192.168.1.80"
]

# Gerando 100 logs fictícios com informações aleatórias
logs_ficticios = []

for i in range(100):  # Gerando 100 entradas
    usuario = random.choice(usuarios)
    ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    sucesso = random.choice([True, False])  # Sucesso aleatório (True ou False)
    horario = (datetime.datetime(2025, 3, 19, 10, 0, 0) + datetime.timedelta(minutes=5 * i)).isoformat()
    logs_ficticios.append({"usuario": usuario, "horario": horario, "ip": ip, "sucesso": sucesso})

# Função de classificação inicial
def classificacao():
    eventos_classificados = []
    for log in logs_ficticios:
        nivel = "Normal" if log["sucesso"] else "Suspeito"
        eventos_classificados.append({**log, "classificacao": nivel})
    return eventos_classificados

# Criando um DataFrame com os dados
def criar_dataframe():
    eventos_classificados = classificacao()
    df = pd.DataFrame(eventos_classificados)
    
    # Criando colunas de features para ML
    df['horario'] = pd.to_datetime(df['horario']).dt.hour  # Extrair hora
    df['ip_distinto'] = df['ip'].apply(lambda x: len(set(x.split('.'))))  # Número de partes distintas no IP
    df['sucesso'] = df['sucesso'].astype(int)  # Sucesso como 1 ou 0
    df['classificacao'] = df['classificacao'].apply(lambda x: 1 if x == "Normal" else 0)  # 1 para normal, 0 para suspeito
    
    return df

# Função para treinar o modelo
def treinar_modelo(df):
    X = df[['horario', 'ip_distinto', 'sucesso']]
    y = df['classificacao']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print("Relatório de Classificação:\n", classification_report(y_test, y_pred))

    return modelo

# Função para prever uma lista de logins
def prever_logins(modelo, logs):
    log_df = pd.DataFrame(logs)  # Criando DataFrame com todos os logs

    # Processamento das features
    log_df['horario'] = pd.to_datetime(log_df['horario']).dt.hour
    log_df['ip_distinto'] = log_df['ip'].apply(lambda x: len(set(x.split('.'))))
    log_df['sucesso'] = log_df['sucesso'].astype(int)

    # Fazendo a predição
    predicoes = modelo.predict(log_df[['horario', 'ip_distinto', 'sucesso']])
    
    # Adicionando a classificação aos logs
    log_df['classificacao'] = ["Normal" if p == 1 else "Suspeito" for p in predicoes]

    return log_df.to_dict(orient='records')  # Convertendo DataFrame para lista de dicionários

# Criando o DataFrame com os logs
df = criar_dataframe()

# Treinando o modelo de ML
modelo_ml = treinar_modelo(df)

# Prevendo a classificação para todos os logins fictícios
resultados = prever_logins(modelo_ml, logs_ficticios)

# Exibindo os resultados
print("Resultado da Simulação para Todos os Logins:")
print(json.dumps(resultados, default=str, indent=4))


# Criar DataFrame com os resultados
df_resultados = pd.DataFrame(resultados)

# Salvar em um arquivo Excel
df_resultados.to_excel("logins_classificados.xlsx", index=False)

print("Arquivo Excel 'logins_classificados.xlsx' salvo com sucesso!")



