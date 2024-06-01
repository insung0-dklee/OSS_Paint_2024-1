"""
함수들:
- upload_image(window, canvas): 사용자가 파일 대화 상자를 통해 이미지 파일을 선택하고 미리보기 창을 엽니다.
- preview_image(window, canvas, path): 선택한 이미지를 미리보기 창에 표시하고 이미지 정보를 보여줍니다.
- select_image(canvas, path, preview_window): 선택한 이미지를 메인 캔버스에 표시하고 미리보기 창을 닫습니다.
"""

from tkinter import Toplevel, Label, Button, filedialog, NW
from PIL import Image, ImageTk

def upload_image(window, canvas):
    filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"), ("All files", "*.*")]
    path = filedialog.askopenfilename(filetypes=filetypes)
    if path:
        preview_image(window, canvas, path)

def preview_image(window, canvas, path):
    preview_window = Toplevel(window)
    preview_window.title("Image Preview")

    img = Image.open(path)
    img.thumbnail((200, 200))  # 미리보기 크기 조정
    img_tk = ImageTk.PhotoImage(img)

    img_label = Label(preview_window, image=img_tk)
    img_label.image = img_tk  # 이미지 참조를 저장하여 가비지 컬렉션 방지
    img_label.pack()

    img_info = f"File: {path}\nSize: {img.width}x{img.height}\nFormat: {img.format}"
    info_label_preview = Label(preview_window, text=img_info)
    info_label_preview.pack()

    Button(preview_window, text="Select", command=lambda: select_image(canvas, path, preview_window)).pack()

def select_image(canvas, path, preview_window):
    img = Image.open(path)
    img_resized = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)  # 이미지 크기 조정
    img_tk = ImageTk.PhotoImage(img_resized)
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.image = img_tk  # 이미지가 GC에 의해 수집되지 않도록 참조를 저장
    preview_window.destroy()