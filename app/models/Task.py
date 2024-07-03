from Item import Item

class Task(Item):
    def __init__(self, name, time, break_time, cycles, sound, status):
        super().__init__(name, time, break_time, cycles, sound)
        self.status: str = status
        self.pause: bool = False
        self.running: bool = False
        self.finish: bool = False
        self.break_time: bool = False

    def pause(self) -> int:
        """
            Returns the value in seconds of the task's time.
        """
        self.pause = True
    
    def resume(self) -> str:
        """
            Resume paused task.
        """
        self.pause = False
    
    def run_time(self) -> int:
        # Implement execution logic
        pass

    def run_break_time() -> int:
        pass
