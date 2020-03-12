import math
import sys
import tkinter as tk


class MyCanvas(tk.Canvas):
    """
    Extension of a tkinter canvas with some added functions for directly drawing beams and balls
    """
    beam_y = 300

    @staticmethod
    def rotate(points, angle, center):
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = center
        new_points = []
        for x_old, y_old in points:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        return new_points

    def draw_points(self, points, color, angle, rotate_center):
        if angle:
            points = self.rotate(points, angle, rotate_center)
        self.create_polygon(points, fill=color)

    def draw_rectangle(self, x, y, width, height, color, angle=None, rotate_center=None):
        points = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        ]
        center = rotate_center or (x + width * 0.5, y + height * 0.5)
        self.draw_points(points, color, angle, center)

    def draw_circle(self, x, y, size, color, angle=None, rotate_center=None):
        # Generate the points to draw the circle
        r = size * 0.5  # radius of the circle
        res = size  # resolution
        points_at_origin = [(math.cos(2 * math.pi / res * i) * r, math.sin(2 * math.pi / res * i) * r)
                            for i in range(0, res + 1)]
        d_x = x + size * 0.5
        d_y = y + size * 0.5
        points = [(origin_x + d_x, origin_y + d_y) for origin_x, origin_y in points_at_origin]

        center = rotate_center or (x + size * 0.5, y + size * 0.5)
        self.draw_points(points, color, angle, center)

    def draw_beam(self, beam, center):
        self.draw_rectangle(
            *self.get_beam_coordinates(beam, center),
            color="RoyalBlue3",
            angle=beam.angle
        )

    def draw_ball(self, beam, ball, center):
        start_x = center - beam.size / 2
        ball_size = 35
        y = self.beam_y - ball_size

        beam_x, beam_y, beam_width, beam_height = self.get_beam_coordinates(beam, center)
        self.draw_circle(
            x=start_x + ball.location,
            y=y,
            size=ball_size,
            color="sea green",
            angle=beam.angle,
            rotate_center=(beam_x + beam_width * 0.5, beam_y + beam_height * 0.5)
        )

    def get_beam_coordinates(self, beam, center):
        return center - beam.size / 2, self.beam_y, beam.size, 50


class View:
    """
    The view has a pointer to model and uses that to make the canvas draw the balls and beam
    """

    def __init__(self, model, keydown_method, canvas_width=1400, canvas_height=600):
        self.model = model
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.master = tk.Tk()
        self.master.title("Beam and balls demo")
        self.master.bind('<Escape>', self.close)  # So we can close by pressing escape

        # Create canvas
        self.canvas = MyCanvas(self.master, width=canvas_width, height=canvas_height)
        self.canvas.bind("<KeyPress>", keydown_method)
        self.canvas.focus_set()
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        message = tk.Label(self.master, text="Press 'a' and 'l' to rotate the beam.")
        message.pack(side=tk.BOTTOM)

        self.draw_model()

    def draw_model(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the beam
        self.canvas.draw_beam(self.model.beam, self.canvas_width / 2)

        for ball in self.model.balls:
            self.canvas.draw_ball(self.model.beam, ball, self.canvas_width / 2)

    @staticmethod
    def close(event):
        sys.exit()
