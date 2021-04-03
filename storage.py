import json
from types import SimpleNamespace

db = {}

def load():
    global db
    with open('data.json', 'r') as f:
        db = json.load(f)

def save():
    with open('data.json', 'w') as f:
        json.dump(db, f, indent=4)

def set_val(tag, val):
    db[tag] = val
    save()

def get_val(tag):
    return db.get(tag, None)

# linear search for wallet id from user id
def get_addr(user_id):
    lookup = db['wallet_lookup']

    for w in lookup:
        if lookup[w]['type'] == 'user':
            if lookup[w]['user_id'] == user_id:
                return w

def get_user(addr):
    return db['wallet_lookup'].get(addr, None)

async def get_name(bot, addr):
    lookup = db['wallet_lookup']
    if addr in lookup:
        entry = lookup[addr]
        
        if entry['type'] == 'user':
            user = await bot.fetch_user(entry['user_id'])
            return user.name
        else:
            return entry['name']


def add_wallet(addr, user_id):
    print(f'Adding wallet for {user_id}')
    lookup = db['wallet_lookup']

    # checks if wallet addr already in use
    if addr in lookup:
        print(f'Wallet id {addr} already in use')
        r = 'collision'
    else:
        # checks if user already listed under differet wallet
        old_addr = get_addr(user_id)
        if old_addr:
            data = lookup.pop(old_addr)
            lookup[addr] = data
            print(f'Updated wallet id {old_addr} -> {addr}')
            r = 'update'
        # regular case for new wallet
        else:
            lookup[addr] = {
                'type': 'user',
                'user_id': user_id
            }
            print(f'Added wallet id {addr}')
            r = 'new'
    save()
    return r

load()