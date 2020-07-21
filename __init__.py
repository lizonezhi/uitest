#!/usr/bin/env python
# coding=utf-8

__author__ = "lzz"
'''
参考：
https://github.com/openatx/uiautomator2
https://github.com/gb112211/Adb-For-Test
项目地址：https://github.com/lizonezhi/uitest
支持python3.6
目前功能无需在手机上装任何程序
'''
import tempfile
import os
import sys
import platform
import subprocess
import re
import time
import datetime

import xml.etree.cElementTree as ET

command = 'adb'
fastboot = 'fastboot'
PATH = lambda p: os.path.abspath(p)

# 判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
# if system is "Windows":
#     find_util = "findstr"
# else:
#     find_util = "grep"
find_util = "findstr"
# # 判断是否设置环境变量ANDROID_HOME
# if "ANDROID_HOME" in os.environ:
#     if system == "Windows":
#         command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
#     else:
#         command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
# else:
#     raise EnvironmentError(
#         "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])

def getUdid():
    '''
    :return:adb devices 返回的第一个设备 
    '''
    try:
        '''''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = subprocess.check_output('%s devices' % (command)).decode().split("\r\n")
        adb_first_start = False
        for i in deviceInfo:
            if 'successfully' in i:
                adb_first_start = True
                break
        if adb_first_start:
            udid = 'device'.join(deviceInfo[3].split('device')[:1])
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[3] == '':
                return ''
            else:
                return udid.strip()
        else:
            udid='device'.join(deviceInfo[1].split('device')[:1])
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[1]=='':
                return ''
            else:
                return udid.strip()
    except:
        return ''
def get_sideload_udid_list():
    '''
    :return: sideload 界面的设备
    '''
    try:
        udid_list = []
        '''''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = subprocess.check_output('%s devices' % (command)).decode().split("\r\n")
        adb_first_start = False
        for i in deviceInfo:
            if 'successfully' in i:
                adb_first_start = True
                break
        if adb_first_start:
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[3] == '':
                return ''
            else:
                for i in range(3,11):
                    try:
                        j = '\tsideload'.join(deviceInfo[i].split('\tsideload')[:1])
                        udid_list.append(j)
                        if j == '' or 'device' in j or 'recovery' in j:
                            udid_list.remove(j)
                    except:
                        break
                return udid_list
        else:
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[1]=='':
                return ''
            else:
                for i in range(1,9):
                    try:
                        j = '\tsideload'.join(deviceInfo[i].split('\tsideload')[:1])
                        udid_list.append(j)
                        if j == '' or 'device' in j or 'recovery' in j:
                            udid_list.remove(j)
                    except:
                        break
                return udid_list
    except :
        return ''
def get_recovery_udid_list():
    '''
    :return: recovery 界面的设备
    '''
    try:
        udid_list = []
        '''''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = subprocess.check_output('%s devices' % (command)).decode().split("\r\n")
        adb_first_start = False
        for i in deviceInfo:
            if 'successfully' in i:
                adb_first_start = True
                break
        if adb_first_start:
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[3] == '':
                return ''
            else:
                for i in range(3,11):
                    try:
                        j = '\trecovery'.join(deviceInfo[i].split('\trecovery')[:1])
                        udid_list.append(j)
                        if j == '' or 'device' in j or 'sideload' in j:
                            udid_list.remove(j)
                    except:
                        break
                return udid_list
        else:
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[1]=='':
                return ''
            else:
                for i in range(1,9):
                    try:
                        j = '\trecovery'.join(deviceInfo[i].split('\trecovery')[:1])
                        udid_list.append(j)
                        if j == '' or 'device' in j or 'sideload' in j:
                            udid_list.remove(j)
                    except:
                        break
                return udid_list
    except :
        return ''
def get_fastboot_udid_list():
    '''
    :return: fastboot 界面的设备
    '''
    try:
        udid_list = []
        '''''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = subprocess.check_output('%s devices' % (fastboot)).decode().split("\r\n")
        if deviceInfo[0]=='':
            return ''
        else:
            for i in range(0,8):
                try:
                    j = '\tfastboot'.join(deviceInfo[i].split('\tfastboot')[:1])
                    udid_list.append(j)
                    if j == '':
                        udid_list.remove(j)
                except:
                    break
            return udid_list
    except :
        return ''
def get_udid_list():
    '''
    :return: adb devices 返回的设备(sideload和recovery界面除外)
    '''
    try:
        udid_list = []
        '''''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = subprocess.check_output('%s devices' % (command)).decode().split("\r\n")
        adb_first_start = False
        for i in deviceInfo:
            if 'successfully' in i:
                adb_first_start = True
                break
        if adb_first_start:
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[3] == '':
                return ''
            else:
                for i in range(3,11):
                    try:
                        j = '\tdevice'.join(deviceInfo[i].split('\tdevice')[:1])
                        udid_list.append(j)
                        if j == '' or 'sideload' in j or 'recovery' in j:
                            udid_list.remove(j)
                    except:
                        break
                return udid_list
        else:
            '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
            if deviceInfo[1]=='':
                return ''
            else:
                for i in range(1,9):
                    try:
                        j = '\tdevice'.join(deviceInfo[i].split('\tdevice')[:1])
                        udid_list.append(j)
                        if j == '' or 'sideload' in j or 'recovery' in j:
                            udid_list.remove(j)
                    except:
                        break
                return udid_list
    except :
        return ''
# 字节bytes转化kb\m\g
def formatSize(bytes, unit = 'm'):
    '''
    :param bytes: 
    :param unit= 'b','k','m','g'
    :return: 'b','k','m','g'
    '''
    try:
        bytes = float(bytes)
    except:
        print("传入的字节格式不对")
        return "Error"
    kb = bytes / 1024
    M = kb / 1024
    G = M / 1024
    if unit == 'b' or unit == 'bytes':
        return bytes
    elif unit == 'k' or unit == 'kb':
        return kb
    elif unit == 'm' or unit == 'mb':
        return M
    elif unit == 'g' or unit == 'gb':
        return G
# 获取文件大小
def getDocSize(path, unit='m'):
    '''
    :param bytes: 
    :param unit= 'b','k','m','g'
    :return: 'b','k','m','g'
    '''
    try:
        size = os.path.getsize(path)
        return formatSize(size, unit=unit)
    except Exception as err:
        print(err)
# 获取文件夹大小
def getFileSize(path, unit='m'):
    '''
    :param bytes: 
    :param unit= 'b','k','m','g'
    :return: 'b','k','m','g'
    '''
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize, unit=unit)
    except Exception as err:
        print(err)

# 倒计时
def time_remain(**kwargs):
    '''
    :param lineTmpla: 
    :param mins: 多少秒后停止
    :usage:  interface_show(title="倒计时demo", artist="内容", rate="内容", minutes=5) 
    '''
    lineTmpla = ' ' * 5 + kwargs['title'] + kwargs['artist'] + kwargs['rate'] + " %-3s"
    print(__time_remain(lineTmpla, kwargs['minutes']))
# 倒计时
def __time_remain(lineTmpla, mins):
    count = 0
    while (count < mins):
        count += 1
        n = mins - count
        time.sleep(1)
        sys.stdout.write("\r" + lineTmpla % (n), )
        sys.stdout.flush()
        if not n:
            return 'completed'

# 正计时
def time_jishi(**kwargs):
    '''
    :param lineTmpla: 
    :param mins: 多少秒后停止
    :usage:  time_jishi(title="计时demo", artist="内容", rate="") 
    '''
    lineTmpla = kwargs['str'] + " %s " + "秒"
    return __time_jishi(lineTmpla,
                        kwargs['udid_all'] if kwargs.get('udid_all') else '',
                        kwargs['device'] if kwargs.get('device') else '',
                        kwargs['recovery'] if kwargs.get('recovery') else '',
                        kwargs['sideload'] if kwargs.get('sideload') else '',
                        kwargs['fastboot'] if kwargs.get('fastboot') else '',
                        kwargs['timeout'] if kwargs.get('timeout') else 3600)
# 正计时
def __time_jishi(lineTmpla, udid_all, device, recovery, sideload, fastboot, timeout):
    start_time = time.time()
    count = 0
    if udid_all:
        while getUdid() == '':
            count += 1
            time.sleep(1)
            sys.stdout.write("\r" + lineTmpla % (count) )
            sys.stdout.flush()
            if time.time() - start_time > timeout:
                print_color('超时%s秒，自动退出' % (timeout), 4)
                break
    elif device:
        while len(get_udid_list()) == 0:
            count += 1
            time.sleep(1)
            sys.stdout.write("\r" + lineTmpla % (count) )
            sys.stdout.flush()
            if time.time() - start_time > timeout:
                print_color('超时%s秒，自动退出' % (timeout), 4)
                break
    elif recovery:
        while len(get_recovery_udid_list()) == 0:
            count += 1
            time.sleep(1)
            sys.stdout.write("\r" + lineTmpla % (count) )
            sys.stdout.flush()
            if time.time() - start_time > timeout:
                print_color('超时%s秒，自动退出' % (timeout), 4)
                break
    elif sideload:
        while len(get_sideload_udid_list()) == 0:
            count += 1
            time.sleep(1)
            sys.stdout.write("\r" + lineTmpla % (count) )
            sys.stdout.flush()
            if time.time() - start_time > timeout:
                print_color('超时%s秒，自动退出' % (timeout), 4)
                break
    elif fastboot:
        while len(get_fastboot_udid_list()) == 0:
            count += 1
            time.sleep(1)
            sys.stdout.write("\r" + lineTmpla % (count) )
            sys.stdout.flush()
            if time.time() - start_time > timeout:
                print_color('超时%s秒，自动退出' % (timeout), 4)
                break
def get_local_ip(LAN=False):
    '''
        获取电脑本地ip地址
        LAN = True 时表示获取192.168开头的局域网ip
    '''
    import psutil
    ip = ''
    try:
        for k, v, in psutil.net_if_addrs().items():
            if "无线" in k or "WLAN" in k or "以太" in k:
                for item in v:
                    ip_tmp = item[1]
                    try:
                        if LAN:
                            ip = re.search('(192)\.(168)\.([\d]{1,3}\.){1}[\d]{1,3}', ip_tmp).group()
                        else:
                            ip = re.search('([\d]{1,3}\.){3}[\d]{1,3}', ip_tmp).group()
                        if ip:
                            break
                    except:
                        pass
    except Exception as e:
        print('Exception:' + e.args)
    return ip
def print_log(content='content', path='log/'):
    '''
    写入内容到电脑本地txt文件，指定路径
    :param name:文件名  content：内容
    :return: True or False 写入成功或失败
    ：usage： write_txt_file(name='记录日志', content='123')
    '''
    try:
        # 获取今天的字符串
        time_ymd = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        time_ymdhms = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        msg = time_ymdhms + "  ：" + content + '\n'
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        f = open(path + '%s.log' % (time_ymd), 'a')
        f.write('%s \n' % (msg))
        f.close()
        return True
    except:
        return False
def write_txt_file(name='name', content='content'):
    '''
    写入内容到电脑本地txt文件
    :param name:文件名  content：内容
    :return: True or False 写入成功或失败
    ：usage： write_txt_file(name='记录日志', content='123')
    '''
    try:
        f = open('%s.txt' % (name), 'a')
        f.write('%s \n' % (content))
        f.close()
        return True
    except:
        return False
def read_txt_file(name='name'):
    '''
    写入文件到电脑本地
    :param name:文件名  content：内容
    :return: True or False 写入成功或失败
    ：usage： write_txt_file(name='记录日志', content='123')
    '''
    try:
        list1 = []
        f = open('%s.txt' % (name))
        line = f.readline()
        while line:
            line = f.readline().replace('\n', '')
            list1.append(line)
            if line == '':
                list1.remove('')
        f.close()
        return list1
    except:
        return ''
# 判断是否为数字
def is_number(s):
    '''
    判断是否由数字组成，包括小数
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
# 打印带颜色的字
def print_color(text, color=19):
    '''
    Windows CMD命令行颜色
    :param text: 打印的文字
    :param color:  1蓝字 2绿字 4红色 6黄色  ，默认黄色（加亮）
    :usage: uitest.print_color('你好', 2)
    '''
    import ctypes
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
# Helper for popen() -- a proxy for a file whose close waits for the process
class _wrap_close:
    def __init__(self, stream, proc):
        self._stream = stream
        self._proc = proc
    def close(self):
        self._stream.close()
        returncode = self._proc.wait()
        if returncode == 0:
            return None
        if name == 'nt':
            return returncode
        else:
            return returncode << 8  # Shift left to match old behavior
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()
    def __getattr__(self, name):
        return getattr(self._stream, name)
    def __iter__(self):
        return iter(self._stream)
def os_popen(cmd):
    '''
    重写os.popen()方法
    :param cmd: 
    :return: 
    usage： push_result = d.os_popen('-s %s push %s /data/local/tmp/tmp_apk.apk' % (udid, apk))
            此处可以运行其它命令
            push_result.close()
    '''
    if not isinstance(cmd, str):
        raise TypeError("invalid cmd type (%s, expected string)" % type(cmd))
    import io
    cmd = '%s %s' % (command, cmd)
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            bufsize=-1)
    return _wrap_close(io.TextIOWrapper(proc.stdout), proc)
class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class Element(object):
    """
    通过元素定位
    """

    def __init__(self, device_id=""):
        """
        初始化，获取系统临时文件存储目录，定义匹配数字模式
        """
        self.utils = Device(device_id)
        self.tempFile = tempfile.gettempdir()
        self.pattern = re.compile(r"\d+")

    def __uidump(self):
        """
        获取当前Activity的控件树
        """
        if int(self.utils.getSdkVersion()) >= 19:
            self.utils.shell("uiautomator dump --compressed /data/local/tmp/uidump.xml").wait()
        else:
            self.utils.shell("uiautomator dump /data/local/tmp/uidump.xml").wait()
        self.utils.adb("pull data/local/tmp/uidump.xml %s" % self.tempFile).wait()
        # self.utils.shell("rm /data/local/tmp/uidump.xml").wait()

    def __element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组，(x, y)
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        """
        Xpoint = None
        Ypoint = None

        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                # 获取元素所占区域坐标[x, y][x, y]
                bounds = elem.attrib["bounds"]

                # 通过正则获取坐标列表
                coord = self.pattern.findall(bounds)

                # 求取元素区域中心点坐标
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                break

        if Xpoint is None or Ypoint is None:
            raise Exception("Not found this element(%s) in current activity" % name)

        return (Xpoint, Ypoint)

    def d(self, attrib=None, name=None, **msg):
        """
        同属性单个元素，返回单个坐标元组，(x, y)
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        用法：d(resourceId='com.android.calculator2:id/op_mul')
             d(text='8')
             d(content_desc='乘')
        """
        textContains = False
        if attrib and name:
            attrib = attrib.replace('resourceId', 'resource-id').replace('description', 'content-desc')
        else:
            for attrib in msg:
                if msg.get('resourceId'):
                    attrib = 'resource-id'
                    name = msg['resourceId']
                    break
                if msg.get('text'):
                    attrib = 'text'
                    name = msg['text']
                    break
                if msg.get('content_desc'):
                    attrib = 'content-desc'
                    name = msg['content_desc']
                    break
                if msg.get('textContains'):
                    attrib = 'text'
                    name = msg['textContains']
                    textContains = True
                    break
        Xpoint = None
        Ypoint = None

        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if textContains:
                if name in elem.attrib[attrib]:
                    # 获取元素所占区域坐标[x, y][x, y]
                    bounds = elem.attrib["bounds"]

                    # 通过正则获取坐标列表
                    coord = self.pattern.findall(bounds)

                    # 求取元素区域中心点坐标
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    break
            else:
                if elem.attrib[attrib] == name:
                    # 获取元素所占区域坐标[x, y][x, y]
                    bounds = elem.attrib["bounds"]

                    # 通过正则获取坐标列表
                    coord = self.pattern.findall(bounds)

                    # 求取元素区域中心点坐标
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    break

        if Xpoint is None or Ypoint is None:
            return False
        else:
            return (Xpoint, Ypoint)
    def click(self, attrib=None, name=None, **msg):
        """
        同属性单个元素，返回是否存在
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        用法：d(resourceId='com.android.calculator2:id/op_mul')
             d(text='8')
             d(content_desc='乘')
        """
        textContains = False
        timeout = 1
        if attrib and name:
            attrib = attrib.replace('resourceId', 'resource-id').replace('description', 'content-desc')
        else:
            for attrib in msg:
                if msg.get('timeout'):
                    timeout = msg['timeout']
                if msg.get('resourceId'):
                    attrib = 'resource-id'
                    name = msg['resourceId']
                    break
                if msg.get('text'):
                    attrib = 'text'
                    name = msg['text']
                    break
                if msg.get('content_desc'):
                    attrib = 'content-desc'
                    name = msg['content_desc']
                    break
                if msg.get('className'):
                    attrib = 'class'
                    name = msg['className']
                    break
                if msg.get('textContains'):
                    attrib = 'text'
                    name = msg['textContains']
                    textContains = True
                    break
        Xpoint = None
        Ypoint = None
        startTime = time.time()
        while timeout:
            self.__uidump()
            tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if textContains:
                    if name in elem.attrib[attrib]:
                        # 获取元素所占区域坐标[x, y][x, y]
                        bounds = elem.attrib["bounds"]

                        # 通过正则获取坐标列表
                        coord = self.pattern.findall(bounds)

                        # 求取元素区域中心点坐标
                        Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                        Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                        timeout = 0
                        break
                else:
                    if elem.attrib[attrib] == name:
                        # 获取元素所占区域坐标[x, y][x, y]
                        bounds = elem.attrib["bounds"]

                        # 通过正则获取坐标列表
                        coord = self.pattern.findall(bounds)

                        # 求取元素区域中心点坐标
                        Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                        Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                        timeout = 0
                        break
            if time.time() - startTime > timeout:
                break

        if Xpoint is None or Ypoint is None:
            return False
        else:
            self.utils.click(Xpoint, Ypoint)
            return True
    def swipe_find(self, **msg):
        """
        下滑屏幕,找到元素就点击
        """
        try:
            msg['resourceId'] != ''
            msg['text'] != ''
            msg['content_desc'] != ''
            msg['textContains'] != ''
        except:
            pass
        start_time = time.time()
        while not self.click(**msg):
            self.utils.swipeToUp()
            if time.time() - start_time > 60:
                print('未找到%s' % (msg))
                return False
        return True
    def d_right_corner(self, attrib=None, name=None, **msg):
        """
        同属性单个元素，返回单个 右下角 坐标元组，(x, y)
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        用法：d(resourceId='com.android.calculator2:id/op_mul')
             d(text='8')
             d(content_desc='乘')
        """
        textContains = False
        if attrib and name:
            attrib = attrib.replace('resourceId', 'resource-id').replace('description', 'content-desc')
        else:
            for attrib in msg:
                if msg.get('resourceId'):
                    attrib = 'resource-id'
                    name = msg['resourceId']
                    break
                if msg.get('text'):
                    attrib = 'text'
                    name = msg['text']
                    break
                if msg.get('content_desc'):
                    attrib = 'content-desc'
                    name = msg['content_desc']
                    break
                if msg.get('textContains'):
                    attrib = 'text'
                    name = msg['textContains']
                    textContains = True
                    break
        Xpoint = None
        Ypoint = None

        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if textContains:
                if name in elem.attrib[attrib]:
                    # 获取元素所占区域坐标[x, y][x, y]
                    bounds = elem.attrib["bounds"]

                    # 通过正则获取坐标列表
                    coord = self.pattern.findall(bounds)

                    # 求取元素区域中心点坐标
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    break
            else:
                if elem.attrib[attrib] == name:
                    # 获取元素所占区域坐标[x, y][x, y]
                    bounds = elem.attrib["bounds"]

                    # 通过正则获取坐标列表
                    coord = self.pattern.findall(bounds)

                    # 求取元素区域中心点坐标
                    Xpoint = (int(coord[2]) - int(coord[0])) / 0.99 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 0.99 + int(coord[1])
                    break

        if Xpoint is None or Ypoint is None:
            return False
        else:
            return (Xpoint, Ypoint)

    def info(self, attrib=None, name=None, **msg):
        """
        同属性单个元素，返回单个控件所有属性
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        用法：d(resourceId='com.android.calculator2:id/op_mul')
             d(text='8')
             d(content_desc='乘')
        返回参数：{'index': '14', 'text': '×', 'resource-id': 'com.android.calculator2:id/op_mul', 'class': 'android.widget.Button', 'package': 'com.android.calculator2', 'content-desc': '乘', 'checkable': 'false', 'checked': 'false', 'clickable': 'true', 'enabled': 'true', 'focusable': 'true', 'focused': 'false', 'scrollable': 'false', 'long-clickable': 'false', 'password': 'false', 'selected': 'false', 'bounds': '[370,556][426,622]'}
        """
        textContains = False
        timeout = 1
        if attrib and name:
            attrib = attrib.replace('resourceId', 'resource-id').replace('description', 'content-desc')
        else:
            for attrib in msg:
                if msg.get('timeout'):
                    timeout = msg['timeout']
                if msg.get('resourceId'):
                    attrib = 'resource-id'
                    name = msg['resourceId']
                    break
                if msg.get('text'):
                    attrib = 'text'
                    name = msg['text']
                    break
                if msg.get('content_desc'):
                    attrib = 'content-desc'
                    name = msg['content_desc']
                    break
                if msg.get('className'):
                    attrib = 'class'
                    name = msg['className']
                    break
                if msg.get('textContains'):
                    attrib = 'text'
                    name = msg['textContains']
                    textContains = True
                    break
        Xpoint = None
        Ypoint = None
        startTime = time.time()
        while timeout:
            self.__uidump()
            tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if textContains:
                    if name in elem.attrib[attrib]:
                        element_info = elem.attrib
                        timeout = 0
                        break
                else:
                    if elem.attrib[attrib] == name:
                        element_info = elem.attrib
                        timeout = 0
                        break
            if time.time() - startTime > timeout:
                break
        return element_info
    # def infomation(self, msg):
    #     """
    #     同属性单个元素，返回单个控件所有属性
    #     :args:
    #     - attrib - node节点中某个属性
    #     - name - node节点中某个属性对应的值
    #     用法：d(('resourceId,'com.android.calculator2:id/op_mul'))
    #     返回参数：{'index': '14', 'text': '×', 'resource-id': 'com.android.calculator2:id/op_mul', 'class': 'android.widget.Button', 'package': 'com.android.calculator2', 'content-desc': '乘', 'checkable': 'false', 'checked': 'false', 'clickable': 'true', 'enabled': 'true', 'focusable': 'true', 'focused': 'false', 'scrollable': 'false', 'long-clickable': 'false', 'password': 'false', 'selected': 'false', 'bounds': '[370,556][426,622]'}
    #     """
    #     attrib = msg[0].replace('resourceId','resource-id').replace('description','content-desc')
    #     name = msg[1]
    #     element_info = None
    #     self.__uidump()
    #     tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
    #     treeIter = tree.iter(tag="node")
    #     for elem in treeIter:
    #         if elem.attrib[attrib] == name:
    #             element_info = elem.attrib
    #             break
    #     return element_info
    def exists(self,attrib=None,name=None, **msg):
        """
        同属性单个元素，返回boolean
        :args:
        - attrib - node节点中某个属性
        - name - node节点中某个属性对应的值
        用法：d(('resourceId,'com.android.calculator2:id/op_mul'))
        返回参数：{'index': '14', 'text': '×', 'resource-id': 'com.android.calculator2:id/op_mul', 'class': 'android.widget.Button', 'package': 'com.android.calculator2', 'content-desc': '乘', 'checkable': 'false', 'checked': 'false', 'clickable': 'true', 'enabled': 'true', 'focusable': 'true', 'focused': 'false', 'scrollable': 'false', 'long-clickable': 'false', 'password': 'false', 'selected': 'false', 'bounds': '[370,556][426,622]'}
        """
        textContains = False
        if attrib and name:
            attrib = attrib.replace('resourceId', 'resource-id').replace('description', 'content-desc')
        else:
            for attrib in msg:
                if msg.get('resourceId'):
                    attrib = 'resource-id'
                    name = msg['resourceId']
                    break
                if msg.get('text'):
                    attrib = 'text'
                    name = msg['text']
                    break
                if msg.get('content_desc'):
                    attrib = 'content-desc'
                    name = msg['content_desc']
                    break
                if msg.get('textContains'):
                    attrib = 'text'
                    name = msg['textContains']
                    textContains = True
                    break
        element_info = None
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if textContains:
                if name in elem.attrib[attrib]:
                    element_info = elem.attrib
                    break
            else:
                if elem.attrib[attrib] == name:
                    element_info = elem.attrib
                    break
        return True if element_info else False

    # 正计时
    def time_jishi(self, **kwargs):
        '''
        :param lineTmpla: 
        :param mins: 多少秒后停止
        :usage:  time_jishi(str="等待", text='交易成功', click=True)
        '''
        lineTmpla = kwargs['str'] + " %s "
        return self.__time_jishi(lineTmpla, kwargs['text'] if kwargs.get('text') else '',
                                 kwargs['resourceId'] if kwargs.get('resourceId') else '',
                                 kwargs['content_desc'] if kwargs.get('content_desc') else '',
                                 kwargs['textContains'] if kwargs.get('textContains') else '',
                                 kwargs['icon_name'] if kwargs.get('icon_name') else '',
                                 kwargs['confidence'] if kwargs.get('confidence') else '',
                                 kwargs['timeout'] if kwargs.get('timeout') else 3600,
                                 kwargs['click'] if kwargs.get('click') else '')
    def __time_jishi(self, lineTmpla, text, resourceId, content_desc, textContains, icon_name, confidence, timeout, click):
        count = 0
        start_time = time.time()
        if text:
            if click:
                while not self.click(text=text):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
            else:
                while not self.exists(text=text):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
        elif resourceId:
            if click:
                while not self.click(resourceId=resourceId):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
            else:
                while not self.exists(resourceId=resourceId):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
        elif content_desc:
            if click:
                while not self.click(content_desc=content_desc):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
            else:
                while not self.exists(content_desc=content_desc):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
        elif textContains:
            if click:
                while not self.click(textContains=textContains):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
            else:
                while not self.exists(textContains=textContains):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
        elif icon_name:
            if click:
                while not self.utils.find_icon_click(icon_name, confidence):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
            else:
                while not self.utils.find_icon(icon_name, confidence):
                    count += 1
                    sys.stdout.write("\r" + lineTmpla % (count))
                    sys.stdout.flush()
                    if time.time() - start_time > timeout:
                        print_color('超时%s秒，自动退出' % (timeout), 4)
                        break
        else:
            print_color('缺少kwargs值', 4)
    def __elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表，[(x1, y1), (x2, y2)]
        """
        pointList = []
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                # 将匹配的元素区域的中心点添加进pointList中
                pointList.append((Xpoint, Ypoint))

        return pointList

    def __bound(self, attrib, name):
        """
        同属性单个元素，返回单个坐标区域元组,(x1, y1, x2, y2)
        """
        coord = []

        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)

        if not coord:
            raise Exception("Not found this element(%s) in current activity" % name)

        return (int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))

    def __bounds(self, attrib, name):
        """
        同属性多个元素，返回坐标区域列表，[(x1, y1, x2, y2), (x3, y3, x4, y4)]
        """

        pointList = []
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                pointList.append((int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])))

        return pointList

    def __checked(self, attrib, name):
        """
        返回布尔值列表
        """
        boolList = []
        self.__uidump()
        tree = ET.ElementTree(file=PATH("%s/uidump.xml" % self.tempFile))
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                checked = elem.attrib["checked"]
                if checked == "true":
                    boolList.append(True)
                else:
                    boolList.append(False)

        return boolList

    def findElementByName(self, name):
        """
        通过元素名称定位单个元素
        usage: findElementByName(u"设置")
        """
        return self.__element("text", name)

    def findElementsByName(self, name):
        """
        通过元素名称定位多个相同text的元素
        """
        return self.__elements("text", name)

    def findElementByClass(self, className):
        """
        通过元素类名定位单个元素
        usage: findElementByClass("android.widget.TextView")
        """
        return self.__element("class", className)

    def findElementsByClass(self, className):
        """
        通过元素类名定位多个相同class的元素
        """
        return self.__elements("class", className)

    def findElementById(self, id):
        """
        通过元素的resource-id定位单个元素
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        return self.__element("resource-id", id)

    def findElementsById(self, id):
        """
        通过元素的resource-id定位多个相同id的元素
        """
        return self.__elements("resource-id", id)

    def findElementByContentDesc(self, contentDesc):
        """
        通过元素的content-desc定位单个元素
        """
        return self.__element("content-desc", contentDesc)

    def findElementsByContentDesc(self, contentDesc):
        """
        通过元素的content-desc定位多个相同的元素
        """
        return self.__elements("content-desc", contentDesc)

    def getElementBoundByName(self, name):
        """
        通过元素名称获取单个元素的区域
        """
        return self.__bound("text", name)

    def getElementBoundsByName(self, name):
        """
        通过元素名称获取多个相同text元素的区域
        """
        return self.__bounds("text", name)

    def getElementBoundByClass(self, className):
        """
        通过元素类名获取单个元素的区域
        """
        return self.__bound("class", className)

    def getElementBoundsByClass(self, className):
        """
        通过元素类名获取多个相同class元素的区域
        """
        return self.__bounds("class", className)

    def getElementBoundByContentDesc(self, contentDesc):
        """
        通过元素content-desc获取单个元素的区域
        """
        return self.__bound("content-desc", contentDesc)

    def getElementBoundsByContentDesc(self, contentDesc):
        """
        通过元素content-desc获取多个相同元素的区域
        """
        return self.__bounds("content-desc", contentDesc)

    def getElementBoundById(self, id):
        """
        通过元素id获取单个元素的区域
        """
        return self.__bound("resource-id", id)

    def getElementBoundsById(self, id):
        """
        通过元素id获取多个相同resource-id元素的区域
        """
        return self.__bounds("resource-id", id)

    def isElementsCheckedByName(self, name):
        """
        通过元素名称判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("text", name)

    def isElementsCheckedById(self, id):
        """
        通过元素id判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("resource-id", id)

    def isElementsCheckedByClass(self, className):
        """
        通过元素类名判断checked的布尔值，返回布尔值列表
        """
        return self.__checked("class", className)
class Keycode():
    HOME键 = 3
    返回键 = 4
    打开拨号应用 = 5
    挂断电话 = 6
    增加音量 = 24
    降低音量 = 25
    电源键 = 26
    拍照需要在相机应用里 = 27
    换行 = 61
    KEYCODE_TAB = 61
    打开浏览器 = 64
    回车 = 66
    # 回车 = KEYCODE_ENTER
    退格键 = 67
    KEYCODE_DEL = 67
    菜单键 = 82
    通知键 = 83
    播放暂停 = 85
    停止播放 = 86
    播放下一首 = 87
    播放上一首 = 88
    移动光标到行首或列表顶部 = 122
    移动光标到行末或列表底部 = 123
    恢复播放 = 126
    暂停播放 = 127
    扬声器静音键 = 164
    打开系统设置 = 176
    切换应用 = 187
    打开联系人 = 207
    打开日历 = 208
    打开音乐 = 209
    打开计算器 = 210
    降低屏幕亮度 = 220
    提高屏幕亮度 = 221
    系统休眠 = 223
    点亮屏幕 = 224
    打开语音助手 = 231
    如果没有wakelock则让系统休眠 = 276

    POWER = 26
    BACK = 4
    HOME = 3
    MENU = 82
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    SPACE = 62
    BACKSPACE = 67
    ENTER = 66
    MOVE_HOME = 122
    MOVE_END = 123

class Device(object):
    """
    单个设备，可不传入参数device_id
    """
    def __init__(self, device_id=""):
        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s %s" % device_id

    # 当前时间
    def get_time(self):
        return time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

    def get_time_day(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    # 时间戳 + str
    def print_before(self, str):
        print('%s %s' % (self.get_time(), str))

    # 时间戳 + str1 + str2
    def print_str(self, str1, str2):
        print('%s %s%s' % (self.get_time(), str1, str2))

    # adb命令
    def adb(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # adb 命令,返回运行结果
    def adb_return(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return subprocess.check_output(cmd).decode('utf8')
    # os.system('adb 命令)
    def adb_os_system(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return os.system(cmd)
    def adb_os_popen(self, args):
        '''
        重写os.popen()方法,自带多线程效果
        :param cmd: 
        :return: 
        usage： push_result = d.adb_os_popen('push %s /data/local/tmp/tmp_apk.apk' % (apk))
                此处可以运行其它命令
                push_result.close()
        '''
        import io
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        proc = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                bufsize=-1)
        return _wrap_close(io.TextIOWrapper(proc.stdout), proc)
    # adb shell命令
    def shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # adb shell命令,返回运行结果
    def shell_return(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args))
        return subprocess.check_output(cmd).decode('utf8')
    # adb shell命令,返回运行结果.比如adb shell ls sdcard/dd.txt的返回，上面获取不了
    def shell_return_os_popen(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args))
        return list(os.popen(cmd).readlines())[0].replace('\n','')
    # 运行fastboot命令
    def fastboot(self,args):
        cmd = "%s %s %s" % (fastboot, self.device_id, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 获取udid ，判断设备是否连接
    def getUdid(self):
        try:
            '''''获取设备列表信息，并用"\r\n"拆分'''
            deviceInfo = self.adb_return('devices').split("\r\n")
            adb_first_start = False
            for i in deviceInfo:
                if 'successfully' in i:
                    adb_first_start = True
                    break
            if adb_first_start:
                udid = 'device'.join(deviceInfo[3].split('device')[:1])
                '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
                if deviceInfo[3] == '':
                    return ''
                else:
                    return udid.strip()
            else:
                udid = 'device'.join(deviceInfo[1].split('device')[:1])
                '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
                if deviceInfo[1] == '':
                    return ''
                else:
                    return udid.strip()
        except MyError as e:
            print("Device Connect Fail:", e.value)

    def getDeviceState(self):
        """
        获取设备状态： offline | bootloader | device
        """
        return self.adb("get-state").stdout.read().strip().decode('utf8')

    def get_serialno(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip().decode('utf8')

    def get_value(self,value, str):
        '''
        按照指定格式拿出值
        usage:  packages = "package:com.github.uiautomator package:com.netease.atx.assistant"
                version0 = "name=tool.terminal.apphelperservice versionCode=1000002 versionName=1.0.2"
                get_value('name',version0)
                结果：tool.terminal.apphelperservice
        :param str: 
        :return: 
        '''
        if '=\'' in str:
            name = '%s=\'' % (value).join(str.split('%s=\'' % (value))[1:])
            name = '\''.join(name.split('\'')[:1])
        else:
            name = '%s=' % (value).join(str.split('%s=' % (value))[1:])
            name = ' '.join(name.split(' ')[:1])
            if name[-1:] == '=':
                name = name[:-1]
        return name
    # 获取设备信息，大方法
    def get_device_info(self):
        device_info = self.shell("getprop").stdout.read().strip().decode('utf8').replace('\r\r\n',',').replace('[','').replace(']','').replace(':','=').replace(' ','')
        device_info = device_info.replace(',',' ')

        '''
        usage:如下所示
        
        getAndroidVersion = self.get_value('ro.build.version.release',device_info)
        get_brand = self.get_value('ro.boot.hardware',device_info)
        getSdkVersion = self.get_value('ro.build.version.sdk',device_info)
        getDeviceModel = self.get_value('ro.product.model',device_info)
        get_heapgrowthlimit = self.get_value('dalvik.vm.heapgrowthlimit',device_info)
        get_heapstartsize = self.get_value('dalvik.vm.heapstartsize',device_info)
        get_heapsize = self.get_value('dalvik.vm.heapsize',device_info)
        '''
        return device_info
    def getAndroidVersion(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        return self.shell("getprop ro.build.version.release").stdout.read().strip().decode('utf8')

    def get_brand(self):
        """
        获取Android平台型号品牌
        """
        return self.shell("getprop ro.boot.hardware").stdout.read().strip().decode('utf8')

    def getSdkVersion(self):
        """
        获取设备SDK版本号,如19
        """
        return self.shell("getprop ro.build.version.sdk").stdout.read().strip().decode('utf8')

    def getDeviceModel(self):
        """
        获取设备型号
        """
        return self.shell("getprop ro.product.model").stdout.read().strip().decode('utf8')
    def getOsVersion(self):
        """
        获取os版本
        """
        return self.shell("getprop ro.build.id").stdout.read().strip().decode('utf8')

    def getPid(self, packageName):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        if system is "Windows":
            pidinfo = self.shell("ps | findstr %s$" % packageName).stdout.read().decode('utf8')
        else:
            pidinfo = self.shell("ps | grep -w %s" % packageName).stdout.read().decode('utf8')

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return pattern.findall(" ".join(result))[0]

    def killProcess(self, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if self.shell_return("kill %s" % str(pid)).split(": ")[-1] == "":
            return "kill success"
        else:
            return self.shell_return("kill %s" % str(pid))  # .split(": ")[-1]

    def force_stop(self, packageName):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        self.shell("am force-stop %s" % packageName)

    def getFocusedPackageAndActivity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        # pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        # out = self.shell("dumpsys window w | %s \/ | %s name=" % (find_util, find_util)).stdout.read()
        # 
        # return pattern.findall(out.decode('utf8'))[0]

        packageName = subprocess.check_output(
            'adb -s %s shell dumpsys activity top | grep ACTIVITY' % (getUdid())).decode()
        packageName_list = packageName.split('ACTIVITY')
        packageName = packageName_list[-1]
        
        packageName = packageName.strip()
        packageName = ' '.join(packageName.split(' ')[:1])
        return packageName

    def getCurrentPackageName(self):
        """
        获取当前运行的应用的包名
        """
        # return self.getFocusedPackageAndActivity().split("/")[0]

        
        packageName = '/'.join(self.getFocusedPackageAndActivity().split('/')[:1])
        return packageName

    def getCurrentActivity(self):
        """
        获取当前运行应用的activity
        """
        # return self.getFocusedPackageAndActivity().split("/")[-1]

        packageName = self.getFocusedPackageAndActivity().split('/')[1]
        return packageName
    def getMemTotal(self):
        """
        获取最大内存
        """
        MemTotal = self.shell("cat proc/meminfo | %s MemTotal" % find_util).stdout.read().decode('utf8').split(":")[-1]

        return MemTotal.replace('\r\r\n','').strip()
    def getMemFree(self):
        """
        获取剩余内存
        """
        MemFree = self.shell("cat proc/meminfo | %s MemFree" % find_util).stdout.read().decode('utf8').split(":")[-1]

        return MemFree.replace('\r\r\n','').strip()
    def getCpuHardware(self):
        """
        获取cpu型号
        """
        Hardware = self.shell("cat proc/cpuinfo | %s Hardware" % find_util).stdout.read().decode('utf8').split(":")[-1]

        return Hardware.replace('\r\r\n','').strip()
    def getBatteryLevel(self):
        """
        获取电池电量
        """
        level = self.shell("dumpsys battery | %s level" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return int(level)
    def getBatteryVoltage(self):
        """
        获取电池电压,单位mV毫伏
        """
        voltage = self.shell("dumpsys battery | %s voltage" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return int(voltage)

    def getBatteryHealth(self):
        """
        电池健康状态：只有数字2表示good
        """
        health = self.shell("dumpsys battery | %s health" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return int(health)
    def getBatteryACpowered(self):
        """
        电池是否在AC充电器充电
        """
        ACpowered = self.shell("dumpsys battery | %s AC" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return ACpowered.replace('\r\r\n','')
    def getBatteryPresent(self):
        """
        电池是否安装在机身
        """
        present = self.shell("dumpsys battery | %s present" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return present.replace('\r\r\n','')

    def getBatteryStatus(self):
        """
        获取电池充电状态 ：2：充电状态 ，其他数字为非充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        """
        statusDict = {1: "BATTERY_STATUS_UNKNOWN:未知状态",
                      2: "BATTERY_STATUS_CHARGING:充电状态",
                      3: "BATTERY_STATUS_DISCHARGING:放电状态",
                      4: "BATTERY_STATUS_NOT_CHARGING:未充电",
                      5: "BATTERY_STATUS_FULL:充电已满"}
        status = self.shell("dumpsys battery | %s status" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return statusDict[int(status)]

    def getBatteryTemp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" % find_util).stdout.read().decode('utf8').split(": ")[-1]

        return int(temp) / 10.0

    def get_heapgrowthlimit(self):
        """
        单个应用程序最大内存限制，超过这个值会产生OOM(内存溢出）
        测程序一般看这个
        """
        heapgrowthlimit = self.shell("getprop dalvik.vm.heapgrowthlimit").stdout.read().decode('utf8').split("\r\r\n")[0]
        return heapgrowthlimit
    def get_heapstartsize(self):
        """
        应用启动后分配的初始内存
        """
        heapstartsize = self.shell("getprop dalvik.vm.heapstartsize").stdout.read().decode('utf8').split("\r\r\n")[0]
        return heapstartsize
    def get_heapsize(self):
        """
        单个java虚拟机最大的内存限制，超过这个值会产生OOM(内存溢出）
        """
        heapsize = self.shell("getprop dalvik.vm.heapsize").stdout.read().decode('utf8').split("\r\r\n")[0]
        return heapsize

    def getScreenResolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        pattern = re.compile(r"\d+")
        out = self.shell("dumpsys display | %s PhysicalDisplayInfo" % find_util).stdout.read()
        # print(type(out))
        display = ""
        if out:
            display = pattern.findall(out.decode('utf-8'))
        elif int(self.getSdkVersion()) >= 18:
            display = self.shell("wm size").stdout.read().decode('utf8').split(":")[-1].strip().split("x")
        else:
            raise Exception("get screen resolution failed!")
        return (int(display[0]), int(display[1]))

    def screenshot(self, fileName=None):
        """
        截图，保存到脚本"tmp\screenshot"目录里
        usage: adb.screenchot('screenshot.png')
        win 7不自动创建文件夹，所有要先判断然后创建
        """
        if not os.path.exists('tmp//screenshot'):
            os.makedirs('tmp//screenshot', exist_ok=True)
        self.shell("/system/bin/screencap -p /sdcard/screenshot.png").stdout.read().decode('utf8')
        self.adb("pull /sdcard/screenshot.png tmp/screenshot/%s" % (fileName if fileName != '' else 'screenshot.png')).stdout.read().decode('utf8')

    def reboot(self):
        """
        重启设备
        """
        self.adb("reboot")

    def getSystemAppList(self):
        """
        获取设备中安装的系统应用包名列表
        """
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.decode('utf8').split(":")[-1].splitlines()[0])

        return sysApp

    def getThirdAppList(self):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.decode('utf8').split(":")[-1].splitlines()[0])

        return thirdApp

    def getInstalledAppList(self):
        """
        获取设备中所有安装的应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages").stdout.readlines():
            thirdApp.append(packages.decode('utf8').split(":")[-1].splitlines()[0])

        return thirdApp

    def getMatchingAppList(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.shell("pm list packages %s" % keyword).stdout.readlines():
            matApp.append(packages.decode('utf8').split(":")[-1].splitlines()[0])

        return matApp

    def getAppStartTotalTime(self, component):
        """
        获取启动应用所花时间
        usage: getAppStartTotalTime("com.android.settings/.Settings")
        """
        time = self.shell("am start -W %s | %s TotalTime" % (component, find_util)) \
            .stdout.read().decode('utf8').split(": ")[-1]
        return int(time)

    def installApp(self, appFile):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("d:\\apps\\Weico.apk")
        """
        self.adb("install %s" % appFile)

    def isInstall(self, packageName):
        """
        根据包名判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        matApp = []
        for packages in self.shell("pm list packages %s" % packageName).stdout.readlines():
            package = packages.decode('utf8').split(":")[-1].splitlines()[0]
            if package == packageName:
                matApp.append(package)
                break
        if matApp:
            return True
        else:
            return False

    def uninstallApp(self, packageName):
        """
        卸载应用
        args:
        - packageName -:应用包名，非apk名
        """
        return self.adb_return("uninstall %s" % packageName).split("\r\n")

    def clearAppData(self, packageName):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.shell_return("pm clear %s" % packageName):
            return True
        else:
            return False
            return "清除缓存数据失败，请确认应用是否存在"

    def clearCurrentApp(self):
        """
        清除当前应用缓存数据
        """
        packageName = self.getCurrentPackageName()
        component = self.getFocusedPackageAndActivity()
        self.clearAppData(packageName)
        self.startActivity(component)

    def startActivity(self, component):
        """
        启动一个Activity
        usage: startActivity("com.android.settinrs/.Settings")
        """
        self.shell_return("am start %s" % component)
    def start_app(self, packageName):
        """
        启动一个应用
        usage: start_app("com.android.settings")
        """
        self.shell_return("monkey -p %s -c android.intent.category.LAUNCHER 1" % packageName)

    def startWebpage(self, url):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        self.shell_return("am start -a android.intent.action.VIEW -d %s" % url)

    def callPhone(self, number):
        """
        启动拨号器拨打电话
        usage: callPhone(10086)
        """
        self.shell("am start -a android.intent.action.CALL -d tel:%s" % str(number))

    def sendKeyEvent(self, keycode):
        """
        发送一个按键事件
        args:
        - keycode -:
        http://developer.android.com/reference/android/view/KeyEvent.html
        usage: sendKeyEvent(keycode.HOME)
        """
        self.shell_return("input keyevent %s" % str(keycode))

    def longPressKey(self, keycode):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(keycode.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(keycode))

    def click_element(self, element):
        """
        点击元素
        usage: click_element(Element().findElementByName(u"计算器"))
        """
        self.shell("input tap %s %s" % (str(element[0]), str(element[1])))

    def click(self, x, y=None):
        """
        发送触摸点击事件
        usage: click(0.5, 0.5) 点击屏幕中心位置
        """
        if isinstance(x,(list,tuple)):
            x0 = x
            x = x0[0]
            y = x0[1]
        if x < 1:
            self.shell("input tap %s %s" % (
            str(x * self.getScreenResolution()[0]), str(y * self.getScreenResolution()[1])))
        else:
            self.shell("input tap %s %s" % (x, y))

    def swipe(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, duration=" "):
        """
        发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(0.9, 0.5, 0.1, 0.5) 左滑
        """
        if start_ratioWidth < 1:
            self.shell_return("input swipe %s %s %s %s %s" % (
            str(start_ratioWidth * self.getScreenResolution()[0]), str(start_ratioHigh * self.getScreenResolution()[1]), \
            str(end_ratioWidth * self.getScreenResolution()[0]), str(end_ratioHigh * self.getScreenResolution()[1]),
            str(duration)))
        elif start_ratioWidth >= 1:
            self.shell_return("input swipe %s %s %s %s %s" % (
            start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, str(duration)))

    def swipeToLeft(self):
        """
        左滑屏幕
        """
        self.swipe(0.8, 0.5, 0.2, 0.5)

    def swipeToRight(self):
        """
        右滑屏幕
        """
        self.swipe(0.2, 0.5, 0.8, 0.5)

    def swipeToUp(self):
        """
        上滑屏幕
        """
        self.swipe(0.5, 0.8, 0.5, 0.2)

    def swipeToDown(self):
        """
        下滑屏幕
        """
        self.swipe(0.5, 0.2, 0.5, 0.8)

    def click_long(self, x, y,duration=None):
        """
        长按屏幕的某个坐标位置, Android 4.4及以上
        usage: click_long(500, 600)
               click_long(0.5, 0.5)
        """
        self.swipe(x, y, x, y, duration=duration if duration else 2000)

    def longPressElement(self, e):
        """
       长按元素, Android 4.4
        """
        self.shell("input swipe %s %s %s %s %s" % (str(e[0]), str(e[1]), str(e[0]), str(e[1]), str(2000)))

    # 删除文本框内容，入参：删除次数
    def clear_text(self, number):
        if not number:
            self.sendKeyEvent(keycode=67)
        else:
            for i in range(number):
                self.sendKeyEvent(keycode=67)

    def setText(self, string):
        """
        发送一段文本，只能包含英文字符和空格
        usage: setText("i am unique")
        """
        self.shell_return('input text "%s"' % (string))

    # 获取内存,并写入到txt中记录
    def get_meminfo_heap(self, packageName):
        if not os.path.exists("tmp//meminfo"):
            os.makedirs("tmp//meminfo", exist_ok=True)
        if packageName != '':
            Native_Heap = self.shell_return('dumpsys meminfo %s | grep Native' % (packageName)).split('\r\n')[0].strip()
            write_txt_file(name='tmp/meminfo/%s的Native层内存使用情况%s.txt' % (packageName, self.get_time()[:10]), content=Native_Heap)
            Dalvik_Heap = self.shell_return('dumpsys meminfo %s | grep Dalvik' % (packageName)).split('\r\n')[0].strip()
            write_txt_file(name='tmp/meminfo/%s的Java    堆内存使用情况%s.txt' % (packageName, self.get_time()[:10]), content=Dalvik_Heap)
        else:
            RAM_Used = self.shell_return('dumpsys meminfo | grep Used').split('\r\n')[0].strip()
            write_txt_file(name='tmp/meminfo/全部内存情况%s.txt' % (self.get_time()[:10]), content=RAM_Used)
            # top6 = self.shell_return('top -m 6 -n 1').split('\r\n')[0].strip()
            # g = open('tmp/meminfo/全部top前6内存情况%s.txt' % (self.get_time()[:10]), 'a')
            # g.write('%s\n' % (top6))
            # g.close()

    # 取日志,入参：str1，str2
    def logcat_pull(self, **msg):
        if not os.path.exists("tmp//logcat"):
            os.makedirs("tmp//logcat", exist_ok=True)
        try:
            self.shell('rm -r /data/local/tmp/logcat.txt')
            self.shell('logcat -v threadtime -d -f /data/local/tmp/logcat.txt')
            self.adb('pull /data/local/tmp/logcat.txt tmp//logcat//logcat%s-%s-%s.txt' % (
            self.get_time()[11:], msg['str1'], msg['str2']))
        except:
            self.print_before('取logcat失败')
            pass

    # 可疑情况截图并打开，入参：str1，str2自定义错误信息，截图后缀名
    def screenshot_err(self, **msg):
        try:
            icon_name = ('screenshot%s-%s-%s.jpg' % (self.get_time()[11:], msg['str1'], msg['str2']))
            self.screenshot(icon_name)
            os.system('start tmp/screenshot/%s' % (icon_name))
        except:
            self.print_before('screenshot_err失败')
            pass

    # 可疑情况截图不打开，入参：str1，str2自定义错误信息，截图后缀名
    def screenshot_err_no_open(self, **msg):
        try:
            icon_name = ('screenshot%s-%s-%s.jpg' % (self.get_time()[11:], msg['str1'], msg['str2']))
            self.screenshot(icon_name)
        except:
            self.print_before('screenshot_err_no_open失败')
            pass
    def push(self, local, remote, override=True):
        '''
        push电脑本地文件到手机
        :param pc_file: 
        :param remote: 
        :return: 
        '''
        if self.is_remote_file_exist(remote) and not override:
            pass
        else:
            self.adb_return('push %s %s' % (local, remote))
    def is_remote_file_exist(self, remote):
        '''
        判断手机内部文件是否存在,查看手机内部文件是否存在
        :param remote: 
        :return: 存在 Ture;不存在 False
        '''
        ls_remote = self.shell_return_os_popen(remote)
        if 'No such file or directory' in ls_remote or 'not found' in ls_remote:
            return False
        else:
            return True
    def pull(self, remote, local=''):
        '''
        pull手机里的文件到电脑本地
        :param remote: 
        :param local: 
        :return: 
        '''
        if not self.is_remote_file_exist(remote):
            print('手机文件不存在')
        self.adb_return('pull %s %s' % (remote, local))
    def pull_apkByPackagename(self, packagename, local=''):
        '''
        根据apk包名 取出手机里apk文件，需要root权限
        :param packagename: 
        :param local: 
        :return: 
        '''
        self.adb('root')
        self.adb_return('root')
        self.adb('remount')
        self.adb_return('remount')
        apk_version = self.getVersionName(packagename)
        resourcePath = apk_version[-2]  # '/data/app/com.lzz.test-1'
        resourceName = '/'+resourcePath.split('/')[-1]+'.apk'
        resourcePath_resourceName = resourcePath+resourceName
        is_split = apk_version[-1]
        if is_split:
            print('apk文件被拆分')
        else:
            print('取出完整文件')
        if self.is_remote_file_exist(resourcePath+'/base.apk'):
            self.pull(resourcePath+'/base.apk', local)
        elif self.is_remote_file_exist(resourcePath_resourceName):
            self.pull(resourcePath_resourceName, local)
        else:
            print('手机文件不存在')
    # 点亮解锁屏幕
    def screen_on(self):
        self.sendKeyEvent(keycode=224)
        # if Element().info(resourceId='com.android.systemui:id/lock_icon'):
        #     self.sendKeyEvent(keycode=224)
        #     self.swipeToUp()
    # 熄灭屏幕
    def screen_off(self):
        self.sendKeyEvent(keycode=223)
    # 判断屏幕是否点亮
    def is_screen_on(self):
        output = self.shell_return("dumpsys power")
        return 'mHoldingDisplaySuspendBlocker=true' in output

    # 判断WiFi是否打开
    def is_wifi_on(self):
        wifi_on = self.shell_return('settings get global wifi_on').replace('\r','').replace('\n','')
        if wifi_on == '1':
            return True
        else:
            return False

    def getH5PackageName(self):
        '''
        示例，暂时不用 。
        :return: 
        '''
        h5packageName = ''
        try:
            h5packageName = self.shell_return(
                'dumpsys activity activities | grep index')
            h5packageName = '/index'.join(h5packageName.split('/index')[:1])
            h5packageName = 'ULightApp/'.join(h5packageName.split('ULightApp/')[1:])
        except:
            pass
        if h5packageName == '':
            return ''
        else:
            return h5packageName

    # 获取ip地址
    def ipAddress(self):
        ipAddress0 = self.shell_return('ifconfig wlan0')
        ipAddress0 = 'ask'.join(ipAddress0.split('ask')[:1])
        if ipAddress0.count('ip'):
            ipAddress0 = 'ip'.join(ipAddress0.split('ip')[1:])
        elif ipAddress0.count('addr:'):
            ipAddress0 = 'addr:'.join(ipAddress0.split('addr:')[1:]).split(' ')[0]
        ip = ipAddress0.strip()
        try:
            ip = re.search('([\d]{1,3}\.){3}[\d]{1,3}', ip).group()
            if ip != '':
                return ip
        except:
            return ''
    # 获取物理网卡mac地址
    def get_mac(self):
        try:
            mac = self.shell_return('cat /sys/class/net/wlan0/address')
            mac = str(mac).replace('\r','').replace('\n','')
            if len(mac) < 21:
                return mac
        except:
            return ''
    # 获取设备里已装程序版本信息
    def getVersionName(self, packageName):
        '''
        :param packageName: 包名
        :return: 0内部版本号、1版本名、2首次安装时间、3上次安装时间、4data/app/路径、5是否拆分
        '''
        if packageName != '':
            if not self.isInstall(packageName):
                return []
            versionName = self.shell_return(
                'dumpsys package %s | grep versionName' % (packageName)).replace(
                '\n', '').replace('\r', '').strip()
            versionCode = self.shell_return(
                'dumpsys package %s | grep versionCode' % (packageName)).replace(
                '\n', '').replace('\r', '')
            versionTime = self.shell_return(
                'dumpsys package %s | grep lastUpdateTime' % (packageName)).replace(
                '\n', '').replace('\r', '').strip()
            versionFirstTime = self.shell_return('dumpsys package %s | grep firstInstallTime' % (
            packageName)).replace('\n', '').replace('\r', '').strip()
            resourcePath = self.shell_return('dumpsys package %s | grep resourcePath' % (
            packageName)).replace('\n', '').replace('\r', '').strip()
            splits = self.shell_return('dumpsys package %s | grep splits' % (
            packageName)).replace('\n', '').replace('\r', '').strip()
            if versionCode != '':
                versionCode = versionCode.split(' ')
                i = 0
                versionCode_len = len(versionCode)
                while i < versionCode_len:
                    if versionCode[0] == '' or versionCode[0] == ' ':
                        versionCode.remove(versionCode[0])
                    else:
                        break
                    i += 1
                versionCode = versionCode[0]
            if versionTime != '':
                versionTime = versionTime.split('lastUpdateTime=')[1]
            if versionFirstTime != '':
                versionFirstTime = versionFirstTime.split('firstInstallTime=')[1]
            if splits == 'splits=[base]':
                splits = False
            else:
                splits = True
            resourcePath = resourcePath.replace('resourcePath=','')
            return [versionName, versionCode, versionFirstTime, versionTime, resourcePath, splits]
        else:
            return []
    # 获取sn号
    def get_sn(self):
        serialno = self.shell_return('getprop persist.sys.product.serialno').replace(
            '\r', '').replace('\n', '')
        return serialno

    # 获取tusn号
    def get_tusn(self):
        tusn = self.shell_return('getprop persist.sys.product.tusn').replace(
            '\r', '').replace('\n', '')
        return tusn

    # python获取当前位置所在的行号和函数名
    def get_head_info(self):
        '''
        :return: D:/Python_script_selenium/adbUtil_test.py, texst, 10, 
        '''
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        return ' %s, %s, %s' % (f.f_code.co_filename, f.f_code.co_name, str(f.f_lineno))

    # 根据图片名判断当前页面
    def find_icon(self, icon_name, confidence=None):
        '''
        usage:  find_icon('icon/print_cancel.720x1280.jpg', '')
                find_icon('icon/print_cancel.720x1280.jpg', 0.9)
        :param icon_name: 本地图片路径，待查找的图
        :param confidence: 相似度
        :return: 位置坐标
        '''
        from uitest import aircv as ac
        self.screenshot('screenshot.png')
        imsrc = ac.imread('tmp/screenshot/screenshot.png')  # 原始图像
        imsch = ac.imread(icon_name)  # 待查找的部分
        result = ac.find_template(imsrc, imsch)
        print(result)
        if not confidence:
            confidence = 0.95
        if result == None:
            return False
        elif result['confidence'] < confidence:
            return False
        else:
            location = result['result']
            return location

    # 点击找到的图片
    def find_icon_click(self, icon_name, confidence=None):
        '''
        usage:  find_icon_click('icon/print_cancel.720x1280.jpg', '')
                find_icon_click('icon/print_cancel.720x1280.jpg', 0.9)
        :param icon_name: 本地图片路径，待查找的图
        :param confidence: 相似度
        :return: True 或者 False
        '''
        location = self.find_icon(icon_name, confidence)
        if location:
            self.click(location[0], location[1])
            # print('点击位置：', location[0], location[1])
            return location
        else:
            print('未找到%s' % (icon_name))
            return False
    # 返回
    def back(self):
        self.sendKeyEvent(Keycode.BACK)
    # HOME键
    def home(self):
        self.sendKeyEvent(Keycode.HOME)
    def get_allnet(self, packageName):
        '''
        获取指定包名的应用的wifi流量消耗, 目前只针对部分机型
        :param packageName: 
        :return: 使用流量：单位m：get_allnet('com.lzz.test')[4]
        :usage: allnet = get_allnet('com.lzz.test')
        # print('网络数据：', allnet[2]+allnet[3], 'kb','≈', allnet[4],'m')
        '''
        print('1、pid方式查看wifi流量：')
        # 获取程序pid
        package_pid = re.split('[ ]+', self.shell_return('ps | grep %s' % (packageName)).split("\r\r\n")[-2])[1].strip()
        print('package_pid:',package_pid)
        # 通过pid查看wifi流量
        package_wlan = re.split('[ ]+', self.shell_return('cat /proc/%s/net/dev | grep wlan0' % (package_pid)).split("\r\r\n")[0])
        package_wlan1 = int(package_wlan[2])/1024
        package_wlan2 = int(package_wlan[10])/1024
        print(round(package_wlan1), '+', round(package_wlan2), '=', round(package_wlan1+package_wlan2), 'kb ≈ ', round((package_wlan1+package_wlan2)/1024), 'm')
        package_Thread = self.shell_return('cat /proc/%s/status | grep Thread' % (package_pid)).split("\t")[1].strip()
        print('线程数:',package_Thread)

        print('2、uid方式：')
        # 获取程序uid
        package_uid = self.shell_return('cat /proc/%s/status | grep Uid' % (package_pid)).split("\t")[1].strip()
        print('package_uid:',package_uid)
        # 通过uid查看wifi流量
        package_allnet = self.shell_return('cat /proc/net/xt_qtaguid/stats | grep %s' % (package_uid)).split("\r\r\n")
        package_list = []
        for i in package_allnet:
            if i == '':
                break
            else:
                package_list.append(i.split(' '))
        package_rx_bytes = 0
        package_tx_bytes = 0
        for i in package_list:
            package_rx_bytes += int(i[5])
            package_tx_bytes += int(i[7])
        print('接收数据package_rx_bytes:', package_rx_bytes, '传输数据package_tx_bytes:', package_tx_bytes)
        return [package_rx_bytes, package_tx_bytes, round(package_rx_bytes/1024), round(package_tx_bytes/1024), round((package_rx_bytes+package_tx_bytes)/1024/1024)]

    # 判断设备是否root
    def is_root(self):
        if 'cannot' in self.adb_return('root'):
            return False
        else:
            return True

    # 获取设备开机时间
    def get_boot_time(self):
        s_1970 = self.shell_return('cat proc/stat | grep btime')# 1970秒数
        s_1970 = s_1970.replace('btime ', '').replace('\r', '').replace('\n', '')
        timeArray = time.localtime(int(s_1970))
        us_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return datetime.datetime.strptime(us_time, "%Y-%m-%d %H:%M:%S")

    # 获取设备已开机时间
    def get_has_boot_time(self, show='s'):
        s_1970 = self.shell_return('cat proc/stat | grep btime')  # 1970秒数
        s_1970 = s_1970.replace('btime ', '').replace('\r', '').replace('\n', '')
        time_s = time.time() - float(s_1970)
        if show == 's':
            return round(time_s, 3)
        elif show == 'm':
            return round(time_s / 60, 2)
        elif show == 'h':
            return round(time_s / 60 / 60, 1)

import json
# 支持自动序列化的基类
class archive_json(object):
    def from_json(self, json_str):
        obj = json.loads(json_str)
        for key in vars(self):
            if key in obj:
                setattr(self, key, obj[key])

    def to_json(self):
        return json.dumps(vars(self))

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        return True

