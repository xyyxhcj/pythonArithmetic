# 画三角形,递归画三个角
import tkinter

import math

OFFSET = 5
# 正三角形角度
ANGLE = 60


class DrawSudoku(tkinter.Tk):
    def __init__(self, class_name, length, depth):
        self.length = length
        super().__init__(className=class_name)
        # 计算停止递归的边长
        x2 = y2 = length + OFFSET
        min_length = self.get_min(depth)
        self.geometry('%dx%d' % (x2 + OFFSET, y2 + OFFSET))
        self.canvas = tkinter.Canvas(self, width=length, height=length)
        self.bind('<Key>', self.redraw)
        self.canvas.pack()
        self.draw(self.canvas, OFFSET, length, length, min_length)
        self.mainloop()

    def get_min(self, depth):
        math_pow = math.pow(2, depth)
        min_length = max(self.length // math_pow, 2)
        print('min_length:%d' % min_length)
        return min_length

    def redraw(self, event):
        # 判断是否数字
        char = event.char
        if char.isdigit():
            click_num = int(char)
            print(click_num)
            if 0 <= click_num < 10:
                min_length = self.get_min(click_num)
                self.canvas.destroy()
                self.canvas = tkinter.Canvas(self, width=self.length, height=self.length)
                self.canvas.pack()
                self.draw(self.canvas, OFFSET, self.length, self.length, min_length)
                self.mainloop()

    # x,y为正三角形左下角坐标
    def draw(self, canvas, start_x, start_y, length, min_length):
        # 角度转弧度
        radians = math.radians(ANGLE)
        # 计算三角形的高度
        height = math.sin(radians) * length
        # 设置三个角坐标的list
        points = [
            start_x, start_y,
            start_x + length, start_y,
            start_x + (length / 2), start_y - height,
        ]
        if length <= min_length:
            # 根据点来连线
            canvas.create_polygon(points, fill='lightBlue')
            return
        else:
            # 画三个角
            # 求三个角左下角坐标的距离差
            count_next = [[0, 0], [length / 2, 0], [length / 4, -height / 2]]
            # 递归画三个角
            for item in count_next:
                self.draw(canvas, start_x + item[0], start_y + item[1], length / 2, min_length)


def main():
    DrawSudoku('sierpinski', 900, 2)


if __name__ == '__main__':
    main()
