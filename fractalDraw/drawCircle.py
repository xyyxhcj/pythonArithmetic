import tkinter

OFFSET = 5


class DrawCircle(tkinter.Tk):

    def __init__(self, class_name, width, height):
        x2 = width + OFFSET
        y2 = height + OFFSET
        super().__init__(class_name)
        self.geometry('%dx%d' % (x2+OFFSET, y2+OFFSET))
        c = tkinter.Canvas(self, width=width, height=height)
        c.pack()
        y = int(height / 2)
        c.create_oval(OFFSET, OFFSET, width, height, fill='lightblue')
        self.mainloop()

    def run(self):
        pass


if __name__ == '__main__':
    DrawCircle('画圆', 200, 200)
