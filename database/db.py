import os
from tinydb import TinyDB, Query

class Database:
    def __init__(self, name):
        self.db_name = name
        os.makedirs('database/decks', exist_ok=True)

        self.file_path = f'database/decks/{self.db_name}.json'

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as fp:
                fp.close()

        self.fruit = Query()

        self.db = TinyDB(self.file_path)

    def insert(self, fields: dict):
        if not isinstance(fields, dict):
            raise TypeError("Fields must be a dictionary.")
        return self.db.insert(fields)

    def search_all(self):
        return self.db.all()

    def search(self, query):
        return self.db.search(self.fruit.task == query)

    def delete(self, query):
        return self.db.remove(self.fruit.task == query)

    def update(self, fields, query):
        return self.db.update(fields, self.fruit.task == query)

class Decks:
    def __init__(self) -> None:
        self.decks_db = TinyDB('database\configs\decks.json')

    def list_decks(self):
        files = os.listdir('database/decks')
        decks = [os.path.splitext(f)[0] for f in files if f.endswith('.json')]
            
        return decks
    
    def delete(self, deck):
        Fruit = Query()
        self.decks_db.remove(Fruit.deck_name == deck)
        return os.remove(f'database/decks/{deck}.json')
    
    def query(self, deck):
        Fruit = Query()
        return self.decks_db.search(Fruit.deck_name == deck)
    
    def configs(self, name, task_time=25, break_time=5, cicles=3, ring='alert-sound-loop-189741.mp3'):
        return self.decks_db.insert(
            {
                'deck_name' : name,
                'task_time' : task_time,
                'break_time' : break_time,
                'cicles': cicles,
                'ring': f'assets/rings/{ring}' 
            }
        )