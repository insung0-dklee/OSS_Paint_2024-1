import tkinter as tk
from PIL import Image, ImageTk
import os

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack()
        
        # 스탬프 이미지의 절대 경로
        stamp_image_path = os.path.join("C:/Users/minja/OneDrive/바탕 화면", "stamp.png")
        
        # 스탬프 이미지 로드
        self.stamp_image = Image.open(stamp_image_path)
        self.stamp_photo = ImageTk.PhotoImage(self.stamp_image)
        
        # 캔버스 클릭 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.stamp)

    def stamp(self, event):
        # 클릭 위치에 스탬프 이미지를 그립니다.
        self.canvas.create_image(event.x, event.y, image=self.stamp_photo, anchor=tk.CENTER)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
