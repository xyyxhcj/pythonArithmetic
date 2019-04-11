# http://www.runoob.com/python/python-gui-tkinter.html
import tkinter


def test01():
    # 创建窗口对象
    root = tkinter.Tk()
    # 创建两个列表
    li = ['C', 'python', 'php', 'html', 'SQL', 'java']
    movie = ['CSS', 'jQuery', 'Bootstrap']
    # 创建两个列表组件
    list_a = tkinter.Listbox(root)
    list_b = tkinter.Listbox(root)
    # 第一个小部件插入数据
    for item in li:
        list_a.insert(0, item)
    # 第二个小部件插入数据
    for item in movie:
        list_b.insert(0, item)
    # 将小部件放置到主窗口中
    list_a.pack()
    list_b.pack()
    # 进入消息循环
    root.mainloop()


# http://www.runoob.com/python/python-tk-canvas.html
def test02():
    root = tkinter.Tk()
    # 创建一个Canvas，设置其背景色为白色
    cv = tkinter.Canvas(root, bg='white')
    # 创建一个矩形，坐标为(10,10,110,110)
    cv.create_rectangle(10, 10, 110, 110)
    cv.pack()
    root.mainloop()


def test03():
    root = tkinter.Tk(className='扫雷')
    img = tkinter.PhotoImage(file='./png/block.png')
    for x in range(20):
        for y in range(20):
            tkinter.Button(root, image=img, width=20, height=20).grid(row=y, column=x)
            # tkinter.Label(root, image=img).grid(row=y, column=x)
    root.mainloop()


test03()
