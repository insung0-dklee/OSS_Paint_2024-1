from tkinter import Canvas

class TransformationHandler:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def flip_horizontal(self):
        objects = self.canvas.find_all()
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        for obj in objects:
            coords = self.canvas.coords(obj)
            for i in range(len(coords)):
                if i % 2 == 0:  # x 좌표를 반전시킵니다.
                    coords[i] = canvas_width - coords[i]
            self.canvas.coords(obj, *coords)

    def flip_vertical(self):
        objects = self.canvas.find_all()
        self.canvas.update()
        canvas_height = self.canvas.winfo_height()
        for obj in objects:
            coords = self.canvas.coords(obj)
            for i in range(len(coords)):
                if i % 2 != 0:  # y 좌표를 반전시킵니다.
                    coords[i] = canvas_height - coords[i]
            self.canvas.coords(obj, *coords)

    def rotate_90(self):
        objects = self.canvas.find_all()
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        for obj in objects:
            coords = self.canvas.coords(obj)
            new_coords = []
            for i in range(0, len(coords), 2):
                x = coords[i]
                y = coords[i + 1]
                new_x = y
                new_y = canvas_width - x
                new_coords.extend([new_x, new_y])
            self.canvas.coords(obj, *new_coords)