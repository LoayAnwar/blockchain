from hashlib import sha256
import json
import time
import threading
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

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 4

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

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

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index


blockchain = Blockchain()


def change_block(bc, id):
    global blockchain
    if(len(blockchain.chain) + 4 < len(bc.chain)):
        blockchain = copy.deepcopy(bc)
        print(len(bc.chain), id)


class thread(threading.Thread):
    def __init__(self, thread_ID):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
        self.blockchain_local = copy.deepcopy(blockchain)
        self.flag = False

    def run(self):
        while True:
            if len(blockchain.chain) > len(self.blockchain_local.chain):
                self.blockchain_local = copy.deepcopy(blockchain)
            for i in range(100):
                self.blockchain_local.add_new_transaction(i)
            if(self.thread_ID == 2):
                time.sleep(2)
            elif self.flag is False and self.thread_ID == 1:
                self.blockchain_local.chain.pop()
                self.flag = True
            self.blockchain_local.mine()
            change_block(self.blockchain_local, self.thread_ID)


thread1 = thread(1)
thread2 = thread(2)

thread1.start()
thread2.start()
