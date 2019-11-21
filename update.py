# -*- coding: utf-8 -*-

import tkinter.messagebox
import requests
import re
import configparser
import os

# VERSION_NOW='100'#1.0.0
# UPDATE_DOWNLOAD_URL='http://www.url.com/a.zip' #新版本文件
# VERSION_URL='http://www.url.com/version'#最新版本号

# try:
#     ver=request.get(VERSION_URL)#获取最新版本号
#    #然后自己根据版本号对版本进行对比处理
#     #这里省略
#     #直接跳到更新代码
#     tkinter.messagebox.showwarning(title='提示', message='发现新版本，点击确定开始更新。更新时间跟网速有关，请耐心等待！')
#     newFile=requests.get(UPDATE_DOWNLOAD_URL)
#         with open("newFile_update.zip","wb") as fp:
#             fp.write(newFile.content)
# except:
#     tkinter.messagebox.showwarning(title='警告', message='更新失败，请检查网络！')
#     tkinter.messagebox.showwarning(title='提示', message='新版本软件下载完成！请在当前软件目录查看(文件名：newFile_update.zip)并使用新版本。')





try:
    url_ver = 'http://soft.sanmoo.com:8080/index.html'
    url_down = 'http://soft.sanmoo.com:8080/down/%E5%86%B0%E5%B1%B1%E6%8C%96%E8%AF%8D.zip'


    response = requests.get(url_ver)
    result = re.search('<Verson>(.*?)</Verson>',response.text)
    verson_server = result[1]

    cf = configparser.RawConfigParser()
    cf.read("./config.ini", encoding='GBK')
    verson_local = cf.get('setting','verson')

    if verson_server == verson_local:
        main = "web.exe"
        os.system(main)
    else:
        tkinter.messagebox.showinfo('发现新版本，点击确定开始更新。')
        response_zip = requests.get('url_down')
        with open('QT_web.zip','wb') as f:
            f.write(response_zip.content)
except Exception as e:
    tkinter.messagebox.showinfo(e)
    pass