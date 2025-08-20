#code based on will assad on youtube
from hashlib import sha256
import ecdsa, json

def updateHash(*args):
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text += json.dumps(arg, sort_keys=True)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

def safe_default(o):
    if isinstance(o, bytes):
        return o.hex()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

def updateHash(*args):
    hashing_text = ""
    h = sha256()
   
    for arg in args:
        hashing_text += json.dumps(arg, sort_keys=True, default=safe_default)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Wallet():
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        pub_key_bytes = self.public_key.to_string()
        return sha256(pub_key_bytes).hexdigest()

    def sign(self, message):
        message_bytes = str(message).encode('utf-8')
        return self.private_key.sign(message_bytes)
    

class Block():
    def __init__(self, data, prev_hash="0" * 64, number=0):
        self.data = data
        self.number = number
        self.prev_hash = prev_hash
        self.nonce = 0

    def hash(self):
       return updateHash(
            self.prev_hash, 
            self.number, 
            self.data, 
            self.nonce
        )

    def add_entry(self, transaction):
       self.data.append(transaction)

    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.prev_hash,
            json.dumps(self.data, indent=4, default=safe_default),
            self.nonce
        )) 


class Blockchain():
    difficulty = 4
    reward = 100
    
    def __init__(self):
        self.chain = []
        self.pending = []

    def add_block(self, block):
        self.chain.append(block)

    def add_transaction(self, sender, reciever, amount, signature):
        transaction = [sender, reciever, amount, signature]
        self.pending.append(transaction)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if len(transaction) == 4:
                    if address == transaction[0]: # Sender
                        balance -= transaction[2]
                    if address == transaction[1]: # Recipient
                        balance += transaction[2]
                elif len(transaction) == 3 and transaction[0] == "Network":
                    if address == transaction[1]: # Recipient
                        balance += transaction[2]
        return balance 
    
    def mine(self, miner_address):
        reward_transaction = ["Network", miner_address, self.reward]

        block_data = [reward_transaction] + self.pending
        self.pending = []

        try:
            last_hash = self.chain[-1].hash()
            block_number = self.chain[-1].number + 1
        except IndexError:
            last_hash = "0" * 64
            block_number = 0

        new_block = Block(number=block_number, prev_hash=last_hash, data=block_data)

        while True:
            if new_block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add_block(new_block)
                break
            else:
                new_block.nonce += 1

        print(f"Block #{new_block.number} mined by address starting with: {miner_address[:10]}...")

        
def main():
    """
    A corrected main function to demonstrate the blockchain in action.
    """
    # Create wallets for our users
    alice_wallet = Wallet()
    bob_wallet = Wallet()

    # Create the blockchain
    blockchain = Blockchain()

    # --- Round 1: Mine the Genesis Block ---
    print("Mining Genesis Block...")
    blockchain.mine(alice_wallet.address)
    print("-" * 30)

    # --- Round 2: Alice sends Bob 50 coins ---
    print(f"Alice's address: {alice_wallet.address}")
    print(f"Bob's address:   {bob_wallet.address}")
    print("\nAlice is sending 50 coins to Bob...")
    
    # The message to be signed
    message_to_sign = {'sender': alice_wallet.address, 'recipient': bob_wallet.address, 'amount': 50}
    signature = alice_wallet.sign(message_to_sign)
    
    # Add the transaction to the pending pool
    blockchain.add_transaction(alice_wallet.address, bob_wallet.address, 50, signature)
    
    # Mine a new block to confirm the transaction
    print("\nMining next block...")
    blockchain.mine(bob_wallet.address) # Bob mines this block
    print("-" * 30)
    
    # --- Final Balances ---
    print("Final Balances:")
    print(f"Alice's balance: {blockchain.get_balance(alice_wallet.address)}")
    print(f"Bob's balance:   {blockchain.get_balance(bob_wallet.address)}")
    print("-" * 30)

    # --- Print the full chain ---
    print("Full Blockchain:")
    for block in blockchain.chain:
        print(block)
        print("-" * 20)

if __name__ == "__main__":
    main()
