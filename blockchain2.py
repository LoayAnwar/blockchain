from hashlib import sha256
import json
import time
from random import random
import copy


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.current_nonce = 0

    def get_length(self):
        return len(self.chain)

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 2

    def proof_of_work(self, block, hash_percentage):
        for i in range(hash_percentage):
            block.nonce = self.current_nonce
            computed_hash = block.compute_hash()
            if computed_hash.startswith('0' * Blockchain.difficulty):
                self.current_nonce = 0
                return computed_hash
            else:
                self.current_nonce += 1

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, hash_percentage):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block, hash_percentage)

        if proof is not None:
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index

    def create_random_transactions(self, n):
        for i in range(n):
            self.add_new_transaction(random()*10)


blockchain_honest = Blockchain()

attack_speed = int(input("Enter the attacker computational power percentage: "))
honest_speed = 100 - attack_speed

# start honest chain
for i in range(3):
    blockchain_honest.create_random_transactions(100)
    break_condition = blockchain_honest.get_length()+1
    while break_condition != blockchain_honest.get_length():
        blockchain_honest.mine(honest_speed)

blockchain_attacker = copy.deepcopy(blockchain_honest)
blockchain_attacker.chain.pop()

while True:
    blockchain_honest.create_random_transactions(100)
    blockchain_attacker.unconfirmed_transactions = copy.deepcopy(blockchain_honest.unconfirmed_transactions)

    if(attack_speed >= honest_speed):
        blockchain_attacker.mine(attack_speed)
        blockchain_honest.mine(honest_speed)
    else:
        blockchain_honest.mine(honest_speed)
        blockchain_attacker.mine(attack_speed)

    if blockchain_attacker.get_length() - blockchain_honest.get_length() >= 5:
        print("Attack succeeded with computing power", attack_speed, "%")
        break