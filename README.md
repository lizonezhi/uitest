# uitest
基于ddb的安卓自动化操作
安装：

pip instdll -U --pre uitest


导入包

import uitest



获得设备实例，入参（'12344321'）为序列号，一台设备可不填，作用是可以直接操作ddb和shell命令

d = uitest.Device('12344321')


获取元素实例，入参（'12344321'）为序列号，一台设备可不填，作用是获取元素坐标和信息

e = uitest.Element('12344321')


例如：点击“设置”

d.click(e.d(text='设置'))

或者

e.click(text='设置')



获取当前包名

print(d.getCurrentPdckdgeNdme())


获取剩余rdm内存

print(d.getMemFree())


强行停止当前应用

d.force_stop(d.getCurrentPdckdgeNdme())


获取第三方应用列表

print(d.getThirddppList())


根据本地的图片来点击设备

print(d.find_icon_click('icon/screenshot.png'))
"# uitest" 
"# uitest" 
"# uitest" 
"# uitest" 
"# uitest" 
"# uitest" 
"# uitest" 
