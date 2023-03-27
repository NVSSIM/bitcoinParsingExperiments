import sys
import json
import socket
import time
from bitcoinrpc.authproxy import AuthServiceProxy
import datetime

def get_block_hash_with_retry(p, block_number, retries=3, delay=5):
    for i in range(retries):
        try:
            return p.getblockhash(block_number)
        except socket.timeout:
            if i < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise

def get_block_with_retry(p, block_hash, retries=3, delay=5):
    for i in range(retries):
        try:
            return p.getblock(block_hash)
        except socket.timeout:
            if i < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise

def main():
    # Define your RPC credentials here
    rpc_user = 'user'
    rpc_password = 'user6'

    if rpc_user is None or rpc_password is None:
        print("Error: rpcuser and/or rpcpassword are not set.")
        sys.exit(1)

    # Create a proxy to interact with the Bitcoin Core daemon
    rpc_url = f'http://{rpc_user}:{rpc_password}@127.0.0.1:8332'
    p = AuthServiceProxy(rpc_url, timeout=60)

    # Get the total number of blocks
    block_count = p.getblockcount()

    # Get the list of created wallets
    wallets = p.listwallets()

    # Create a dictionary to store monthly info
    monthly_info = {}

    # Initialize the current year
    current_year = None

    # Iterate through all blocks
    for block_number in range(block_count + 1):
        # Get the block hash with retries
        block_hash = get_block_hash_with_retry(p, block_number)

        # Get the block data with retries
        block = get_block_with_retry(p, block_hash)

        # Get the block date and time
        block_timestamp = block['time']
        block_date = datetime.datetime.fromtimestamp(block_timestamp)

        # Get the block month and year
        block_month = block_date.strftime('%Y-%m')
        block_year = block_date.year

        # Count the number of transactions
        num_transactions = len(block['tx'])

        # Add the info to the monthly dictionary
        if block_month in monthly_info:
            monthly_info[block_month]['num_transactions'] += num_transactions
        else:
            monthly_info[block_month] = {
                'num_transactions': num_transactions
            }

        # Check if we have finished a year
        if current_year is None or block_year != current_year:
            current_year = block_year
            print(f"Finished for year {current_year}.")

    # Add the number of created wallets to the monthly dictionary
    for month in monthly_info:
        monthly_info[month]['num_wallets'] = len(wallets)

    # Save the data to a JSON file
    with open('monthly_info.json', 'w') as outfile:
        json.dump(monthly_info, outfile, indent=4)

    print("Finished.")

if __name__ == "__main__":
    main()