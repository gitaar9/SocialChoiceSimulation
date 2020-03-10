from model import Model
from view import View


class Program:

    def __init__(self, time_step_duration=200):
        self.time_step_duration = time_step_duration
        self.model = Model()
        self.view = View(self.model, self.keydown)

    def keydown(self, e):
        if e.char == 'a':
            self.model.turn_beam_left()
        elif e.char == 'l':
            self.model.turn_beam_right()
        self.view.draw_model()

    def update(self, master):
        self.model.run_timestep()
        self.view.draw_model()
        master.after(self.time_step_duration, self.update, master)


def main():
    p = Program()

    p.view.master.after(100, p.update, p.view.master)
    p.view.master.mainloop()


main()
