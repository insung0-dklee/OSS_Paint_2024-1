# image_editor.py
from tkinter import NW, PhotoImage

class ImageEditor:
    def __init__(self, canvas):
        self.canvas = canvas

    def open_image(self, file_path):
        if file_path:
            self.image = PhotoImage(file=file_path)
            canvas_width = self.canvas.winfo_width() or 400  
            canvas_height = self.canvas.winfo_height() or 400  
            quarter_width = canvas_width // 2
            quarter_height = canvas_height // 2
            self.image = self.image.subsample(2)  
            x = (canvas_width - quarter_width) // 2
            y = (canvas_height - quarter_height) // 2
            self.canvas.create_image(x, y, anchor=NW, image=self.image)
"""
class
@fun(이미지 open )
    __init__ : 생성자로 canvas 객체를 매개변수로 받아 변수에 저장
    open_imgae(): 매개변수로 파일 경로를 받아 사진을 해당 경로로 사진을 받아온다.
    @variable: 
      canvas_width: 캔버스의 너비를 가져온다. 너비가 0이면 400으로 지정
      canvas_height :캔버스 높이를 가져온다. 너비가 0이면 400으로 지정 
      self.image.subsample(2): 이미지를 캔버스 크기의 4분의 1로 축소 
self.canvas.create_image: 이미지를 캔버스에 배치 
  
"""