#这个程序的结构为，读取保存在剪贴板中的图片或者截图，然后调用百度的API，提取图片中的所有文字，然后再将提取出来的所有文字通过翻译的API进行翻译，最后显示翻译结果
#2.0：增加程序的容错能力
#打包为可执行文件.
#使用方法：后台点击运行之后，前台选择或者截取需要翻译的图片后，按下“Ctrl + Alt + z”之后，进行翻译

import hashlib
import json
import os
import time
import tkinter as tk
from datetime import datetime
from urllib import parse, request
import tkinter.font as tkFont
import keyboard
from aip import AipOcr
from PIL import ImageGrab


def  filerm(filename):
    try:
        os.remove(filename)
    except Exception as identifier:
        pass


def translate_Word(en_str):
    URL='http://api.fanyi.baidu.com/api/trans/vip/translate'
    From_Data={}  #创建From_Data字典，存储向服务器发送的data
    From_Data['from']='en'
    From_Data['to']='zh'
    From_Data['q']=en_str     #要翻译的数据
    From_Data['appid']='20200201000379206'       #申请的APPID
    From_Data['salt']='1435660288'        #随机数
    Key='IPVf3pjpSPJ8mcsEj2bB'                    #平台分配的密匙
    m=From_Data['appid']+en_str+From_Data['salt']+Key
    m_MD5=hashlib.md5(m.encode('utf8'))
    From_Data['sign']=m_MD5.hexdigest()

    data=parse.urlencode(From_Data).encode('utf-8')
                                                  #使用urlencode()方法转换标准格式
    response=request.urlopen(URL,data)            #传递request对象和转换完格式的数据
    html=response.read().decode('utf-8')          #读取信息并解码
    translate_results=json.loads(html)            #使用JSON
    #print(translate_results)                      #打印出JSON数据
    translate_results=translate_results['trans_result'][0]['dst']   #找到翻译结果

    print('翻译的结果是: %s'%translate_results)               #打印翻译信息
    return translate_results




def screen_shot():
    #截图的热键，个人根据自己的设置更改就好
    try:
        if not keyboard.wait(hotkey='ctrl+shift+z'):
            time.sleep(0.1)
            image=ImageGrab.grabclipboard()
            imagename = nameProcessing()
            image.save(imagename)
            return imagename 
    except Exception as identifier:
        show_result('Cannot find the target image or screenshot!\n','未获取到需要识别的图片')

#处理文件名         
def nameProcessing():
    timepoint = str(datetime.now()).split(' ')
    imagename = 'ScreenShot'+timepoint[0]
    filepath = './'+imagename +'.png'
    number = 0 
    while  os.path.exists(filepath):
        number += 1
        filepath = './'+imagename + '_' +str(number) +'.png'
        continue 
    return filepath 

#调用接口进行识别
def get_file_content(filepath):
    all_text=''
    with open(filepath,'rb') as f:
        image=f.read()
    f.close()
    APP_ID = '18353385'
    API_KEY = '4LGd8EGwMnZ0a04VYaTCkYVM'
    SECRET_KEY = 'h0bd7kqd6zZdIbTnNelgfC4e1ldjxOXV'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    req=client.basicGeneral(image)
    for i in req['words_result']:
        all_text+=i['words']+' '
    filerm(filepath)
    return all_text

#对识别之后的文字进行处理
def strProcessing(string):
    #a = string + translate_Word(string)
    en_str = string +'\n'+'-----------------\n'
    cn_str = translate_Word(string)
    #print('--------------')
    show_result(en_str,cn_str)

    
def main():
    filepath = screen_shot()
    try:
        string=get_file_content(filepath)
        str = strProcessing(string)
    except Exception as identifier:
        show_result('404---An unknown error happened！\n','调用API失败,请检查是否为网络原因')





def show_result(en_str,cn_str):
    win = tk.Tk()
    #win.geometry("100x50")
    #win.maxsize('500x800')
    try:
        ft = tkFont.Font(family='华文中宋', size=12)
        ft1 = tkFont.Font(family='Futura',size=15)
        ft2 = tkFont.Font(size=10, weight=tkFont.BOLD, underline=1, overstrike=1)
    except Exception as identifier:
        ft = tkFont.Font(size=12)
        ft1 = tkFont.Font(size=15)

    win.title("Translation Result ")
    win.maxsize(500,800) 
    t = tk.Text(win)
    sc = tk.Scrollbar()  # 滚动条
    sc.pack(side=tk.RIGHT, fill=tk.Y)
    t.pack(side=tk.LEFT, fill=tk.Y)
    sc.config(command=t.yview)
    t.config(yscrollcommand=sc.set)
    t.tag_configure('en', font=ft1)
    t.tag_configure('cn', font=ft)    
    t.insert(tk.INSERT, en_str,'en')
    t.insert(tk.INSERT,cn_str,'cn')
    win.wm_attributes('-topmost',1)
    win.mainloop()






if __name__=='__main__':
    number = 0 
    mark = True 
    while mark :
        number +=1
        if number ==20:
            mark =False
        main()




