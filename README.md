# uitest
基于adb的安卓自动化操作
安装：

pip install -U --pre uitest


导入包

import uitest



获得设备实例，入参（'12344321'）为序列号，一台设备可不填，作用是可以直接操作adb和shell命令

a = uitest.Device('12344321')


获取元素实例，入参（'12344321'）为序列号，一台设备可不填，作用是获取元素坐标和信息

e = uitest.Element('12344321')


例如：点击“设置”

a.click(e.d(text='设置'))

或者

e.click(text='设置')



获取当前包名

print(a.getCurrentPackageName())


获取剩余ram内存

print(a.getMemFree())


强行停止当前应用

a.force_stop(a.getCurrentPackageName())


获取第三方应用列表

print(a.getThirdAppList())


根据本地的图片来点击设备

print(a.find_icon_click('icon/screenshot.png'))
"# uitest" 
