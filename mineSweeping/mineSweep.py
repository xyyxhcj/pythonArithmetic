import random
import tkinter

# 配置
ROOT = tkinter.Tk(className='扫雷')
# 刷新延迟
DELAY = 1000
# 长宽
HEIGHT = 20
WIDTH = 20
# 雷区数量
MINE_NUM = 20
# 雷区x坐标范围
MINE_X_MAX = 20
MINE_Y_MAX = 15
# 雷
MINE_VALUE = -3
# 标记
FLAG_VALUE = -2
DEFAULT_VALUE = -1


# 更新字典
def update(t_dict, key_x, key_y, value, length):
    if key_x not in t_dict:
        t_dict[key_x] = {}
    elif key_y not in t_dict[key_x]:
        t_dict[key_x][key_y] = value
        length += 1
    return length


class MineSweepData:
    # 定义值对应的图片
    img = {
        # 未探索
        -1: tkinter.PhotoImage(file='./png/block.png'),
        # 标记
        -2: tkinter.PhotoImage(file='./png/flag.png'),
        # 雷
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

    def __init__(self, num) -> None:
        # 用于存储画面对应数据的二维数组
        self.data = []
        # 存储雷区字典
        self.mine_data = {}
        # 存储标记数量
        self.flag_num = 0
        # 存储雷区数量
        self.mine_num = 0
        self.label_value = tkinter.StringVar()
        # 存储随机雷区
        while self.mine_num < num:
            x = random.randint(0, MINE_X_MAX)
            y = random.randint(0, MINE_Y_MAX)
            self.mine_num = update(self.mine_data, x, y, MINE_VALUE, self.mine_num)

    # 刷新数据
    def refresh_label(self):
        self.label_value.set('剩余数量：' + str(self.mine_num - self.flag_num))

    def refresh_img(self, x, y):
        show_data = self.data[x][y]
        show_data['btn'].configure(image=self.img[show_data['val']])
        # 批量更新图片:ROOT.update_idletasks()

    def show(self):
        # 初始化展示数据
        for x in range(MINE_X_MAX):
            y_list = []
            for y in range(MINE_Y_MAX):
                button = tkinter.Button(ROOT, image=self.img[DEFAULT_VALUE], width=WIDTH, height=HEIGHT,
                                        command=lambda x1=x, y1=y: self.click(x1, y1))
                # 绑定右击事件 事件关联参数: https://www.cnblogs.com/aland-1415/p/6849193.html
                button.bind('<Button-3>', lambda event, x1=x, y1=y: self.click_right(x1, y1))
                button.grid(row=y, column=x)
                # 存储展示数据
                y_list.append({'val': DEFAULT_VALUE, 'btn': button})
            self.data.append(y_list)
        self.refresh_label()
        label = tkinter.Label(ROOT, textvariable=self.label_value)
        label.grid(row=MINE_Y_MAX, columnspan=MINE_X_MAX)
        ROOT.mainloop()

    def click(self, x, y):
        # 如果是雷区则game over,否则计算周围雷区数量,显示对应图片
        # todo test
        print(x, y)
        self.data[x][y]['val'] = 5
        self.refresh_img(x, y)
        print(self.data[x][y])

    def click_right(self, x, y):
        # 反选区域标记
        if FLAG_VALUE == self.data[x][y]['val']:
            self.data[x][y]['val'] = DEFAULT_VALUE
            self.flag_num -= 1
        elif DEFAULT_VALUE == self.data[x][y]['val']:
            self.data[x][y]['val'] = FLAG_VALUE
            self.flag_num += 1
        self.refresh_label()


def run():
    MineSweepData(MINE_NUM).show()


run()
