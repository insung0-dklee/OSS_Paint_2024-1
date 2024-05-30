from tkinter import *
from tkinter import filedialog

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        image = PhotoImage(file=file_path)
        canvas.image = image  # Keep a reference to avoid garbage collection
        canvas.create_image(0, 0, anchor=NW, image=image)

def paint_with_mouse():
    def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

    window = Tk()
    canvas = Canvas(window)
    canvas.pack()
    canvas.bind("<B1-Motion>", paint)
    window.mainloop()

if __name__ == "__main__":
    paint_with_mouse()