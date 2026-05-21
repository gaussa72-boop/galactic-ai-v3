from tinydb import TinyDB, Query
import os

# Speicherort für das Gedächtnis
db_dir = 'modules/memory'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db = TinyDB(f'{db_dir}/db.json')
User = Query()

def save_fact(key, value):
    """Speichert oder aktualisiert eine Information."""
    db.upsert({'key': key, 'value': value}, User.key == key)
    print(f"💾 Quanten-Memory-Update: {key} -> {value}")

def get_memory_string():
    """Gibt alle gespeicherten Fakten als Text für die KI zurück."""
    all_facts = db.all()
    if not all_facts:
        return "Keine vorherigen Daten vorhanden."
    return " ".join([f"{f['key']} ist {f['value']}." for f in all_facts])

def clear_memory():
    """Löscht das Gedächtnis (Reset)."""
    db.truncate()