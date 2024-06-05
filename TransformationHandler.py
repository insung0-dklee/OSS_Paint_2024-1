from tkinter import Canvas

class TransformationHandler:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def flip_horizontal(self):
        self._flip_coordinates(horizontal=True)

    def flip_vertical(self):
        self._flip_coordinates(horizontal=False)

    def _flip_coordinates(self, horizontal=True):
        objects = self.canvas.find_all()
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        for obj in objects:
            coords = self.canvas.coords(obj)
            for i in range(len(coords)):
                if horizontal and i % 2 == 0:  # x 좌표를 반전시킵니다.
                    coords[i] = canvas_width - coords[i]
                elif not horizontal and i % 2 != 0:  # y 좌표를 반전시킵니다.
                    coords[i] = canvas_height - coords[i]
            self.canvas.coords(obj, *coords)

    def rotate_90(self):
        objects = self.canvas.find_all()
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        for obj in objects:
            coords = self.canvas.coords(obj)
            new_coords = []
            for i in range(0, len(coords), 2):
                x = coords[i] - canvas_center_x
                y = coords[i + 1] - canvas_center_y
                new_x = y
                new_y = -x
                new_coords.extend([new_x + canvas_center_x, new_y + canvas_center_y])
            self.canvas.coords(obj, *new_coords)

# 예시 사용법
# root = Tk()
# canvas = Canvas(root, width=400, height=400)
# canvas.pack()
# handler = TransformationHandler(canvas)
# handler.flip_horizontal()
# handler.flip_vertical()
# handler.rotate_90()
