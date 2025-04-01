import json
import datetime
import random
import pandas as pd
import re
from tabulate import tabulate
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Listas de usuários e IPs para simulação
usuarios = ["user1", "user2", "user3", "user4", "user5", "admin1", "admin_test", "user8", "user9", "user10"]

# Função para validar o formato do IP
def validar_ip(ip):
    padrao_ip = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    return bool(re.match(padrao_ip, ip))

# Função para identificar padrões suspeitos nos IPs
def ip_suspeito(ip):
    padrao_suspeito = r"(\d{1,3})\.\1\.\1\.\1"  # Padrão "111.111.111.111"
    return bool(re.match(padrao_suspeito, ip))

# Função para identificar usuários suspeitos
def usuario_suspeito(usuario):
    padrao_usuario = r"^admin.*"  # Usuários que começam com "admin"
    return bool(re.match(padrao_usuario, usuario))

# Gerando 100 logs fictícios com informações aleatórias
logs_ficticios = []

for i in range(100):
    usuario = random.choice(usuarios)
    ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    sucesso = random.choice([True, False])
    horario = (datetime.datetime(2025, 3, 19, 10, 0, 0) + datetime.timedelta(minutes=5 * i)).strftime("%H:%M:%S")
    
    # Verificação de IP suspeito ou usuário suspeito
    status_suspeito = not validar_ip(ip) or ip_suspeito(ip) or usuario_suspeito(usuario)
    
    logs_ficticios.append({
        "usuario": usuario,
        "horario": horario,
        "ip": ip,
        "sucesso": sucesso,
        "suspeito_regex": status_suspeito
    })

# Função de classificação inicial
def classificacao():
    eventos_classificados = []
    for log in logs_ficticios:
        nivel = "Normal" if log["sucesso"] and not log["suspeito_regex"] else "Suspeito"
        eventos_classificados.append({**log, "classificacao": nivel})
    return eventos_classificados

# Criando um DataFrame com os dados
def criar_dataframe():
    eventos_classificados = classificacao()
    df = pd.DataFrame(eventos_classificados)
    df['ip_distinto'] = df['ip'].apply(lambda x: len(set(x.split('.'))))
    df['sucesso'] = df['sucesso'].astype(int)
    df['classificacao'] = df['classificacao'].apply(lambda x: 1 if x == "Normal" else 0)
    return df

# Treinar o modelo
def treinar_modelo(df):
    X = df[['ip_distinto', 'sucesso']]
    y = df['classificacao']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    print("Relatório de Classificação:\n", classification_report(y_test, y_pred))
    return modelo

# Prever novos logins
def prever_logins(modelo, logs):
    log_df = pd.DataFrame(logs)
    log_df['ip_distinto'] = log_df['ip'].apply(lambda x: len(set(x.split('.'))))
    log_df['sucesso'] = log_df['sucesso'].astype(int)
    predicoes = modelo.predict(log_df[['ip_distinto', 'sucesso']])
    log_df['classificacao'] = ["Normal" if p == 1 else "Suspeito" for p in predicoes]
    return log_df.to_dict(orient='records')

# Criando DataFrame e treinando o modelo
df = criar_dataframe()
modelo_ml = treinar_modelo(df)

# Prevendo a classificação para todos os logins fictícios
resultados = prever_logins(modelo_ml, logs_ficticios)
print(json.dumps(resultados, default=str, indent=4))

# Exibir tabela com todos os logins
print("\nTabela de Logins:")
print(tabulate(resultados, headers="keys", tablefmt="grid"))

# Salvar os resultados em um Excel
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel("logins_classificados.xlsx", index=False)
print("Arquivo Excel 'logins_classificados.xlsx' salvo com sucesso!")
