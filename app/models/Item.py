class Item:
    def __init__(self, name, time, break_time, cycles, sound):
        self.name: str = name
        self.time: int = time
        self.break_time: int = break_time
        self.cycles: int = cycles
        self.sound: str = sound

    def die(self):
        # Implement delete logic
        pass
