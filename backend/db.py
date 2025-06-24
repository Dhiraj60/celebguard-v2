import json
import os

DB_FILE = 'data/contracts.json'

def save_contract(contract_data):
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)

    try:
        with open(DB_FILE, 'r') as f:
            contracts = json.load(f)
    except json.JSONDecodeError:
        contracts = []

    contracts.append(contract_data)

    with open(DB_FILE, 'w') as f:
        json.dump(contracts, f, indent=4)
def load_contracts():
    with open(DB_FILE, 'r') as f:
        return json.load(f)
