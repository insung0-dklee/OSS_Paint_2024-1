from PIL import Image, ImageTk, ImageEnhance
from tkinter import CENTER
"""
캔버스에 워터마크를 적용하는 기능을 제공합니다.

Function:
- apply_watermark(canvas, watermark_path, alpha=1.0, brightness=1.0): 
  지정된 투명도(alpha)와 밝기(brightness)를 사용하여 주어진 캔버스에 워터마크를 적용합니다.
"""
def apply_watermark(canvas, watermark_path, alpha=1.0, brightness=1.0):
    # 캔버스 크기를 가져옵니다.
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # 워터마크 이미지를 열고 크기를 조정합니다.
    watermark = Image.open(watermark_path)
    watermark = watermark.resize((canvas_width // 3, canvas_height // 3), Image.Resampling.LANCZOS)

    # 워터마크의 밝기 설정
    enhancer = ImageEnhance.Brightness(watermark)
    watermark = enhancer.enhance(brightness)

    # 투명도 설정
    watermark = watermark.convert("RGBA")
    alpha_channel = watermark.split()[3]
    alpha_channel = ImageEnhance.Brightness(alpha_channel).enhance(alpha)
    watermark.putalpha(alpha_channel)

    # 워터마크 이미지를 PhotoImage로 변환합니다.
    watermark = ImageTk.PhotoImage(watermark)

    # 워터마크 이미지를 캔버스 중앙에 추가합니다.
    canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=CENTER, image=watermark)
    canvas.watermark = watermark  # 이 라인을 추가하여 이미지가 GC에 의해 수집되지 않도록 합니다.
