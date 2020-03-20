from model import Model
from social_choice_functions import *
from view import View
import time


class Program:

    def __init__(self, time_step_duration=100):
        self.time_step_duration = time_step_duration
        self.model = Model(social_choice_function=Plurality)
        self.view = View(self.model, self.keydown)

    def keydown(self, e):
        if e.char == 'a':
            self.model.turn_beam_left()
        elif e.char == 'l':
            self.model.turn_beam_right()
        self.view.draw_model()

    def update(self, master):
        start_time = time.time()
        self.model.run_timestep()
        self.view.draw_model()
        master.after(self.time_step_duration - int((time.time() - start_time) * 1000), self.update, master)
        # print(time.time() - start_time)


def main():
    p = Program()

    p.view.master.after(100, p.update, p.view.master)
    p.view.master.mainloop()


main()
