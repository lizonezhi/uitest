# uitest
- Python >=3.6
安装：
```bash
pip install -U --pre uitest
```

导入包
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

根据文字点击“设置”

```python
e.click(text='设置')
```

根据id点击计算器的“1”

```python
e.click(resourceId='com.android.calculator2:id/digit_1')
```

根据content-desc点击计算器的“+”号

```python
e.click(content_desc='加')
```

根据本地的图片来点击设备，此处screenshot.png为脚本目录下icon文件夹里的图片
```python
print(d.find_icon_click('icon/screenshot.png'))
```

在设置里滑动查找并点击“日期和时间”，此处是点击内容包含“日期”的

```python
e.swipe_find(textContains='日期')
```

获取当前包名
```python
print(d.getCurrentPackageName())
```

获取剩余ram内存
```python
print(d.getMemFree())
```

强行停止当前应用
```python
d.force_stop(d.getCurrentPackageName())
```

获取第三方应用列表
```python
print(d.getThirdappList())
```
备注：如需打包exe，可注释掉__init__代码里的from uitest import aircv as ac, 能大幅减小exe包大小


"# uitest" 
