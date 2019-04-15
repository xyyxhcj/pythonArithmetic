import random
import tkinter

# 配置
ROOT = tkinter.Tk(className='扫一下雷')
# 默认窗口坐标
DEFAULT_WIN_X, DEFAULT_WIN_Y = 3482, 76
# 长宽
HEIGHT = 26
WIDTH = 26
# 雷区数量
MINE_NUM = 20
# 雷区x坐标范围
MINE_X_MAX = 10
MINE_Y_MAX = 15
# 总格子数量
TOTAL = MINE_X_MAX * MINE_Y_MAX
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
                if not MineSweepData.in_area(x_temp, y_temp):
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
        for i in range(MINE_NUM, TOTAL):
            update(self.mine_data, i % MINE_X_MAX, i // MINE_X_MAX, DEFAULT_VALUE)

        # 使用fisherYates洗牌
        fisher_yates_shuffle(self.mine_data, TOTAL)
        # 计算左键点开雷区后应该显示的值
        count_mine(self.mine_data, TOTAL)
        # 提示框
        self.top = tkinter.Toplevel()
        self.top.destroy()
        # 设置窗口位置
        # ROOT.geometry('+' + str(DEFAULT_WIN_X) + '+' + str(DEFAULT_WIN_Y))
        ROOT.bind('<Configure>', self.change)
        # 存储窗口变更后的坐标
        self.win_x, self.win_y = DEFAULT_WIN_X, DEFAULT_WIN_Y

    @staticmethod
    def in_area(x, y):
        return 0 <= x < MINE_X_MAX and 0 <= y < MINE_Y_MAX

    # 刷新数据
    def refresh_label(self):
        self.label_value.set('剩余数量：' + str(MINE_NUM - self.flag_num))

    def refresh_img(self, x, y):
        show_data = self.data[x][y]
        show_data['btn'].configure(image=self.img[show_data['val']])
        # 仅未探索及标记区域 可使用按键
        if show_data['val'] == DEFAULT_VALUE or show_data['val'] == FLAG_VALUE:
            show_data['btn'].configure(state=tkinter.ACTIVE)
        else:
            show_data['btn'].configure(state=tkinter.DISABLED)

    def start(self):
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

    # 展开空的区域 flood fill遍历
    def open(self, l):
        while len(l) > 0:
            x, y = l.pop()
            for x_t in range(x - 1, x + 2):
                for y_t in range(y - 1, y + 2):
                    # 判断越界
                    if not MineSweepData.in_area(x_t, y_t):
                        continue
                    # 判断中心
                    if x_t == x and y_t == y:
                        continue
                    # 仅处理未探索及未标记区域
                    if self.data[x_t][y_t]['val'] == DEFAULT_VALUE and self.data[x][y]['val'] != FLAG_VALUE:
                        # 该区域未探索且值为0,需要再次从该点再向八个方向探索
                        if self.mine_data[x_t][y_t] == EMPTY_VALUE:
                            l.append((x_t, y_t))
                        self.data[x_t][y_t]['val'] = self.mine_data[x_t][y_t]
                        self.refresh_img(x_t, y_t)
                        if self.mine_data[x_t][y_t] == MINE_VALUE:
                            self.game_over()

    def click(self, x, y):
        if self.data[x][y]['val'] == FLAG_VALUE:
            return
            # 如果是雷区则game over,否则计算周围雷区数量,显示对应图片
        if self.mine_data[x][y] == MINE_VALUE:
            self.game_over()
        self.data[x][y]['val'] = self.mine_data[x][y]
        self.refresh_img(x, y)
        if self.mine_data[x][y] == EMPTY_VALUE:
            # 使用flood fill算法展开空白区域
            self.open([(x, y)])
        if self.check_win(TOTAL):
            self.show_msg_win()

    def click_right(self, x, y):
        # 反选区域标记
        if FLAG_VALUE == self.data[x][y]['val']:
            self.data[x][y]['val'] = DEFAULT_VALUE
            self.flag_num -= 1
        elif DEFAULT_VALUE == self.data[x][y]['val']:
            self.data[x][y]['val'] = FLAG_VALUE
            self.flag_num += 1
        elif self.data[x][y]['val'] > 0:
            # 该点为数字,如果四周已标记数量=该数字,则探索其八个方向的格子
            # 计算四周的标记和未探索区域
            count_flag, count_default = 0, 0
            default_temp = []
            for x_t in range(x - 1, x + 2):
                for y_t in range(y - 1, y + 2):
                    if not MineSweepData.in_area(x_t, y_t):
                        continue
                    if FLAG_VALUE == self.data[x_t][y_t]['val']:
                        count_flag += 1
                    elif DEFAULT_VALUE == self.data[x_t][y_t]['val']:
                        count_default += 1
                        default_temp.append((x_t, y_t))
            if count_flag == self.data[x][y]['val']:
                self.open([(x, y)])
            elif count_flag + count_default == self.data[x][y]['val']:
                # 如果未标记+已标记数量=数字,标记所有默认格子
                while len(default_temp) > 0:
                    x_t, y_t = default_temp.pop()
                    self.data[x_t][y_t]['val'] = FLAG_VALUE
                    self.flag_num += 1
                    self.refresh_img(x_t, y_t)
                    self.refresh_label()

        self.refresh_img(x, y)
        self.refresh_label()
        if self.check_win(TOTAL):
            self.show_msg_win()

    def game_over(self):
        # 显示所有雷
        for i in range(TOTAL):
            x, y = i % MINE_X_MAX, i // MINE_X_MAX
            if MINE_VALUE == self.mine_data[x][y]:
                self.data[x][y]['val'] = MINE_VALUE
                self.refresh_img(x, y)
            else:
                # 单独禁用
                self.data[x][y]['btn'].configure(state=tkinter.DISABLED)
        self.show_msg()

    def show_msg(self):
        self.top = tkinter.Toplevel()
        self.top.geometry('200x60+' + str(self.win_x) + '+' + str(self.win_y))
        tkinter.Label(self.top, text='game over').pack()
        tkinter.Button(self.top, text='try again', command=self.restart).pack()

    def show_msg_win(self):
        self.top = tkinter.Toplevel()
        self.top.geometry('200x60+' + str(self.win_x) + '+' + str(self.win_y))
        tkinter.Label(self.top, text='win！').pack()
        tkinter.Button(self.top, text='again', command=self.restart).pack()

    def restart(self):
        self.top.destroy()
        # 重新加载数据
        # 存储雷盘实际数据
        self.mine_data = {}
        # 重置标记数量
        self.flag_num = 0
        # 依序放入雷
        for i in range(MINE_NUM):
            update(self.mine_data, i % MINE_X_MAX, i // MINE_X_MAX, MINE_VALUE)
        # 初始化字典
        for i in range(MINE_NUM, TOTAL):
            update(self.mine_data, i % MINE_X_MAX, i // MINE_X_MAX, DEFAULT_VALUE)
        # 使用fisherYates洗牌
        fisher_yates_shuffle(self.mine_data, TOTAL)
        # 计算左键点开雷区后应该显示的值
        count_mine(self.mine_data, TOTAL)
        # 重置用于显示的字典
        self.refresh_label()
        for i in range(TOTAL):
            # 赋初始值
            x = i % MINE_X_MAX
            y = i // MINE_X_MAX
            self.data[x][y]['val'] = DEFAULT_VALUE
            self.refresh_img(x, y)

    def change(self, event):
        self.win_x, self.win_y = event.x, event.y

    def check_win(self, size):
        for i in range(size):
            # 获取坐标
            x, y = i % MINE_X_MAX, i // MINE_X_MAX
            if MINE_NUM != self.flag_num or self.data[x][y]['val'] == DEFAULT_VALUE:
                return False
        return True


def run():
    MineSweepData().start()


run()
