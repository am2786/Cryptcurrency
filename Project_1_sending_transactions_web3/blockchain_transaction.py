from web3 import Web3
import json

def send_transaction(sender_address, reciever_address, amount, sender_private_key, blockchain_url):

    """
    sender_address: (str) wallet address sending funds
    reciever_address: (str) wallet address recieveing funds
    amount: (int, float) amount to be sent in (in eth)
    sender_private_key: (str) private key for the wallet sending funds
    blockchain_url: (str) websocket url to connect to the blockchain
    """

    print ("Transaction Underway! \nEstablishing blockchain connection...")

    # make sure you are connected to blockchain
    web3 = Web3(Web3.HTTPProvider(blockchain_url))
    assert web3.isConnected(), f"Blockchain is not connected. Make sure the url is correct"

    # check that sender has enough eth to send 
    sender_balance = web3.fromWei(web3.eth.getBalance(sender_address), 'ether')
    assert sender_balance > amount, f"Insufficient funds. Wallet only has {sender_balance} eth."
    
    # making transaction
    sender_nonce = web3.eth.getTransactionCount(sender_address)
    value = web3.toWei(amount, 'ether')
    txn = {
            'nonce': sender_nonce, 
            'to': reciever_address, 
            'value': value, 
            'gas': 1000000, 
            'gasPrice': web3.toWei(50, 'gwei')
    }
    
    # signing transaction
    txn_signature = web3.eth.account.signTransaction(txn, sender_private_key)

    # sending transaction, then waiting for completion before checking sender wallet balance
    txn_hash = web3.eth.sendRawTransaction(txn_signature.rawTransaction)
    web3.eth.waitForTransactionReceipt(txn_hash)

    # new balance of sender's wallet (in eth)
    sender_updated_balance = web3.fromWei(web3.eth.getBalance(sender_address), 'ether')

    print ("Transaction Complete!")
    print (f"sender new balance = {round(float(sender_updated_balance), 2)} eth")
    
    return({'sender': sender_address, 
            'receiver': reciever_address, 
            'eth amount': amount, 
            'sender new balance':sender_updated_balance, 
            'transaction hash': txn_hash})

boss_address = "0x9b1a8ed0bec6DF90087EbfD8a3927aB216A5a0ec" # wallet address of the boss
employee_address = "0x07068BD85E6939c8070C71D23b4D7608660D2BF4" # wallet address of the employee
amount = 5  # amount to be sent in eth
boss_private_key = "bffbce34ab40d71bbb8d559e881bef60ab16b33b63afe51728ad08818cf3bc02" # private key for the boss who is funding the transaction
ganache_url = "http://127.0.0.1:7545"

txn_output = send_transaction(boss_address, employee_address, amount, boss_private_key, ganache_url)

