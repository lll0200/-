# -*- codeing = utf-8 -*-
# @Time :2021/6/3 21:45
# @Author : 刘念卿
# @File : shumeipai_sever.py
# @Software : PyCharm
import socket
import sys
import RPi.GPIO

# 指定GPIO口的选定模式为GPIO引脚扁号模式
RPi.GPIO.setmode(RPi.GPIO.BCM)
# 指定GPIO18的模式为输出模式
RPi.GPIO.setup(18, RPi.GPIO.OUT)
pwm = RPi.GPIO.PWM(18, 70)


def socket_service_data():
    ##获取服务端的地址
    # host = socket.gethostname()
    host = '192.168.63.101'
    # 打印服务器主机名称
    print("当前服务器主机名称为:", host)

    port = 1234
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))  # 在同一台主机的ip下使用测试ip进行通信
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection..................")
    num = 50
    while True:
        sock, addr = s.accept()
        print('connection success', addr[0])
        buf = sock.recv(1024)  # 接收数据
        buf = buf.decode()  # 解码
        print("客户端发来的消息" + str(buf))
        print('num:', num)
        if str(buf) == "on":
            RPi.GPIO.output(18, True)  # 让GPIO输出高电平
            # 启用 PWM，参数是占空比（可以理解为电流大小），范围：0.0 <= 占空比 >= 100.0
            pwm.start(50)
        elif str(buf) == "off":
            RPi.GPIO.output(18, False)  # 让GPIO输出高电平
            # 停用 PWM
            pwm.stop()
        elif str(buf) == '+':
            if num in range(101):
                try:
                    num += 10
                    pwm.ChangeDutyCycle(num)
                except ValueError:
                    num = 100
            else:
                sock.sendall('error'.encode('utf-8'))
        elif str(buf) == '-':
            if num in range(101):
                try:
                    num -= 10
                    pwm.ChangeDutyCycle(num)
                except ValueError:
                    num = 0
        else:
            print('error commond')


if __name__ == '__main__':
    socket_service_data()

