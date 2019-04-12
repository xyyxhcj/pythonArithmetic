import random
import tkinter

# 配置
ROOT = tkinter.Tk(className='扫雷')
# 长宽
HEIGHT = 24
WIDTH = 24
# 雷区数量
MINE_NUM = 20
# 雷区x坐标范围
MINE_X_MAX = 10
MINE_Y_MAX = 15
# 雷
MINE_VALUE = -3
# 标记
FLAG_VALUE = -2
DEFAULT_VALUE = -1
EMPTY_VALUE = 0


# 更新字典
def update(t_dict, key_x, key_y, value):
    if key_x not in t_dict:
        t_dict[key_x] = {}
    t_dict[key_x][key_y] = value


# fisherYates洗牌算法
def fisher_yates_shuffle(dict_data, size):
    for i in range(size - 1, 0, -1):
        randint = random.randint(0, i)
        if randint != i:
            # 交换两张牌
            x_1, y_1 = i % MINE_X_MAX, i // MINE_X_MAX
            x_2, y_2 = randint % MINE_X_MAX, randint // MINE_X_MAX
            dict_data[x_1][y_1], dict_data[x_2][y_2] = dict_data[x_2][y_2], dict_data[x_1][y_1]


# 计算左键点开雷区后应该显示的值
def count_mine(mine_data, size):
    for i in range(size):
        # 获取坐标
        x, y = i % MINE_X_MAX, i // MINE_X_MAX
        if mine_data[x][y] == MINE_VALUE:
            continue
        # 计算周围雷量并赋值
        total = 0
        for x_temp in range(x - 1, x + 2):
            for y_temp in range(y - 1, y + 2):
                if x_temp < 0 or x_temp >= MINE_X_MAX or y_temp < 0 or y_temp >= MINE_Y_MAX:
                    continue
                if mine_data[x_temp][y_temp] == MINE_VALUE:
                    total += 1
        mine_data[x][y] = total


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

    def __init__(self) -> None:
        # 用于存储画面对应数据的二维数组(用于展示)
        self.data = []
        # 存储雷盘实际数据
        self.mine_data = {}
        # 存储标记数量
        self.flag_num = 0
        self.label_value = tkinter.StringVar()
        # 依序放入雷
        for i in range(MINE_NUM):
            update(self.mine_data, i % MINE_X_MAX, i // MINE_X_MAX, MINE_VALUE)
        # 初始化字典
        total = MINE_X_MAX * MINE_Y_MAX
        for i in range(MINE_NUM, total):
            update(self.mine_data, i % MINE_X_MAX, i // MINE_X_MAX, DEFAULT_VALUE)

        # 使用fisherYates洗牌
        fisher_yates_shuffle(self.mine_data, total)
        # 计算左键点开雷区后应该显示的值
        count_mine(self.mine_data, total)

    # 刷新数据
    def refresh_label(self):
        self.label_value.set('剩余数量：' + str(MINE_NUM - self.flag_num))

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

    # 展开空的区域
    def flood_fill(self, l):
        while len(l) > 0:
            x, y = l.pop()
            for x_t in range(x - 1, x + 2):
                for y_t in range(y - 1, y + 2):
                    if x_t < 0 or x_t >= MINE_X_MAX or y_t < 0 or y_t >= MINE_Y_MAX:
                        continue
                    if x_t == x and y_t == y:
                        continue
                    if self.data[x_t][y_t]['val'] == DEFAULT_VALUE and self.data[x][y]['val'] != FLAG_VALUE:
                        if self.mine_data[x_t][y_t] == EMPTY_VALUE:
                            # 该区域未探索且值为0
                            l.append((x_t, y_t))
                        self.data[x_t][y_t]['val'] = self.mine_data[x_t][y_t]
                        self.refresh_img(x_t, y_t)

    def click(self, x, y):
        if self.data[x][y]['val'] == FLAG_VALUE:
            return
            # 如果是雷区则game over,否则计算周围雷区数量,显示对应图片
        if self.mine_data[x][y] == MINE_VALUE:
            # todo
            print('game over')
        self.data[x][y]['val'] = self.mine_data[x][y]
        self.refresh_img(x, y)
        if self.mine_data[x][y] == EMPTY_VALUE:
            # 使用flood fill算法展开空白区域
            self.flood_fill([(x, y)])
        print(self.mine_data[x][y])

    def click_right(self, x, y):
        # 反选区域标记
        if FLAG_VALUE == self.data[x][y]['val']:
            self.data[x][y]['val'] = DEFAULT_VALUE
            self.flag_num -= 1
        elif DEFAULT_VALUE == self.data[x][y]['val']:
            self.data[x][y]['val'] = FLAG_VALUE
            self.flag_num += 1
        self.refresh_img(x, y)
        self.refresh_label()


def run():
    MineSweepData().show()


run()
