from tkinter import *
from tkinter.colorchooser import askcolor

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        # 브러시의 기본 색상과 크기 설정
        self.brush_color = "black"
        self.brush_size = 5

        # 캔버스 생성 및 배치
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)
        
        # 캔버스에서 마우스 드래그 이벤트에 paint 메서드를 바인딩
        self.canvas.bind("<B1-Motion>", self.paint)

        # 메뉴 생성
        self.create_menu()

        # 'All Clear' 버튼 생성
        self.create_clear_button()

    def paint(self, event):
        # 마우스 이벤트를 통해 그림을 그리는 함수
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)

    def change_color(self):
        # 색상 선택 다이얼로그를 열고 선택한 색상으로 브러시 색상을 변경하는 함수
        self.brush_color = askcolor(color=self.brush_color)[1]

    def change_brush_size(self, new_size):
        # 새로운 브러시 크기를 설정하는 함수
        self.brush_size = new_size

    def create_menu(self):
        # 메뉴 생성 및 설정하는 함수
        menu = Menu(self.root)
        self.root.config(menu=menu)

        brush_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="브러시", menu=brush_menu)
        brush_menu.add_command(label="색상 변경", command=self.change_color)

        brush_size_menu = Menu(brush_menu, tearoff=0)
        brush_menu.add_cascade(label="크기 변경", menu=brush_size_menu)
        for size in [2, 5, 10, 20, 50]:
            brush_size_menu.add_command(label=str(size), command=lambda s=size: self.change_brush_size(s))

    def create_clear_button(self):
        # 'All Clear' 버튼 생성 및 설정하는 함수
        clear_button = Button(self.root, text="All Clear", command=self.clear_paint)
        clear_button.pack()

    def clear_paint(self):
        # 캔버스에 있는 그림을 모두 지우는 함수
        self.canvas.delete("all")

if __name__ == "__main__":
    root = Tk()
    app = PaintApp(root)
    root.mainloop()

