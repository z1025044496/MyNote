# DrissionPage库功能



* `SessionPage`：单纯用于收发数据包的页面对象
* `ChromiumPage`：单纯用于操作浏览器的页面对象
* `WebPage`：整合浏览器控制和收发数据包于一体的页面对象



#  `ChromiumPage`与Selenium库

* selenium库控制浏览器需要[chromedriver.exe](https://googlechromelabs.github.io/chrome-for-testing/)
* DrissionPage库在3.0版本之前通过selenium控制浏览器的，需要依赖selenium库，3.0后用chromium协议自行实现了selenium全部功能

## 1. 启动或接管浏览器

### `ChromiumPage`

|初始化参数|类型|默认值|说明|
|---|---|---|---|
|`addr_or_opts`|`str` `int` `ChromiumOptions`|`None`|浏览器启动配置或接管信息, 传入'ip: port'字符串、端口数字或`ChromiumOptions`对象时按配置启动或接管浏览器；为`None`时使用配置文件配置启动浏览器|
|`tab_id`|`str`|`None`|要控制的标签页id，为`None`则控制激活的标签页|
|`timeout`|`float`|`None`|整体超时时间，为`None`则从配置文件中读取，默认10|

# 手动启动浏览器时设置端口和缓存位置

```bat
"C:\Program Files\Google\Chrome\Application\chrome.exe"  --remote-debugging-port=9222  --remote-allow-origins=*  --user-data-dir="C:\Users\10250\AppData\Local\Temp\DrissionPage"
```

# 代码启动浏览器设置端口号

```python
# 设置项启动
co = ChromiumOptions().set_local_port(9222)
co.set_browser_path(r'C:/Program Files/Google/Chrome/Application/chrome.exe')
page = ChromiumPage(addr_or_opts=co)

# 直接启动
page = ChromiumPage(6222)
```

## 2. 访问网页

### `ChromiumPage`

#### 1. `get()`

|初始化参数|类型|默认值|说明|
|---|---|---|---|
|`url`|`str`|必填|目标url，可指向本地文件路径|
|`show_errmsg`|`bool`|`False`|连接出错时是否显示和抛出异常|
|`retry`|`int`|`None`|重试次数，为None时使用页面参数，默认3|
|`interval`|`float`|`None`|重试间隔（秒），为`None`时使用页面参数，默认2|
|`timeout`|`float`|`None`|加载超时时间（秒）|

**返回参数**：`bool`是否链接成功

#### 加载模式

* `normal()`：常规模式，会等待页面加载完毕，超时自动重试或停止，默认使用此模式
* `eager()`：加载完DOM或超时即停止加载，不加载页面资源
* `none()`：超时也不会自动停止，除非加载完成

前两种模式下，页面加载过程会阻塞程序，直到加载完毕才执行后面的操作。

none()模式下，只在连接阶段阻塞程序，加载阶段可自行根据情况执行stop_loading()停止加载

### Selenium



```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.set.load_mode.eager()  # 设置为eager模式
page.get('https://DrissionPage.cn')
```



## 3. 网页交互

## 4. 查找元素⭐

## 5. 元素交互

## 6. iframe 操作

## 7. 自动等待

## 8. 监听数据⭐

# `WebPage`
