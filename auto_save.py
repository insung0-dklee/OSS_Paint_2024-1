import threading
from PIL import ImageGrab

def auto_save(canvas, window, file_path="autosave.png", interval=60):
    """
    일정 시간 간격으로 캔버스를 자동으로 저장하는 함수.
    file_path: 저장할 파일 경로
    interval: 저장 간격(초)
    """
    def save_canvas():
        x = window.winfo_rootx() + canvas.winfo_x()
        y = window.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
        threading.Timer(interval, save_canvas).start()

    save_canvas()


def manual_save(canvas, window, file_path="autosave.png"):
    """
    즉시 캔버스를 저장하는 함수.
    file_path: 저장할 파일 경로
    """
    x = window.winfo_rootx() + canvas.winfo_x()
    y = window.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)