"""
HistoryManager 클래스는 그림판의 상태를 저장하고 실행 취소(undo) 및 다시 실행(redo) 기능을 제공

##함수 설명
- __init__(self, canvas): 초기화 함수
- add_state(self): 현재 캔버스 상태를 히스토리에 추가
- undo(self): 히스토리에서 마지막 상태를 제거하고 이전 상태를 복원
- redo(self): redo 스택에서 마지막 상태를 가져와 히스토리에 추가하고 캔버스를 해당 상태로 복원
- _restore_last_state(self): 히스토리의 마지막 상태를 캔버스로 복원
- start_drawing(self): 드로잉이 시작될 때 호출하여 상태를 추가
- end_drawing(self): 드로잉이 끝날 때 호출하여 상태를 추가
"""

from PIL import Image, ImageGrab, ImageTk

class HistoryManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.history = []
        self.redo_stack = []
        self.is_drawing = False

    def add_state(self):
        self.redo_stack = []  # 새로운 상태가 추가되면 redo 스택 초기화
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab((x, y, x1, y1))
        self.history.append(image)

    def undo(self):
        if len(self.history) > 1:  # 항상 최소한 하나의 상태는 유지
            self.redo_stack.append(self.history.pop())
            self._restore_last_state()

    def redo(self):
        if self.redo_stack:
            self.history.append(self.redo_stack.pop())
            self._restore_last_state()

    def _restore_last_state(self):
        if self.history:
            self.canvas.delete("all")
            image = self.history[-1]
            self.canvas.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor='nw', image=self.canvas.image)

    def start_drawing(self):
        if not self.is_drawing:
            self.is_drawing = True
            self.add_state()

    def end_drawing(self):
        if self.is_drawing:
            self.is_drawing = False
            self.add_state()

