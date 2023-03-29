import requests
import json
import datetime

# Endpoint de l'API Blockchain.com pour récupérer les statistiques sur les frais de transaction
url = "https://api.blockchain.info/charts/fees-usd-per-transaction?timespan=all&sampled=true&metadata=false&daysAverageString=1d&cors=true&format=json"

# Envoie une requête GET à l'API Blockchain.com
response = requests.get(url)

# Convertit la réponse en format JSON
data = response.json()

# Récupère les données sur les frais de transaction par mois/année
fees_data = data['values']
fees_by_year = {}
fees_count_by_year = {}
for item in fees_data:

    timestamp = datetime.datetime.fromtimestamp(item['x'])
    year = timestamp.strftime('%Y') # convertit la valeur en chaîne de caractères avant de la découper
    fee = item['y']
    print(year)
    print(fee)

    if year in fees_by_year:
        fees_by_year[year] += fee
        fees_count_by_year[year] += 1
    else:
        fees_by_year[year] = fee
        fees_count_by_year[year] = 1

# Calcule les frais de transaction moyens par année
fees_avg_by_year = {}
for year in fees_by_year:
    fees_avg_by_year[year] = fees_by_year[year] / fees_count_by_year[year]

# Crée un dictionnaire contenant les frais de transaction moyens par année
result = fees_avg_by_year

# Écrit les données dans un fichier JSON
with open('fees_data.json', 'w') as f:
    json.dump(result, f)