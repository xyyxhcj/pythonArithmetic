import tkinter

# 配置
ROOT = tkinter.Tk(className='扫雷')
# 长宽
HEIGHT = 20
WIDTH = 20


class MineSweepData:
    # 定义值对应的图片
    img = {
        -1: tkinter.PhotoImage(file='./png/block.png'),
        -2: tkinter.PhotoImage(file='./png/flag.png'),
        -3: tkinter.PhotoImage(file='./png/mine.png'),
        0: tkinter.PhotoImage(file='./png/0.png'),
        1: tkinter.PhotoImage(file='./png/1.png'),
        2: tkinter.PhotoImage(file='./png/2.png'),
        3: tkinter.PhotoImage(file='./png/3.png'),
        4: tkinter.PhotoImage(file='./png/4.png'),
        5: tkinter.PhotoImage(file='./png/5.png'),
        6: tkinter.PhotoImage(file='./png/6.png'),
        7: tkinter.PhotoImage(file='./png/7.png'),
        8: tkinter.PhotoImage(file='./png/8.png'),
    }

    def __init__(self) -> None:
        # 创建初始值为-1的二维数组
        self.data = [[-1 for i in range(20)] for i in range(20)]

    def show(self):
        for x, arr in enumerate(self.data):
            for y, val in enumerate(arr):
                tkinter.Button(ROOT, image=self.img[val], width=WIDTH, height=HEIGHT).grid(row=y, column=x)
        ROOT.mainloop()


def run():
    MineSweepData().show()


run()
