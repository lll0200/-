# -*- codeing = utf-8 -*-
# @Time :2021/6/3 7:59
# @Author : 刘念卿
# @File : shumeipia_client.py
# @Software : PyCharm
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import socket

Builder.load_string("""
#:import gmtime time.gmtime
#:import strftime time.strftime
<RootWidget>
    canvas:
        Color:
            rgba: (0.1, 0.5, 0.9, 0.9) # green
        Rectangle:
            size: self.size
            pos: self.pos
            #source: image_name
    FloatLayout:
        orientation: 'vertical'
        Label:
            id: label
            text: 'connect'
            pos_hint: {"right":0.65}

        Button:
            id: on
            color: 0,1,0,1
            background_color: 1.0, 0.0, 0.0, 1.0  #背景色设置
            font_size: 5
            size_hint: 0.15,0.05
            on_release: root.on()
            text: "Led_on"
            font_size: 20
            pos_hint: {"right":0.7, "bottom":0.2,"top":0.8,"left":0.3}
        Button:
            id: off
            color: 0,1,0,1
            background_color: 1.0, 0.0, 0.0, 1.0  #背景色设置
            font_size: 5
            size_hint: 0.15,0.05
            on_release: root.off()
            text: "Led_off"
            font_size: 20
            pos_hint: {"right":0.45, "bottom":0.2,"top":0.8,"left":0.55}
        Button:
            id: bright
            color: 0,1,0,1
            background_color: 0.5 ,0.6, 1, 1.0  #背景色设置
            font_size: 5
            size_hint: 0.15,0.05
            on_release: root.bright()
            text: "Brighten"
            font_size: 20
            pos_hint: {"right":0.7, "bottom":0.4,"top":0.6,"left":0.3}

        Button:
            id: darken
            color: 0,1,0,1
            background_color: 0.5, 0.6, 1, 1.0  #背景色设置
            font_size: 5
            size_hint: 0.15,0.05
            on_release: root.darken()
            text: "Darken"
            font_size: 20
            pos_hint: {"right":0.45, "bottom":0.4,"top":0.6,"left":0.55}
        Button:
            id: ex
            color: 0,1,0,1
            background_color: 6, 0, 0, 1  #背景色设置
            font_size: 5
            size_hint: 0.15,0.05
            on_release: root.exit()
            text: "exit"
            font_size: 20
            pos_hint: {"right":0.56, "bottom":0.6,"top":0.4,"left":0.44}
                    
""")


class RootWidget(Screen):
    """
    on:开灯
    off:关灯
    bright:调亮 每次亮度+10 最大值为100
    darken:调暗 每次亮度-10 最小值为0
    _socket:发送套接字
    """
    def __init__(self,**kwargs):
        self.host='192.168.63.101'
        self.port=1234
        self.commond='waiting'
        super(RootWidget,self).__init__(**kwargs)
        self.ids['label'].text='connect ip:'+self.host


    @staticmethod
    def lianjie():
        print("ok")

    def _socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器
        s.connect((self.host, self.port))
        s.send(self.commond.encode('utf-8'))
        s.close()

    def on(self):
        self.commond='on'
        self._socket()
        print('on')

    def off(self):
        self.commond='off'
        self._socket()
        print('off')

    def bright(self):
        self.commond = '+'
        self._socket()
        print('bright')

    def darken(self):
        self.commond = '-'
        self._socket()
        print('darken')

    def exit(self):
        self.ids['ex'].text='again'
        self.ids['ex'].bind(on_press=exit)

class TestApp(App):
    def __init__(self,**kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title='树莓派控制' #修改窗口名称
    def build(self):

        return RootWidget()

if __name__ == '__main__':
    TestApp().run()