# -*- coding: utf-8 -*-
import getopt
import os
import tkinter.messagebox
import tkinter as tk
import requests
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
import zipfile
import sys
import re

class downwin_class(object):
    def __init__(self,now_version,new_version):
        # 下载新版本zip的地址
        self.url_down = 'http://soft.sanmoo.com:8080/update/{}'
        # 创建主窗口
        self.window = tk.Tk()
        # 设置标题
        self.window.title('发现新版本')
        self.window.iconbitmap('./download.ico')
        # 得到屏幕宽、高
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        # 设置窗口大小及位置
        ww = 380
        wh = 100
        x = (sw - ww) / 2
        y = (sh - wh * 3) / 2
        self.window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.window.resizable(width=False, height=False)

        # 说明文字
        self.label_text = tk.Label(self.window, text='正在更新版本！')
        self.label_text.place(x=20, y=20)
        # 更新包文字
        self.label_update = tk.Label(self.window, text='更新包：')
        self.label_update.place(x=270, y=20)
        # 更新数文字
        self.label_update_count = tk.Label(self.window, text='0/0')
        self.label_update_count.place(x=325, y=20)
        # 创建一个白底画布，作为进度条的底槽
        self.canvas = tk.Canvas(self.window, width=300, height=16, bg="white")
        self.canvas.place(x=20, y=50)

        # 百分比文字
        self.label_percentage = tk.Label(self.window, text='0%')
        self.label_percentage.place(x=325, y=50)

        # 下载按钮
        # self.btn_download = tk.Button(self.window, text='开始下载', command=lambda: self.usr_download(self.url_down))
        # self.btn_download.place(x=365, y=45)
        self.window.update()
        for i in range(1,new_version-now_version+1):
            try:
                self.clean_progressbar()
                update_count = str(i)+'/'+str(new_version-now_version)
                self.label_update_count.config(text=str(update_count))
                self.window.update()
                A = list(str(now_version +i))[0]
                B = list(str(now_version +i))[1]
                C = list(str(now_version +i))[2]
                D = list(str(now_version +i))[3]
                zipName = 'dig_word_update{}.{}.{}.{}.zip'.format(A,B,C,D)
                if self.usr_download(self.url_down.format(zipName)):
                    zfile = zipfile.ZipFile("./{}".format(zipName), "r")
                    zfile.extractall()
                    zfile.close()
            except Exception as e:
                pass
            finally:
                if os.path.exists("./{}".format(zipName)):
                    os.remove("./{}".format(zipName))
        tkinter.messagebox.showinfo('提示', '更新完成,请重新开启软件！')
        self.window.destroy()
        self.window.mainloop()

    # 下载按钮函数
    def usr_download(self, url):
        try:
            # 点击按钮后把按钮设置为不可用
            # self.btn_download.config(text='正在下载', state=tk.DISABLED)
            # stream=True表示请求成功后并不会立即开始下载，而是在调用iter_content方法之后才会开始下载
            response = requests.get(url, verify=False, stream=True)
            chunk_size = 1024000  # 设置每次下载的块大小
            content_size = int(response.headers['content-length'])  # 从返回的response的headers中获取文件大小
            raise_data = chunk_size / content_size * 300  # 每次下载，进度条增量大小

            # 将下载的数据写入文件
            with open(url.split('/')[-1], 'wb') as f:
                n = 0
                for data in response.iter_content(chunk_size=chunk_size):  # 在循环读取文件时，刷新进度条
                    f.write(data)
                    n = n + raise_data
                    # 循环改变进度条的大小，实现进度条效果
                    # 画布上画一个矩形，作为进度条对象
                    fill_line = self.canvas.create_rectangle(0, 0, 0, 0, width=0, fill="green")
                    self.canvas.coords(fill_line, (0, 0, n, 18))
                    # 循环改变百分比文字
                    text = int(n / 3)
                    if text >= 100:
                        text = 100
                    self.label_percentage.config(text=str(text) + '%')
                    # 刷新窗口
                    self.window.update()
            return True
        except Exception as e:
            return False

    # 清空进度条
    def clean_progressbar(self):
        # 清空进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
        x = 500  # 未知变量，可更改
        n = 600 / x  # 465是矩形填充满的次数

        for t in range(x):
            n = n + 600 / x
            # 以矩形的长度作为变量值更新
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.window.update()

def main(now_version,new_version):
    try:
        serverName = 'dig_word_update_Server'
        socket = QLocalSocket()
        socket.connectToServer(serverName)
        # 如果连接成功，表明server已经存在，当前已有实例在运行
        if socket.waitForConnected(500):
            pass
        else:
            localServer = QLocalServer()  # 没有实例运行，创建服务器
            localServer.listen(serverName)
            # 处理其他
            downwin_class(now_version,new_version)
    except:
        pass

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:")
        result = re.search('now_version=(.*?),new_version=(.*?);',opts[0][1])
        now_version = result[1].replace('.','')
        new_version = result[2].replace('.','')
        main(int(now_version),int(new_version))
    except Exception as e:
        print(e)
        pass
