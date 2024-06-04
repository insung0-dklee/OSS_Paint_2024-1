'''
## shortcuts.py
- 이 모듈은 주요 애플리케이션의 키보드 단축키를 표시하는 창을 제공합니다.
- 사용자가 단축키 정보를 쉽게 확인할 수 있도록 하는 GUI를 포함하고 있습니다.
- 만약 새로운 단축키를 추가하신다면 shortcuts = ("단축키", "단축키 설명"), 이렇게 달아주시면 자동으로 반영됩니다.
- 해당 window는 "F1" 단축키에 bind해뒀습니다.
'''

from tkinter import *

def open_shortcuts_window():
    shortcuts_window = Toplevel()
    shortcuts_window.title("Shortcuts")
    shortcuts_window.geometry("400x300")

    Label(shortcuts_window, text="Shortcuts", font=("Helvetica", 16, "bold")).pack(pady=10)

    shortcuts = [
        ("Ctrl+S", "Save canvas"),
        ("Ctrl+Z", "Undo last stroke"),
        ("Ctrl+Y", "Redo last undone stroke"),
        ("C", "Clear canvas"),
        ("D", "Toggle dark mode"),
        ("Q", "Set solid brush mode"),
        ("W", "Set dotted brush mode"),
        ("E", "Set double line brush mode")
    ]

    for shortcut, description in shortcuts:
        frame = Frame(shortcuts_window)
        frame.pack(anchor="w", padx=10, pady=2)
        Label(frame, text=shortcut, font=("Helvetica", 12, "bold"), width=15, anchor="w").pack(side=LEFT)
        Label(frame, text=description, font=("Helvetica", 12), anchor="w").pack(side=LEFT)

    close_button = Button(shortcuts_window, text="Close", command=shortcuts_window.destroy)
    close_button.pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    open_shortcuts_window()
    root.mainloop()