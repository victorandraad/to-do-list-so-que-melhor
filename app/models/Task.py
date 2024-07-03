from app.models.Item import Item

class Task(Item):
    def __init__(self, name, time, break_time, cycles, sound, status):
        super().__init__(name, time, break_time, cycles, sound)
        self.status: int = status
        self.previous_status: int = 0

        self.running: bool          = True if status == 1 else False
        self.is_break_time: bool    = True if status == 2 else False
        self.paused: bool           = True if status == 3 else False
        self.finish: bool           = True if status == 4 else False
        

    def reset_states(self):
        self.running = False
        self.paused = False
        self.finish = False
        self.is_break_time = False
        self.previous_status = self.status

    def set_blank(self):
        self.reset_states()
        self.status = 0

    def set_break_time(self):
        self.reset_states()
        self.is_break_time = True
        self.status = 2

    def set_running(self):
        self.reset_states()
        self.running = True
        self.status = 1

    def set_finish(self):
        self.reset_states()
        self.finish = True
        self.status = 4

    def set_paused(self):
        self.reset_states()
        self.paused = True
        self.status = 3

    def resume(self):
        self.paused = False
        self.status = self.previous_status
        match(self.previous_status):
            case 1:
                self.running = True
            
            case 2:
                self.is_break_time = True
        

    def click(self):
        """ 
            0 = icons.CHECK_BOX_OUTLINE_BLANK
            1 = icons.RADIO_BUTTON_CHECKED
            2 = icons.FREE_BREAKFAST
            3 = icons.PAUSE_ROUNDED
            4 = icons.CHECK_BOX

        """
        match(self.status):
            case 0:
                self.set_running()
            
            case 1:
                self.set_paused()
            
            case 2:
                self.set_paused()

            case 3:
                self.resume()
            
            case 4:
                self.set_blank()


    
    # def run_time(self) -> int:
    #     # Implement execution logic
    #     pass

    # def run_break_time() -> int:
    #     pass
