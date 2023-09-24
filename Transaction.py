import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = str(self.index) + self.previous_hash + json.dumps(self.transactions) + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", [], int(time.time()))

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_reward_address):
        block = Block(len(self.chain), self.get_last_block().hash, self.pending_transactions, int(time.time()))
        block = self.proof_of_work(block)
        self.chain.append(block)
        self.pending_transactions = [self.create_transaction(None, miner_reward_address, 10)]  

    def create_transaction(self, sender, recipient, amount):
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        return transaction

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append(self.create_transaction(sender, recipient, amount))

    def proof_of_work(self, block, difficulty=4):
        while block.hash[:difficulty] != '0' * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
