# uitest
- Python >=3.6

安装：
```bash
pip install -U --pre uitest
```

使用
```python
import uitest
```

获得设备实例，入参（'12344321'）为序列号，一台设备可不填，可以直接操作adb命令
```python
d = uitest.Device('12344321')
```

获取元素实例，入参（'12344321'）为序列号，一台设备可不填，获取元素坐标和信息
```python
e = uitest.Element('12344321')
```

点亮屏幕

```python
d.screen_on()
```

根据文字点击“设置”,等待5秒

```python
e.click(text='设置',timeout=5)
```

根据id点击计算器的“1”

```python
e.click(resourceId='com.android.calculator2:id/digit_1')
```

根据content-desc点击计算器的“+”号

```python
e.click(content_desc='加')
```

根据id或者其它属性获取此控件的信息

```python
e.info(resourceId='com.android.calculator2:id/digit_1')
```

例如根据id获取此控件的text值

```python
e.info(resourceId='com.android.calculator2:id/digit_1')['text']
```

判断此控件是否存在

```python
if e.exists(resourceId='com.android.calculator2:id/digit_1'):
	print('存在')
else:
	print('不存在')
```


根据本地的图片来点击设备，此处screenshot.png为脚本目录下icon文件夹里的图片
```python
print(d.find_icon_click('icon/screenshot.png'))
```

在设置里滑动查找并点击“日期和时间”，此处是点击内容包含“日期”的

```python
e.swipe_find(textContains='日期')
```

等待元素出现。
str是命令行显示内容，自定义；
text表示根据text查找；也可根据resourceId、content_desc、textContains、icon_name查找；
click为True表示找到后就点击，为False不点击

```python
e.time_jishi(str="等待", text='交易成功', click=True)
```

运行adb命令
```python
d.adb_return('adb命令')
```

运行shell命令
```python
d.shell_return('shell命令')
```

获取设备中的Android版本号，如4.2.2
```python
print(d.getAndroidVersion())
```

获取Android平台型号品牌
```python
print(d.get_brand())
```

获取设备SDK版本号,如19
```python
print(d.getSdkVersion())
```

获取设备型号
```python
print(d.getDeviceModel())
```

获取os版本
```python
print(d.getOsVersion())
```

根据包名获取进程pid
```python
print(d.getPid(“com.lzz.cash”))
```

获取当前运行的应用的包名
```python
print(d.getCurrentPackageName())
```

获取当前运行应用的activity
```python
print(d.getCurrentActivity())
```

获取最大内存
```python
print(d.getMemTotal())
```

获取剩余内存
```python
print(d.getMemFree())
```

获取cpu型号
```python
print(d.getCpuHardware())
```

获取电池电量
```python
print(d.getBatteryLevel())
```

获取电池电压,单位mV毫伏
```python
print(d.getBatteryVoltage())
```

电池健康状态：只有数字2表示good
```python
print(d.getBatteryHealth())
```

电池是否在AC充电器充电
```python
print(d.getBatteryACpowered())
```

电池是否安装在机身
```python
print(d.getBatteryPresent())
```

获取电池充电状态：未知状态\充电状态\放电状态\未充电\充电已满
```python
print(d.getBatteryStatus())
```

获取电池温度
```python
print(d.getBatteryTemp())
```

此手机的单个应用程序最大内存限制，超过这个值会产生OOM(内存溢出）
测程序一般看这个
```python
print(d.get_heapgrowthlimit())
```

获取设备屏幕分辨率，return (width, high)
```python
print(d.getScreenResolution())
```

截图，保存到脚本"tmp\screenshot"目录里
```python
d.screenshot("文件名，可不填，默认是screenshot.png")
```

获取设备中安装的系统应用包名列表
```python
print(d.getSystemAppList())
```

获取设备中安装的第三方应用包名列表
```python
print(d.getThirdAppList())
```

模糊查询应用包名列表
```python
print(d.getMatchingAppList("qq"))
```

获取启动应用所花时间，单位毫秒
```python
print(d.getAppStartTotalTime("com.android.settings/.Settings"))
```

根据包名判断应用是否安装，已安装返回True，否则返回False
```python
print(d.isInstall("com.example.apidemo"))
```

清除应用用户数据
```python
print(d.clearAppData("com.android.contacts"))
```

启动一个Activity
```python
print(d.startActivity("com.android.settinrs/.Settings"))
```

启动一个应用
```python
print(d.start_app("com.android.settings"))
```

使用系统默认浏览器打开一个网页
```python
print(d.startWebpage("http://www.baidu.com"))
```

启动拨号器拨打电话
```python
print(d.callPhone(10086))
```

发送一个按键事件。先输入uitest.Keycode.有代码提示。
```python
print(d.sendKeyEvent(uitest.Keycode.增加音量))
```

发送一个按键长按事件，Android 4.4以上
```python
print(d.longPressKey(uitest.Keycode.HOME键))
```

发送触摸点击事件,支持具体坐标和百分比坐标
```python
print(d.click(0.5, 0.5))
```

发送滑动事件，Android 4.4以上可选duration(ms)
```python
print(d.swipe(0.9, 0.5, 0.1, 0.5))
```

长按屏幕的某个坐标位置, Android 4.4及以上
```python
print(d.click_long(500, 600))
print(d.click_long(0.2, 0.9))
```

发送一段文本，只能包含英文字符和空格
```python
print(d.setText("i am unique"))
```

获取内存,并写入到txt中记录
```python
print(d.get_meminfo_heap("com.tencent.cash"))
```

取日志到“tmp\logcat”下
```python
print(d.logcat_pull(**msg))
```

push电脑本地文件到手机
```python
print(d.push(local, remote, override=True))
```

判断手机内部文件是否存在
```python
print(d.is_remote_file_exist(“sdcard/11.png”))
```

pull手机里的文件到电脑本地
```python
print(d.pull(“sdcard/11.png”))
```

判断屏幕是否点亮
```python
print(d.is_screen_on())
```

判断WiFi是否打开
```python
print(d.is_wifi_on())
```

获取ip地址
```python
print(d.ipAddress())
```

获取物理网卡mac地址
```python
print(d.get_mac())
```

获取设备里已装程序版本信息
```python
print(d.getVersionName("com.tencent.qq"))
```

获取sn号
```python
print(d.get_sn())
```

返回
```python
print(d.back())
```

获取指定包名的应用的wifi流量消耗, 目前只针对部分机型
```python
print(d.get_allnet("com.tencent.qq"))
```

写入内容到电脑本地txt文件,name：文件名，context：txt里的内容
```python
uitest.write_txt_file(name='记录日志', content='123')
```

打印带颜色的字
```python
uitest.print_color('你好', 红色)
```

强行停止当前应用
```python
d.force_stop(d.getCurrentPackageName())
```

备注：如需打包exe，可注释掉__init__代码里的from uitest import aircv as ac, 能大幅减小exe包大小

"# uitest" 
"# uitest" 
