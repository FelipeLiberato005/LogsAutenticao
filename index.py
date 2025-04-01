import json
import datetime
import random
from collections import defaultdict
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

# Função de classificação
def classificacao():
    eventos_classificados = []
    for log in logs_ficticios:
        # Classificando como Normal ou Suspeito com base no sucesso
        if log["sucesso"]:
            nivel = "Normal"
        else:
            nivel = "Suspeito"
        
        eventos_classificados.append({**log, "classificacao": nivel})
    return eventos_classificados

# Criando um DataFrame com os dados
def criar_dataframe():
    eventos_classificados = classificacao()
    df = pd.DataFrame(eventos_classificados)
    
    # Criando colunas de features para ML
    df['horario'] = pd.to_datetime(df['horario']).dt.hour  # Extrair hora
    
    # Calculando o número de partes distintas no IP para análise
    df['ip_distinto'] = df['ip'].apply(lambda x: len(set(x.split('.'))))  # Número de partes distintas no IP
    
    df['sucesso'] = df['sucesso'].astype(int)  # Sucesso como 1 ou 0
    
    # Prevendo se o evento é normal ou suspeito (classificação)
    df['classificacao'] = df['classificacao'].apply(lambda x: 1 if x == "Normal" else 0)  # 1 para normal, 0 para suspeito
    return df

    #FUNÇÃO PARA TREINAR E PREVER USANDO RANDOM FOREST
def treinar_modelo(df):
    # Separando as entrada (X) e os de saida (y)
    X = df[['horario', 'ip_distinto', 'sucesso']]  # São as informações que serão usadas para prever a classificação:


    y = df['classificacao'] # É a classificação esperada (1 para "Normal" e 0 para "Suspeito").

    # Separando em treino e teste
    #train_test_split divide os dados em dois grupos:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #80% dos dados são usados para treinar o modelo
    #20% dos dados são usados para testar o modelo
    #random_state=42 Define uma semente fixa para garantir que a divisão seja reprodutível (o mesmo resultado sempre que o código for executado).

    # Criando o modelo Random Forest Classifie
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    #n_estimators=100 Define que a Random Forest terá 100 árvores de decisão.
    #modelo.fit(X_train, y_train) Treina o modelo com os dados de treinamento

    # Avaliando o modelo
    y_pred = modelo.predict(X_test)  #modelo.predict(X_test) O modelo usa os dados de teste para prever se os logins são "Normais" ou "Suspeitos".
    print(classification_report(y_test, y_pred)) #Compara as previsões (y_pred) com os valores reais (y_test), mostrando métricas como: 
                                                 #Quantos dos classificados como "Normal" realmente eram normais?
                                                 #Quantos dos eventos suspeitos foram corretamente identificados?
    return modelo



# Função para prever novos logs
def prever_login(modelo, log):
    # O log precisa estar em formato de DataFrame para ser processado
    log_df = pd.DataFrame(log)
    
    # Garantir que a hora seja extraída corretamente e a coluna 'ip_distinto' seja calculada
    log_df['horario'] = pd.to_datetime(log_df['horario']).dt.hour
    log_df['ip_distinto'] = log_df['ip'].apply(lambda x: len(set(x.split('.'))))
    log_df['sucesso'] = log_df['sucesso'].astype(int)
    
    # Prevendo a classificação para o novo login
    predicao = modelo.predict(log_df[['horario', 'ip_distinto', 'sucesso']])
    
    # Convertendo a previsão para "Normal" ou "Suspeito"
    classificacao = "Normal" if predicao[0] == 1 else "Suspeito"
    
    # Adicionando a classificação ao log original
    log['classificacao'] = classificacao
    
    # Retornando o log completo com todos os dados
    return log

# Criando o DataFrame com os logs
df = criar_dataframe()

# Treinando o modelo de ML
modelo_ml = treinar_modelo(df)

 #Exemplo de novo login
novo_login = {
    'usuario': ['user1'],
    'horario': ['2025-03-19T10:00:00'],  # 10 AM
    'ip': ['192.168.1.10'],  # IP
'sucesso': [1]  # Sucesso
}

# Prevendo a classificação para o novo login e exibindo todos os dados
resultado = prever_login(modelo_ml, novo_login)
print("Resultado do novo login:")
print(json.dumps(resultado, default=str, indent=4))



