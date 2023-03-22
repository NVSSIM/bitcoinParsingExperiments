import sys
import json
from bitcoinrpc.authproxy import AuthServiceProxy

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

    # Créez un dictionnaire pour stocker les informations de chaque bloc
    blocks_info = {}

    # Parcourez tous les blocs
    for block_number in range(block_count + 1):
        # Obtenez le hash du bloc
        block_hash = p.getblockhash(block_number)

        # Obtenez les données du bloc
        block = p.getblock(block_hash)

        # Comptez le nombre de transactions
        num_transactions = len(block['tx'])

        # Stockez les informations dans le dictionnaire
        blocks_info[block_number] = {
            'num_transactions': num_transactions,
            'time': block['time']
        }

        # Enregistrez les données dans un fichier JSON
        with open('block_info.json', 'w') as outfile:
            json.dump(blocks_info, outfile, indent=4)

        # Imprimez l'état actuel
        print(f"Bloc {block_number} traité.")

if __name__ == "__main__":
    main()


