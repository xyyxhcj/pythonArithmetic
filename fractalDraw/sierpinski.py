# 切分九宫格,只填充中心及四角
import tkinter

import math

OFFSET = 5


class DrawSudoku(tkinter.Tk):
    def __init__(self, class_name, width, height, depth):
        self.width = width
        self.height = height
        x2 = width + OFFSET
        y2 = height + OFFSET
        super().__init__(className=class_name)
        # 计算停止递归的边长
        min_length = self.get_min(depth)
        self.geometry('%dx%d' % (x2 + OFFSET, y2 + OFFSET))
        self.canvas = tkinter.Canvas(self, width=width, height=height)
        self.bind('<Key>', self.redraw)
        self.canvas.pack()
        self.draw(self.canvas, OFFSET, OFFSET, width, height, min_length)
        self.mainloop()

    def get_min(self, depth):
        less = self.width if self.width < self.height else self.height
        math_pow = math.pow(3, depth)
        print(math_pow, less // math_pow)
        return max(less // math_pow, 0.5)

    def redraw(self, event):
        # 判断是否数字
        char = event.char
        if char.isdigit():
            click_num = int(char)
            print(click_num)
            if 0 <= click_num < 10:
                min_length = self.get_min(click_num)
                self.canvas.destroy()
                self.canvas = tkinter.Canvas(self, width=self.width, height=self.height)
                self.canvas.pack()
                self.draw(self.canvas, OFFSET, OFFSET, self.width, self.height, min_length)
                self.mainloop()

    def draw(self, canvas, start_x, start_y, end_x, end_y, min_length):
        # 计算九宫格中每格长宽
        width = (end_x - start_x) / 3
        height = (end_y - start_y) / 3
        if width < min_length or height < min_length:
            # 填充最后的点
            canvas.create_rectangle(start_x, start_y, end_x, end_y, fill='lightblue', width=0)
            return
        # 画出中间的格子
        canvas.create_rectangle(start_x + width, start_y + height, end_x - width, end_y - height, fill='lightblue',
                                width=0)

        # 四个角坐标开始xy,结束xy的计算距离
        count_next = [[0, 0, width, height], [width * 2, 0, width * 3, height], [0, height * 2, width, height * 3],
                      [width * 2, height * 2, width * 3, height * 3]]
        # 递归画四个角
        for item in count_next:
            self.draw(canvas, start_x + item[0], start_y + item[1], start_x + item[2], start_y + item[3], min_length)


def main():
    DrawSudoku('递归九宫只画中间', 1000, 800, 0)


if __name__ == '__main__':
    main()
