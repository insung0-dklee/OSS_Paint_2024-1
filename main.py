import tkinter as tk

class DrawingApp:
    def __init__(self, root):
        # Tkinter 윈도우 생성
        self.root = root
        self.root.title("Simple Drawing App")

        # 그림을 그릴 캔버스 생성
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # 그림 히스토리를 저장할 리스트 생성
        self.history = []

        # 메뉴 생성
        self.create_menu()

        # 마우스 이벤트에 따라 그림을 그리는 이벤트 핸들러 바인딩
        self.canvas.bind("<B1-Motion>", self.draw)

    def create_menu(self):
        # 메뉴 생성 및 연결
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)

        # 파일 메뉴에 저장, 불러오기, 지우기 항목 추가
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Load", command=self.load)
        file_menu.add_command(label="Clear", command=self.clear)

    def draw(self, event):
        # 마우스가 움직일 때마다 그림을 그림
        x, y = event.x, event.y
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
        self.history.append((x, y))  # 그림 히스토리에 현재 좌표 추가

    def save(self):
        # 그림 히스토리를 파일로 저장
        with open("drawing.txt", "w") as f:
            for x, y in self.history:
                f.write(f"{x},{y}\n")

    def load(self):
        # 그림 히스토리를 파일에서 불러와서 캔버스에 그림
        self.clear()
        with open("drawing.txt", "r") as f:
            for line in f:
                x, y = map(int, line.strip().split(","))
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
                self.history.append((x, y))  # 불러온 좌표를 그림 히스토리에 추가

    def clear(self):
        # 캔버스와 그림 히스토리를 지움
        self.canvas.delete("all")
        self.history = []

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()
