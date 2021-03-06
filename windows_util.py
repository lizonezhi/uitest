#!/usr/bin/env python
# coding=utf-8

import psutil
import win32clipboard as w
import win32api
import win32con
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST
from ctypes import *
import ctypes
import time
import os
import re
import sys
import socket
from uitest import popen_close
import platform
from psutil import net_if_addrs
import serial
import serial.tools.list_ports


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


class WindowsAutomator:
    """
        use:
        mouse_click(500, 280)
        str1 = 'str'
        key_input(str1)
        time.sleep(4)
        mouse_click(1400, 100)
        win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
    """

    def __init__(self):
        pass

    @property
    def VK_CODE(self):
        VK_CODE = {
            'backspace': 0x08,
            'tab': 0x09,
            'clear': 0x0C,
            'enter': 0x0D,
            'shift': 0x10,
            'ctrl': 0x11,
            'alt': 0x12,
            'pause': 0x13,
            'caps_lock': 0x14,
            'esc': 0x1B,
            'spacebar': 0x20,
            'page_up': 0x21,
            'page_down': 0x22,
            'end': 0x23,
            'home': 0x24,
            'left_arrow': 0x25,
            'up_arrow': 0x26,
            'right_arrow': 0x27,
            'down_arrow': 0x28,
            'select': 0x29,
            'print': 0x2A,
            'execute': 0x2B,
            'print_screen': 0x2C,
            'ins': 0x2D,
            'del': 0x2E,
            'help': 0x2F,
            '0': 0x30,
            '1': 0x31,
            '2': 0x32,
            '3': 0x33,
            '4': 0x34,
            '5': 0x35,
            '6': 0x36,
            '7': 0x37,
            '8': 0x38,
            '9': 0x39,
            'a': 0x41,
            'b': 0x42,
            'c': 0x43,
            'd': 0x44,
            'e': 0x45,
            'f': 0x46,
            'g': 0x47,
            'h': 0x48,
            'i': 0x49,
            'j': 0x4A,
            'k': 0x4B,
            'l': 0x4C,
            'm': 0x4D,
            'n': 0x4E,
            'o': 0x4F,
            'p': 0x50,
            'q': 0x51,
            'r': 0x52,
            's': 0x53,
            't': 0x54,
            'u': 0x55,
            'v': 0x56,
            'w': 0x57,
            'x': 0x58,
            'y': 0x59,
            'z': 0x5A,
            'numpad_0': 0x60,
            'numpad_1': 0x61,
            'numpad_2': 0x62,
            'numpad_3': 0x63,
            'numpad_4': 0x64,
            'numpad_5': 0x65,
            'numpad_6': 0x66,
            'numpad_7': 0x67,
            'numpad_8': 0x68,
            'numpad_9': 0x69,
            'multiply_key': 0x6A,
            'add_key': 0x6B,
            'separator_key': 0x6C,
            'subtract_key': 0x6D,
            'decimal_key': 0x6E,
            'divide_key': 0x6F,
            'F1': 0x70,
            'F2': 0x71,
            'F3': 0x72,
            'F4': 0x73,
            'F5': 0x74,
            'F6': 0x75,
            'F7': 0x76,
            'F8': 0x77,
            'F9': 0x78,
            'F10': 0x79,
            'F11': 0x7A,
            'F12': 0x7B,
            'F13': 0x7C,
            'F14': 0x7D,
            'F15': 0x7E,
            'F16': 0x7F,
            'F17': 0x80,
            'F18': 0x81,
            'F19': 0x82,
            'F20': 0x83,
            'F21': 0x84,
            'F22': 0x85,
            'F23': 0x86,
            'F24': 0x87,
            'num_lock': 0x90,
            'scroll_lock': 0x91,
            'left_shift': 0xA0,
            'right_shift ': 0xA1,
            'left_control': 0xA2,
            'right_control': 0xA3,
            'left_menu': 0xA4,
            'right_menu': 0xA5,
            'browser_back': 0xA6,
            'browser_forward': 0xA7,
            'browser_refresh': 0xA8,
            'browser_stop': 0xA9,
            'browser_search': 0xAA,
            'browser_favorites': 0xAB,
            'browser_start_and_home': 0xAC,
            'volume_mute': 0xAD,
            'volume_Down': 0xAE,
            'volume_up': 0xAF,
            'next_track': 0xB0,
            'previous_track': 0xB1,
            'stop_media': 0xB2,
            'play/pause_media': 0xB3,
            'start_mail': 0xB4,
            'select_media': 0xB5,
            'start_application_1': 0xB6,
            'start_application_2': 0xB7,
            'attn_key': 0xF6,
            'crsel_key': 0xF7,
            'exsel_key': 0xF8,
            'play_key': 0xFA,
            'zoom_key': 0xFB,
            'clear_key': 0xFE,
            '+': 0xBB,
            ',': 0xBC,
            '-': 0xBD,
            '.': 0xBE,
            '/': 0xBF,
            '`': 0xC0,
            ';': 0xBA,
            '[': 0xDB,
            '\\': 0xDC,
            ']': 0xDD,
            "'": 0xDE,
            '`': 0xC0
        }
        return VK_CODE

    def get_mouse_point(self):
        po = POINT()
        windll.user32.GetCursorPos(byref(po))
        return int(po.x), int(po.y)

    def mouse_click(self, x=None, y=None):
        if not x is None and not y is None:
            self.mouse_move(x, y)
            time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_dclick(self, x=None, y=None):
        if not x is None and not y is None:
            self.mouse_move(x, y)
            time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_move(self, x, y):
        windll.user32.SetCursorPos(x, y)

    def key_input(self, str=''):
        for c in str:
            win32api.keybd_event(self.VK_CODE[c], 0, 0, 0)
            win32api.keybd_event(self.VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.01)

    # 按键事件
    def key_event(self, KEY_CODE):
        # 按下
        win32api.keybd_event(KEY_CODE, 0, 0, 0)
        # 抬起
        win32api.keybd_event(KEY_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 按回车键
    def key_event_enter(self):
        self.key_event(self.VK_CODE['enter'])

class Log(object):
    '''
        打日志
        use：
            from uitest import windows_util
            Log = windows_util.Log(is_show=True)
            Log.i('信息')
    '''


    def __init__(self, path='log/', is_show=True):
        self.path = path
        self.is_show = is_show
        self.Level_debug = '调试'
        self.Level_info = '信息'
        self.Level_warning = '警告'
        self.Level_error = '错误'

    def __print_log(self, content, Level='debug', is_show=False):
        '''
        写入内容到电脑本地txt文件，指定路径
        :param name:文件名  content：内容
        '''
        try:
            # 获取今天的字符串
            time_ymd = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            time_ymdhms = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            msg = time_ymdhms + " " + Level + "  ：" + content + '\n'

            if Level == self.Level_debug:
                self.print_color(msg, color=7)
                WindowsUtil().write_txt_file(name=time_ymd, content=msg, path=self.path)
            elif is_show:
                if Level == self.Level_info:
                    self.print_color(msg, color=17)
                elif Level == self.Level_warning:
                    self.print_color(msg, color=19)
                elif Level == self.Level_error:
                    self.print_color(msg, color=18)
                WindowsUtil().write_txt_file(name=time_ymd, content=msg, path=self.path)
            return True
        except Exception as e:
            self.print_color(e.args, color=18)
            return False

    def d(self, content):
        self.__print_log(content=content, Level=self.Level_debug, is_show=True)

    def i(self, content):
        self.__print_log(content=content, Level=self.Level_info, is_show=self.is_show)

    def w(self, content):
        self.__print_log(content=content, Level=self.Level_warning, is_show=self.is_show)

    def e(self, content):
        self.__print_log(content=content, Level=self.Level_error, is_show=self.is_show)

    # 打印带颜色的字
    def print_color(self, text, color=19):
        '''
        Windows CMD命令行颜色
        :param text: 打印的文字
        :param color:  1蓝字 2绿字 4红色 6黄色 7白色 ，默认黄色（加亮）
        :usage: uitest.print_color('你好', 2)
        '''
        # 句柄号
        STD_INPUT_HANDLE = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12

        # 背景色
        BACKGROUND_BLUE = 0x10  # 蓝
        BACKGROUND_GREEN = 0x20  # 绿
        BACKGROUND_RED = 0x40  # 红
        BACKGROUND_INTENSITY = 0x80  # 加亮

        # 前景色
        FOREGROUND_BLACK = 0x0  # 黑
        FOREGROUND_BLUE = 0x01  # 蓝
        FOREGROUND_GREEN = 0x02  # 绿
        FOREGROUND_RED = 0x04  # 红
        FOREGROUND_INTENSITY = 0x08  # 加亮
        黑色 = 0x00
        蓝色 = 0x01
        绿色 = 0x02
        湖蓝色 = 0x03
        红色 = 0x04
        紫色 = 0x05
        黄色 = 0x06
        白色 = 0x07
        灰色 = 0x08  # 加亮
        淡蓝色 = 0x09
        淡绿色 = 0x0A
        淡浅绿色 = 0x0B
        淡红色 = 0x0C
        淡紫色 = 0x0D
        淡黄色 = 0x0E
        亮白色 = 0x0F
        colors2 = [
            黑色,
            蓝色,
            绿色,
            湖蓝色,
            红色,
            紫色,
            黄色,
            白色,
            灰色,
            淡蓝色,
            淡绿色,
            淡浅绿色,
            淡红色,
            淡紫色,
            淡黄色,
            亮白色,
            FOREGROUND_BLUE | FOREGROUND_INTENSITY,  # 蓝字(加亮)16
            FOREGROUND_GREEN | FOREGROUND_INTENSITY,  # 绿字(加亮)17
            FOREGROUND_RED | FOREGROUND_INTENSITY,  # 红字(加亮)18
            黄色 | FOREGROUND_INTENSITY,  # 黄字(加亮)19
            绿色 | FOREGROUND_INTENSITY,  # 绿字(加亮)20
            FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_BLUE | BACKGROUND_INTENSITY  # 红字蓝底21
        ]
        #http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp for information on Windows APIs.

        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        def set_cmd_color(color, handle=std_out_handle):
            bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
            return bool

        def reset_color():
            set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

        def print_color_text(text, color):
            set_cmd_color(color)
            sys.stdout.write('%s\n' % text)  # ==> print(text)
            reset_color()

        print_color_text(text, colors2[color])

class WindowsUtil:

    def get_local_ip(self, LAN=False, get_list=False):
        '''
            获取电脑本地ip地址
            LAN = True 时表示获取192.168开头的局域网ip
        '''
        ip = ''
        ip_list = []
        try:
            for k, v, in psutil.net_if_addrs().items():
                if "无线" in k or "WLAN" in k or "以太" in k:
                    for item in v:
                        ip_tmp = item[1]
                        try:
                            if LAN:
                                ip = re.search('(1[97]2)\.([\d]{1,3}\.){2}[\d]{1,3}', ip_tmp).group()
                            else:
                                ip = re.search('([\d]{1,3}\.){3}[\d]{1,3}', ip_tmp).group()
                            ip_list.append(ip)
                            if ip and not get_list:
                                break
                        except:
                            pass
        except Exception as e:
            print('Exception:' + e.args)
        if get_list:
            return ip_list
        else:
            return ip

    def get_host_ip(self):
        """
        查询本机局域网ip地址
        windows和Linux系统下均可正确获取IP地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    def get_host_name(self):
        '''
        获取本机计算机名称
        :return:
        '''
        hostname = socket.gethostname()
        return hostname

    def get_host_ip_by_name(self):
        '''
        根据本机计算机名称获取ip，不是局域网ip
        :return:
        '''
        ip = socket.gethostbyname(self.get_host_name())
        return ip

    def write_txt_file(self, name='name', content='content', path=''):
        '''
        写入内容到电脑本地txt文件
        :param name:文件名  content：内容
        :return: True or False 写入成功或失败
        ：usage： write_txt_file(name='记录日志', content='123')
        '''
        try:
            if path:
                if not os.path.isdir(path):
                    os.makedirs(path, exist_ok=True)
                f = open(path + '%s.log' % (name), 'a')
                f.write('%s \n' % (content))
                f.close()
            else:
                f = open('%s.txt' % (name), 'a')
                f.write('%s \n' % (content))
                f.close()

            return True
        except:
            return False

    def read_txt_file(self, filename='filename'):
        '''
        读取电脑本地文本文件
        :param filename:文件名  content：内容
        :return: 文本内容
        ：usage： read_txt_file(filename='记录日志')
        '''
        try:
            list1 = []
            f = open('%s' % (filename))
            with open(filename, 'r') as f:
                line = ''
                for i in f.readlines():
                    list1.append(i)
                f.close()
            return list1
        except Exception as e:
            Log().e(str(e))
            return ''

    def hide_window(self, use_ctypes=False):
        '''
            隐藏cmd窗口
        '''
        if use_ctypes:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
                ctypes.windll.kernel32.CloseHandle(whnd)
        else:
            ct = win32api.GetConsoleTitle()
            hd = win32gui.FindWindow(0, ct)
            win32gui.ShowWindow(hd, 0)
    def show_window(self, use_ctypes=False):
        '''
            显示cmd窗口
        '''
        if use_ctypes:
            pass
        else:
            ct = win32api.GetConsoleTitle()
            hd = win32gui.FindWindow(0, ct)
            win32gui.ShowWindow(hd, 1)

    def setText(self, aString):
        '''
            写入剪切板
        '''
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
        w.CloseClipboard()

    def pasteText(self):
        '''
            自动粘贴剪切板中的内容
        '''
        win32api.keybd_event(17, 0, 0, 0)  # ctrl的键位码是17
        win32api.keybd_event(86, 0, 0, 0)  # v的键位码是86
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

    def write(self, data):
        length = win32gui.GetWindowTextLength(self.handle)
        win32gui.SendMessage(self.handle, win32con.EM_SETSEL, length, length)
        win32gui.SendMessage(self.handle, win32con.EM_REPLACESEL, False, data)

    def get_new_file_name(self, path, file_name):
        '''
            返回重命名的文件名,按照（1）（1）格式拼接，保存文件时用
            path: 扫描的目录
            file_name：文件名
        '''
        g = os.walk(path)
        file_name_list = []
        for path, dir_list, file_list in g:
            for file_list_name in file_list:
                file_name_list.append(str(file_list_name))

        new_file_name = file_name
        count = 0
        while new_file_name in file_name_list:
            count = count + 1
            new_file_name_split = new_file_name.split('.')
            tail = ''
            file_name_body = ''
            file_name_tail = ''
            if len(new_file_name_split) > 1:
                tail = new_file_name_split[-1]
                file_name_body = new_file_name[:-(len(tail) + 1)]
                file_name_tail = '.' + tail
            else:
                file_name_body = new_file_name
            new_file_name = file_name_body + '（' + str(count) + '）' + file_name_tail
        return new_file_name

    def get_current_connect_wifi_ssid(self):
        '''
            获取当前连接的WiFi名称
        '''
        cmd = 'netsh WLAN show interfaces'
        scanoutput_list = popen_close(cmd)
        currentSSID = ''
        for i in scanoutput_list:
            if 'SSID' in i:
                currentSSID = i
                break
        if currentSSID:
            currentSSID = currentSSID.split(':')[1].replace('\n', '').replace('\r', '').strip()
        return currentSSID

    def get_current_connect_wifi_authentication(self):
        '''
            获取当前连接的WiFi的身份验证（加密方式， 如：wpa）
        '''
        cmd = 'netsh WLAN show interfaces'
        scanoutput_list = popen_close(cmd)
        current_authentication = ''
        for i in scanoutput_list:
            if '身份验证' in i:
                current_authentication = i
                break
        current_authentication = current_authentication.split(':')[1].replace('\n', '').replace('\r', '').strip()
        current_authentication = current_authentication.upper()
        if current_authentication.startswith("WPA"):
            current_authentication = 'WPA'
        elif current_authentication.startswith("WEP"):
            current_authentication = 'WEP'
        return current_authentication

    def get_wifi_password(self, ssid=None):
        '''
            获取WiFi密码
        '''
        if not ssid:
            # 默认获取当前连接的wifi密码
            ssid = self.get_current_connect_wifi_ssid()
        cmd = 'netsh wlan show profile name="%s" key=clear' % (ssid)
        currentSSID_password_all_info_list = popen_close(cmd)
        currentSSID_password = ''
        for i in currentSSID_password_all_info_list:
            if '关键内容' in i:
                currentSSID_password = i
                break
        if currentSSID_password:
            currentSSID_password = currentSSID_password.split(':')[1].replace('\n', '').replace('\r', '').strip()
        return currentSSID_password

    def get_mac_address(self):
        '''
            获取蓝牙 MAC 地址
        '''
        mac_address = ''
        if platform.system() == 'Darwin':
            address = popen_close('system_profiler SPBluetoothDataType | grep Address:')[0].replace(' ',
                                                                                                             '')
            mac_address = re.search(r"\w\w-\w\w-\w\w-\w\w-\w\w-\w\w", address).group()
            mac_address = mac_address.replace("-", ":")
        else:
            for k, v, in net_if_addrs().items():
                if "蓝牙" in k or "bluetooth" in k or "Bluetooth" in k:
                    for item in v:
                        address = item[1]
                        if '-' in address and len(address) == 17:
                            mac_address = address.replace("-", ":")
                            break
        return mac_address
    
    def get_bluetooth_com_list(self):
        '''
            获取蓝牙串口 COM 端口号列表
        '''
        plist = list(serial.tools.list_ports.comports())
        com_list = []
        if len(plist) > 0:
            for i in plist:
                serialName = i[0]
                # serialFd = serial.Serial(serialName, 9600, timeout=60)
                if i[1].find('蓝牙') >= 0 or i[1].find('Bluetooth') >= 0 or i[1].find('bluetooth') >= 0:
                    com_list.append(serialName)
        return com_list
