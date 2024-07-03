from Item import Item

class Deck(Item):
    def __init__(self, name, time, break_time, cycles, sound):
        super().__init__(name, time, break_time, cycles, sound)
        self.tasks = []
