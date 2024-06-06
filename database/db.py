import os
from tinydb import TinyDB



class Database:
    def __init__(self, name):
        self.db_name = name
        os.makedirs('database', exist_ok=True)

        self.file_path = f'database/{self.db_name}.json'

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as fp:
                fp.close()


        self.db = TinyDB(self.file_path)

    def insert(self, fields: dict):
        if not isinstance(fields, dict):
            raise TypeError("Fields must be a dictionary.")
        return self.db.insert(fields)

    def search_all(self):
        return self.db.all()

    def search(self, query):
        return self.db.search(query)

    def delete(self, query):
        return self.db.remove(query)

    def update(self, fields, query):
        return self.db.update(fields, query)

class Decks:
    def list_decks(self):
        files = os.listdir('database')
        decks = [os.path.splitext(f)[0] for f in files if f.endswith('.json')]
            
        return decks
    
    def delete(self, deck):
        return os.remove(f'database/{deck}.json')