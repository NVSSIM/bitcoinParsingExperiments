import sys
import json
import time
from bitcoinrpc.authproxy import AuthServiceProxy

def progress_bar(current, total, bar_length=20):
    progress = float(current) / float(total)
    arrow = '=' * int(progress * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write('\r[{0}] {1}%'.format(arrow + spaces, int(progress * 100)))
    sys.stdout.flush()

def jumping_rabbit(current, total):
    rabbit_frames = ['  (\(\ ', '  (-.-)', '   o_(")(")', '   (_")(")']
    progress = float(current) / float(total)
    rabbit_index = int(progress * (len(rabbit_frames) - 1))
    return rabbit_frames[rabbit_index]

def main():
    rpc_user = 'user'
    rpc_password = 'user6'

    if rpc_user is None or rpc_password is None:
        print("Erreur : rpcuser et/ou rpcpassword ne sont pas définis.")
        sys.exit(1)

    rpc_url = f'http://user:user6@127.0.0.1:8332'
    p = AuthServiceProxy(rpc_url)

    block_count = p.getblockcount()
    result = {}

    for block_number in range(block_count + 1):
        block_hash = p.getblockhash(block_number)
        block = p.getblock(block_hash)
        num_transactions = len(block['tx'])
        block_time = block['time']

        result[block_number] = {'num_transactions': num_transactions, 'block_time': block_time}
        progress_bar(block_number, block_count)
        sys.stdout.write(jumping_rabbit(block_number, block_count))
        sys.stdout.flush()

    with open('block_data.json', 'w') as f:
        json.dump(result, f)

    print("\n\nLes données ont été enregistrées dans block_data.json")

if __name__ == "__main__":
    main()