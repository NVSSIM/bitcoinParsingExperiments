import requests
import json
import datetime


import timestamp as timestamp

# Endpoint de l'API Blockchain.com pour récupérer les statistiques sur les transactions
url = "https://api.blockchain.info/charts/n-transactions?timespan=all&format=json"

# Envoie une requête GET à l'API Blockchain.com
response = requests.get(url)

# Convertit la réponse en format JSON
data = response.json()

# Récupère les données sur les transactions par année
transactions_data = data['values']
transactions_by_year = {}
for item in transactions_data:
    timestamp = datetime.datetime.fromtimestamp(item['x'])
    year = timestamp.strftime('%Y') # convertit la valeur en chaîne de caractères avant de la découper
    count = item['y']
    if year in transactions_by_year:
        transactions_by_year[year] += count
    else:
        transactions_by_year[year] = count

# Endpoint de l'API Blockchain.com pour récupérer les statistiques sur les portefeuilles
url = "https://api.blockchain.info/charts/my-wallet-n-users?timespan=all&format=json"

# Envoie une requête GET à l'API Blockchain.com
response = requests.get(url)

# Convertit la réponse en format JSON
data = response.json()

# Récupère les données sur les portefeuilles créés par année
wallets_data = data['values']

wallets_by_year = {}
for item in wallets_data:
    timestamp = datetime.datetime.fromtimestamp(item['x'])
    year = timestamp.strftime('%Y') # convertit la valeur en chaîne de caractères avant de la découper
    count = item['y']
    if year in wallets_by_year:
        wallets_by_year[year] += count
    else:
        wallets_by_year[year] = count

# Combine les données sur les transactions et les portefeuilles créés par année
result = {}
for year in sorted(set(transactions_by_year.keys()) | set(wallets_by_year.keys())):
    result[year] = {
        "transactions": transactions_by_year.get(year, 0),
        "wallets_created": wallets_by_year.get(year, 0)
    }

# Écrit les données dans un fichier JSON
with open('wallets_created.json', 'w') as f:
    json.dump(result, f)