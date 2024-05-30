from tkinter import *
from tkinter.colorchooser import askcolor

#브러쉬 색상, 브러쉬 크기를 변경할 수 있는 기능 구현

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        self.brush_color = "black"
        self.brush_size = 5

        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)

        self.create_menu()

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)

    def change_color(self):
        self.brush_color = askcolor(color=self.brush_color)[1]

    def change_brush_size(self, new_size):
        self.brush_size = new_size

    def create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        brush_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="브러시", menu=brush_menu)
        brush_menu.add_command(label="색상 변경", command=self.change_color)

        brush_size_menu = Menu(brush_menu, tearoff=0)
        brush_menu.add_cascade(label="크기 변경", menu=brush_size_menu)
        for size in [2, 5, 10, 20, 50]:
            brush_size_menu.add_command(label=str(size), command=lambda s=size: self.change_brush_size(s))

if __name__ == "__main__":
    root = Tk()
    app = PaintApp(root)
    root.mainloop()

