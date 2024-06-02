import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

class PaintApp:
    def __init__(self, root):
        # 초기화 메서드, 기본 설정을 정의합니다.
        self.root = root
        self.root.title("Python 그림판")
        self.root.geometry("800x600")
        
        # 그림을 그릴 캔버스를 만듭니다.
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 사용자가 텍스트를 입력할 수 있는 입력 상자를 만듭니다.
        self.text_entry = tk.Entry(self.root)
        self.text_entry.pack()
        
        # 글자 뒤집기 버튼을 만듭니다.
        self.btn_flip_text = tk.Button(self.root, text="글자 뒤집기", command=self.flip_text)
        self.btn_flip_text.pack(side=tk.LEFT)
        
        # 글자 기울임 버튼을 만듭니다.
        self.btn_skew_text = tk.Button(self.root, text="글자 기울임", command=self.skew_text)
        self.btn_skew_text.pack(side=tk.LEFT)
        
        self.text_image = None  # 텍스트 이미지를 저장할 변수를 초기화합니다.

    def flip_text(self):
        # 텍스트 뒤집기 기능을 구현합니다.
        text = self.text_entry.get()
        if text:
            # 텍스트를 이미지로 변환합니다.
            font = ImageFont.truetype("arial.ttf", 40)
            bbox = font.getbbox(text)
            size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
            image = Image.new("RGBA", size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.text((-bbox[0], -bbox[1]), text, font=font, fill="black")
            # 이미지를 좌우 반전시킵니다.
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            # 반전된 이미지를 캔버스에 표시합니다.
            self.text_image = ImageTk.PhotoImage(flipped_image)
            self.canvas.create_image(400, 300, image=self.text_image, anchor=tk.CENTER)
    
    def skew_text(self):
        # 텍스트 기울임 기능을 구현합니다.
        text = self.text_entry.get()
        if text:
            # 텍스트를 이미지로 변환합니다.
            font = ImageFont.truetype("arial.ttf", 40)
            bbox = font.getbbox(text)
            size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
            image = Image.new("RGBA", size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.text((-bbox[0], -bbox[1]), text, font=font, fill="black")
            # 이미지를 기울입니다.
            skewed_image = image.transform(
                (size[0] + 20, size[1]),
                Image.AFFINE,
                (1, -0.3, 0, 0, 1, 0),
                resample=Image.BICUBIC
            )
            # 기울어진 이미지를 캔버스에 표시합니다.
            self.text_image = ImageTk.PhotoImage(skewed_image)
            self.canvas.create_image(400, 300, image=self.text_image, anchor=tk.CENTER)

if __name__ == "__main__":
    # 애플리케이션을 실행합니다.
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
