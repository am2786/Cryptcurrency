from blockchain_transaction import *

boss_address = "0x9b1a8ed0bec6DF90087EbfD8a3927aB216A5a0ec" # wallet address of the boss
employee_address = "0x07068BD85E6939c8070C71D23b4D7608660D2BF4" # wallet address of the employee
amount = 5  # amount to be sent in eth
boss_private_key = "bffbce34ab40d71bbb8d559e881bef60ab16b33b63afe51728ad08818cf3bc02" # private key for the boss who is funding the transaction
ganache_url = "http://127.0.0.1:7545"

txn_output = send_transaction(boss_address, employee_address, amount, boss_private_key, ganache_url)
