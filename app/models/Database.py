from tinydb import TinyDB, Query
import os

class Database:
    def __init__(self, name) -> None:
        self.path_decks = r'app\database\config.json'
        self.name = name
        
        self.query = Query()

    def open_task(self):
        self.path_tasks = rf'app\database\decks\{self.name}.json'
        self.tasks_db = TinyDB(self.path_tasks, encoding='utf-8', indent=4)

    def open_deck(self):
        self.deck_db = TinyDB(self.path_decks, encoding='utf-8', indent=4)

    def close_task(self):
        self.tasks_db.close()
    
    def close_deck(self):
        self.deck_db.close()

    def open_databases(self):
        self.open_task()
        self.open_deck()

    def close_databases(self):
        self.close_task()
        self.close_deck()

    def create_task(self, task, **kwargs):
        self.open_databases()

        for key, value in kwargs.items():
            setattr(task, key, value)

        if not self.tasks_db.contains(self.query.name == task.name):
            self.tasks_db.insert(
                {
                    'name': task.name,
                    'status': task.status,
                    'time': task.time,
                    'break_time': task.break_time,
                    'sound': task.sound,
                    'cycles': task.cycles
                }
            )
        self.close_databases()

    def create_deck(self, deck, **kwargs):
        self.open_databases()
        for key, value in kwargs.items():
            setattr(deck, key, value)

        if not self.deck_db.contains(self.query.name == deck.name):
            self.deck_db.insert(
                {
                    'name': deck.name,
                    'time': deck.time,
                    'break_time': deck.break_time,
                    'sound': deck.sound,
                    'cycles': deck.cycles
                }
            )
        self.close_databases()

    def edit_task(self, task, **kwargs):
        self.open_databases()
        for key, value in kwargs.items():
            setattr(task, key, value)

        self.tasks_db.update(
            {
                'name': task.name,
                'time': task.time,
                'status': task.status,  # Adicionei o campo 'status'
                'break_time': task.break_time,
                'sound': task.sound,
                'cycles': task.cycles
            },
            self.query.name == task.name
        )
        self.close_databases()

    def edit_deck(self, deck, **kwargs):
        self.open_databases()
        for key, value in kwargs.items():
            setattr(deck, key, value)

        self.deck_db.update(
            {
                'name': deck.name,
                'time': deck.time,
                'break_time': deck.break_time,
                'sound': deck.sound,
                'cycles': deck.cycles
            },
            self.query.name == self.name
        )
        self.close_databases()

    def delete_task(self, task, **kwargs):
        self.open_databases()
        for key, value in kwargs.items():
            setattr(task, key, value)

        self.tasks_db.remove(self.query.name == task.name)
        self.close_databases()

    def delete_deck(self, deck, **kwargs):

        self.open_deck()
        for key, value in kwargs.items():
            setattr(deck, key, value)

        self.deck_db.remove(self.query.name == deck.name)
        self.close_deck()

        os.remove(self.path_tasks)

    # def find_one_task(self):
    #     self.open_databases()
    #     result = self.deck_db.search(self.query.name == self.name)
    #     self.close_databases()
    #     return result

    def find_deck(self) -> list:
        self.open_databases()
        result = self.deck_db.search(self.query.name == self.name)
        self.close_databases()

        if result:
            first_dict = result[0]
            values_list = list(first_dict.values())
        else:
            values_list = False
        
        return values_list
    
    def find_tasks(self) -> list:
        """
        Returns a list of all tasks in the deck.
        """
        self.open_task()

        tasks = self.tasks_db.all()

        self.close_task()
        return tasks

    def find_decks(self) -> list:
        """
        Returns a list of all decks.
        """
        self.open_databases()
        decks = self.deck_db.all()
        self.close_databases()

        decks_name = []

        for deck in decks:
            decks_name.append(deck['name'])

        return decks_name
