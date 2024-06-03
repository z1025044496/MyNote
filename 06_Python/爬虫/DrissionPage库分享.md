# DrissionPage库功能



* `SessionPage`：单纯用于收发数据包的页面对象
* `ChromiumPage`：单纯用于操作浏览器的页面对象
* `WebPage`：整合浏览器控制和收发数据包于一体的页面对象



#  `ChromiumPage`

* selenium库控制浏览器需要[chromedriver.exe](https://googlechromelabs.github.io/chrome-for-testing/)
* DrissionPage库在3.0版本之前通过selenium控制浏览器的，需要依赖selenium库，3.0后用chromium协议自行实现了selenium全部功能

## 1. ChromiumPage自动化采集流程

```python
from DrissionPage import ChromiumPage
import time
import sys

if __name__ == '__main__':
    ''' 1. 启动浏览器 '''
    from DrissionPage import ChromiumPage

    ''' 1. 启动浏览器 '''
    page = ChromiumPage(addr_or_opts = 6333, timeout = 10)
    work_tab = page.get_tab()

    ''' 2. 访问网页 '''
    work_tab.get('https://login.taobao.com/member/login.jhtml')

    # 等待元素加载
    work_tab.wait.ele_loaded('login-box-warp')

    print(('已加载到淘宝登录页'))

    login_blocks = work_tab.ele('.login-blocks qrcode-bottom-links')
    if login_blocks:
        print('当前为扫码登录，需要切换到账号密码登录')
        password_logins = login_blocks.eles('tag:a')
        for item in password_logins:
            if item.text == '密码登录':
                item.click()
                work_tab.wait.ele_loaded('@name=fm-login-id')
                print('已切换到账号密码登录')

    ''' 3. 网页交互 '''
    # 输入框
    account = '****'
    password = '*********'
    work_tab.ele('@name=fm-login-id').input(account, True)
    time.sleep(2)
    work_tab.ele('@name=fm-login-password').input(password, True)
    # 按钮
    work_tab.ele('.fm-button fm-submit password-login').click()

    # 等待标题栏改
    work_tab.wait.title_change(text='淘宝网 - 淘！我喜欢', exclude=True, timeout=10)

    error_msg = work_tab.ele('.login-error-msg')
    if error_msg: 
        print('账号名或登录密码不正确')
        sys.exit(-1)
    if work_tab.title == "登录-身份验证":
        while True:
            print("登录淘宝需要身份验证，请完成身份验证")
            if work_tab.title != "登录-身份验证":
                print("已完成身份验证")
                break
            time.sleep(3)
    if work_tab.title == "我的淘宝":
        work_tab.get('https://www.taobao.com')
        work_tab.wait.ele_loaded('.btn-search tb-bg')

    search_input = work_tab.ele('#q')
    if not search_input:
        print('没有找到搜索框！')
        sys.exit(-1)

    search_input.input('红富士')
    work_tab.ele('.btn-search tb-bg').click()
    time.sleep(1)
    # 等待元素加载
    page_input = work_tab.wait.ele_loaded('tag:input@@aria-label=请输入跳转到第几页')

    page_input.input(2)
    work_tab.ele('.next-btn next-medium next-btn-normal next-pagination-jump-go').click()

    ''' 4. 监听网络数据 '''

    ''' 5. 保存缓存 '''
    work_tab.wait.ele_deleted('.Loading--loadingBox--o15KRQY')

    for i in range(0, 99):
        work_tab.scroll.down(50)
        time.sleep(0.1)

    content = work_tab.ele('.Content--contentInner--QVTcU0M')
    items = content.eles('@data-name=itemExp')
    index = 1
    for item in items:
        img_ele = item.ele('tag:img')
        img_ele.save(path='./image/', name=f'{index}.jpg')
        index += 1
```

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
