from tkinter import Canvas

class TransformationHandler:
    """
    TransformationHandler 클래스는 주어진 캔버스 객체의 도형들에 대해 다양한 변환 작업을 수행합니다.
    """

    def __init__(self, canvas: Canvas):
        """
        TransformationHandler 객체를 초기화합니다.

        매개변수:
        canvas (Canvas): 변환 작업을 수행할 캔버스 객체.
        """
        self.canvas = canvas

    def flip_horizontal(self):
        """
        캔버스에 그려진 모든 도형을 수평으로 반전시킵니다.
        """
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
        """
        캔버스에 그려진 모든 도형을 수직으로 반전시킵니다.
        """
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
        """
        캔버스에 그려진 모든 도형을 시계 방향으로 90도 회전시킵니다.
        """
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
                # 좌표를 시계 방향으로 90도 회전시킵니다.
                new_x = y
                new_y = canvas_width - x
                new_coords.extend([new_x, new_y])
            self.canvas.coords(obj, *new_coords)
