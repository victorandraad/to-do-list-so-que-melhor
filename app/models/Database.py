from tinydb import TinyDB, Query

class Database:
    def __init__(self, name=None) -> None:
        self.path_decks = r'app\database\config.json'
        self.path_tasks = rf'app\database\decks\{name}.json'

        self.name = name
        self.deck_db = TinyDB(self.path_decks, encoding='utf-8', indent=4)
        self.tasks_db = TinyDB(self.path_tasks, encoding='utf-8', indent=4)

        self.query = Query()

    def create_task(self, task, **kwargs):
        for key, value in kwargs.items():
            setattr(task, key, value)

        if not self.tasks_db.contains(self.query.name == task.name):
            self.tasks_db.insert(
                {
                    'name': task.name,
                    'status': task.status,
                    'time': task.time,
                    'break_time': task.break_time,
                    'ring': task.sound,
                    'cycles': task.cycles
                }
            )

    def create_deck(self, deck, **kwargs):
        for key, value in kwargs.items():
            setattr(deck, key, value)

        if not self.deck_db.contains(self.query.name == deck.name):

            self.deck_db.insert(
                {
                    'name': deck.name,
                    'time': deck.time,
                    'break_time': deck.break_time,
                    'ring': deck.sound,
                    'cycles': deck.cycles
                }
            )

    def edit_task(self, task, **kwargs):
        for key, value in kwargs.items():
            setattr(task, key, value)

        # Update the task in the database
        self.tasks_db.update(
            {
                'name': task.name,
                'time': task.time,
                'status'
                'break_time': task.break_time,
                'ring': task.sound,
                'cycles': task.cycles
            },
            self.query.name == task.name # Assuming doc_id is a unique identifier in TinyDB
        )

    def edit_deck(self, deck, **kwargs):
        for key, value in kwargs.items():
            setattr(deck, key, value)

        # Update the task in the database
        self.deck_db.update(
            {
                'name': deck.name,
                'time': deck.time,
                'break_time': deck.break_time,
                'ring': deck.sound,
                'cycles': deck.cycles
            },
            self.query.name == self.name # Assuming doc_id is a unique identifier in TinyDB
        )

    def delete_task(self, task, **kwargs):
        for key, value in kwargs.items():
            setattr(task, key, value)

        self.tasks_db.remove(self.query.name == task.name)

    def delete_deck(self, deck, **kwargs):
        for key, value in kwargs.items():
            setattr(deck, key, value)

        self.tasks_db.truncate()
        self.deck_db.remove(self.query.name == deck.name)

    # def find_one_task(self, name):
    #     # Implement search logic
    #     pass

    # def find_deck(self, name):
    #     self.create_deck
    
    def find_tasks(self) -> list:
        """
            Returns a list of all tasks in the deck
        """
        return self.tasks_db.all()
        

    def find_decks(self) -> list:
        """
            Returns a list of all decks
        """
        return self.deck_db.all()
