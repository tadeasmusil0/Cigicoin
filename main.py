import hashlib
import json
import os
from time import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

# Model pro data transakce
class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float

# Hlavní logika blockchainu
class Blockchain:
    # Nastavení a načtení dat při startu
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.file_path = 'blockchain.json'
        
        if not self.load_from_file():
            self.create_block(nonce=1, previous_hash='0')

    # Vytvoření bloku a jeho uložení
    def create_block(self, nonce, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.mempool,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        self.mempool = []
        self.chain.append(block)
        self.save_to_file()
        return block

    # Uložení aktuálního stavu do JSONu
    def save_to_file(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.chain, f, indent=4)

    # Načtení historie ze souboru
    def load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.chain = json.load(f)
            return True
        return False

    # Přidání transakce do fronty (mempoolu)
    def add_transaction(self, sender, receiver, amount):
        self.mempool.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.last_block['index'] + 1

    # Pomocná funkce pro získání posledního bloku
    @property
    def last_block(self):
        return self.chain[-1]

    # Výpočet SHA-256 hashe bloku
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Algoritmus Proof of Work (hledání nonce)
    def proof_of_work(self, last_nonce):
        nonce = 0
        while self.valid_proof(last_nonce, nonce) is False:
            nonce += 1
        return nonce

    # Kontrola, jestli hash odpovídá obtížnosti (čtyři nuly)
    @staticmethod
    def valid_proof(last_nonce, nonce):
        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # Kontrola integrity celého řetězce
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current['previous_hash'] != self.hash(prev):
                return False
            if not self.valid_proof(prev['nonce'], current['nonce']):
                return False
        return True

# Spuštění FastAPI
app = FastAPI(title="Cigicoin API")
blockchain = Blockchain()

# Přesměrování na interaktivní rozhraní
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Výpis všech bloků
@app.get("/blocks")
def get_blocks():
    return {"chain": blockchain.chain, "length": len(blockchain.chain)}

# Endpoint pro odeslání nové transakce
@app.post("/transaction")
def new_transaction(tx: Transaction):
    index = blockchain.add_transaction(tx.sender, tx.receiver, tx.amount)
    return {"message": f"Transakce bude pridana do bloku {index}"}

# Endpoint pro spuštění těžby
@app.get("/mine")
def mine_block():
    last_block = blockchain.last_block
    nonce = blockchain.proof_of_work(last_block['nonce'])
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)
    return {"message": "Blok vytezen", "block": block}

# Endpoint pro kontrolu, jestli je blockchain v pořádku
@app.get("/validate")
def validate_chain():
    valid = blockchain.is_chain_valid()
    return {"valid": valid, "message": "OK" if valid else "Naruseno!"}