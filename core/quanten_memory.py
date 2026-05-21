from tinydb import TinyDB, Query

db = TinyDB('modules/memory/db.json')
User = Query()

def save_fact(key, value):
    if db.search(User.key == key):
        db.update({'value': value}, User.key == key)
    else:
        db.insert({'key': key, 'value': value})

def get_memory_string():
    all_facts = db.all()
    if not all_facts:
        return ""
    memory_text = "Erinnerungen an den User: "
    for fact in all_facts:
        memory_text += f"{fact['key']} ist {fact['value']}. "
    return memory_text
from tinydb import TinyDB, Query
import os

db_path = 'modules/memory/db.json'
if not os.path.exists('modules/memory'): os.makedirs('modules/memory')
db = TinyDB(db_path)
User = Query()

def save_fact(key, value):
    db.upsert({'key': key, 'value': value}, User.key == key)

def get_memory_string():
    facts = db.all()
    return " ".join([f"{f['key']} ist {f['value']}." for f in facts])