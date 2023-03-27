import sys
import json
from bitcoinrpc.authproxy import AuthServiceProxy
import datetime

def main():
    # Définissez vos identifiants RPC ici
    rpc_user = 'user'
    rpc_password = 'user6'

    if rpc_user is None or rpc_password is None:
        print("Erreur : rpcuser et/ou rpcpassword ne sont pas définis.")
        sys.exit(1)

    # Créez un proxy pour interagir avec le démon Bitcoin Core
    rpc_url = f'http://user:user6@127.0.0.1:8332'
    p = AuthServiceProxy(rpc_url)

    # Obtenez le nombre total de blocs
    block_count = p.getblockcount()

    # Créez un dictionnaire pour stocker les informations de chaque mois
    monthly_info = {}

    # Initialiser l'année en cours
    current_year = None

    # Parcourez tous les blocs
    for block_number in range(block_count + 1):
        # Obtenez le hash du bloc
        block_hash = p.getblockhash(block_number)

        # Obtenez les données du bloc
        block = p.getblock(block_hash)

        # Obtenez la date et l'heure du bloc
        block_timestamp = block['time']
        block_date = datetime.datetime.fromtimestamp(block_timestamp)

        # Obtenez le mois et l'année du bloc
        block_month = block_date.strftime('%Y-%m')
        block_year = block_date.year

        # Comptez le nombre de transactions
        num_transactions = len(block['tx'])

        # Ajouter les informations au dictionnaire mensuel
        if block_month in monthly_info:
            monthly_info[block_month]['num_transactions'] += num_transactions
        else:
            monthly_info[block_month] = {
                'num_transactions': num_transactions
            }

        # Vérifier si nous avons terminé une année
        if current_year is None or block_year != current_year:
            current_year = block_year
            print(f"Terminé pour l'année {current_year}.")

    # Enregistrer les données dans un fichier JSON
    with open('monthly_info.json', 'w') as outfile:
        json.dump(monthly_info, outfile, indent=4)

    print("Terminé.")

if __name__ == "__main__":
    main()




