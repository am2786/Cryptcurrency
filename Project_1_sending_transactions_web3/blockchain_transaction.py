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

