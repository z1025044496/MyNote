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
import json
import codecs

def save_json(json_str: str, file_path: str):
    res = False
    with codecs.open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_str)
        file.close()
        res = True

    return res

if __name__ == '__main__':

    ''' 1. 启动浏览器 '''
    page = ChromiumPage(addr_or_opts = 6333, timeout = 10)
    work_tab = page.get_tab()
    work_tab.set.cookies.clear()

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
    account = '15263988329'
    password = 'haifei1997?vm'
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

    ''' 4. 监听网络数据 '''
    page.listen.start('https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?jsv')

    page_input.input(2)
    work_tab.ele('.next-btn next-medium next-btn-normal next-pagination-jump-go').click()

    res = page.listen.wait()
    result: str = res.response.body
    begin = result.find('(')
    end = result.rfind(')')
    result = result[begin + 1: end]
    save_json(result, './data/1/res.json')

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
        img_path = img_ele.save(path='./data/2/', name=f'{index}.webp')
        index += 1
```

## 1. 启动或接管浏览器

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

### 页面跳转

|函数|功能|
|---|---|
|`get()`|访问链接|
|`back()`|浏览历史中后退若干步|
|`forward()`|在浏览历史中前进若干步|
|`refresh()`|刷新当前页面|
|`stop_loading()`|强制停止当前页面加载|
|`set.blocked_urls()`|设置忽略的连接|

### *元素管理*

|函数|功能|
|---|---|
|`add_ele()`|添加元素|
|`remove_ele()`|从页面上删除一个元素|

### *执行脚本或命令*

|函数|功能|
|---|---|
|`run_js()`|执行js脚本|
|`run_js_loaded()`|运行js脚本，执行前等待页面加载完毕|
|`run_async_js()`|异步方式执行js代码|
|`run_cdp()`|执行Chrome DevTools Protocol语句,cdp 用法详见[Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)|
|`run_cdp_loaded()`|此方法用于执行Chrome DevTools Protocol语句，执行前先确保页面加载完毕|

### 执行脚本或命令

|函数|功能|
|---|---|
|`set.cookies()`|设置cookie|
|`set.set.cookies.clear()`|清除所有cookie|
|`set.cookies.remove()`|删除一个cookie|
|`set.session_storage()`|设置或删除某项sessionStorage信息|
|`set.local_storage()`|设置或删除某项localStorage信息|
|`set.clear_cache()`|清除缓存，可选择要清除的项|

### 运行参数设置

|函数|功能|
|---|---|
|`set.retry_times()`|设置连接失败时重连次数|
|`set.retry_interval()`|设置连接失败时重连间隔|
|`set.timeouts()`|设置整体、页面加载、脚本运行超时时间，单位为秒。可单独设置，为None表示不改变原来设置|
|`set.load_strategy()`|设置页面加载策略，调用其方法选择某种策略|
|`set.user_agent()`|为浏览器当前标签页设置user agent|
|`set.headers()`|设置额外添加到当前页面请求headers的参数。|

### 窗口管理

|函数|功能|
|---|---|
|`set.window.max()`|窗口最大化|
|`set.window.mini()`|窗口最小化|
|`set.window.full()`|窗口切换到全屏模式|
|`set.window.normal()`|窗口切换到普通模式|
|`set.window.size()`|设置窗口大小|
|`set.window.location()`|设置窗口位置|
|`set.window.hide()`|隐藏浏览器窗口|
|`set.window.show()`|显示当前浏览器窗口|

### 页面滚动

|函数|功能|
|---|---|
|`scroll.to_top()`|滚动页面到顶部，水平位置不变|
|`scroll.to_bottom()`|滚动页面到底部，水平位置不变|
|`scroll.to_half()`|滚动页面到垂直中间位置，水平位置不变|
|`scroll.to_rightmost()`|滚动页面到最右边，垂直位置不变|
|`scroll.to_leftmost()`|滚动页面到最左边，垂直位置不变|
|`scroll.to_location()`|滚动页面到滚动到指定位置|
|`scroll.up()`|页面向上滚动若干像素，水平位置不变|
|`scroll.down()`|页面向下滚动若干像素，水平位置不变|
|`scroll.right()`|页面向右滚动若干像素，垂直位置不变|
|`scroll.left()`|页面向左滚动若干像素，垂直位置不变|
|`scroll.to_see()`|用于滚动页面直到指定元素可见|
|`set.scroll.smooth()`|是否开启平滑滚动。建议关闭|
|`set.scroll.wait_complete()`|设置滚动后是否等待滚动结束|

> [!NOTE]
> 页面滚动有两种方式，一种是滚动时直接跳到目标位置，第二种是平滑滚动，需要一定时间。后者滚动时间难以确定，容易导致程序不稳定，点击不准确的问题。

### 弹出消息处理

|函数|功能|
|---|---|
|`handle_alert()`|此方法用于处理提示框。1. 设置等待时间，等待提示框出现才进行处理，若超时没等到提示框，返回`False`。2. 获取提示框文本而不处理提示框。 3. 处理下一个出现的提示框，这在处理离开页面时触发的弹窗非常有用。|
|`set.auto_handle_alert()`(tab)|自动处理该tab的提示框，使提示框不会弹窗而直接被处理掉|
|`set.auto_handle_alert()`(page)|是否全局设置自动处理|

### 关闭及重连

|函数|功能|
|---|---|
|`disconnect()`|断开与页面的连接，但不关闭标签页|
|`reconnect()`|关闭与页面连接，然后重建一个新连接|
|`quit()`|关闭浏览器|

> [!NOTE]
> 长期运行导致内存占用过高，断开连接可释放内存，然后重连继续控制浏览器

## 4. 查找元素⭐

> `ele()`

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator（元素对象）`|`str``Tuple[str, str]`|必填|元素的定位信息。可以是查询字符串，或 loc 元组|
|`locator（页面对象）`|`str``SessionElement``Tuple[str, str]`|必填|元素的定位信息。可以是查询字符串、loc 元组或一个SessionElement对象|
|`index`|`int`|1|获取第几个匹配的元素，从1开始，可输入负数表示从后面开始数|
|`timeout`|`float`|None|等待元素出现的超时时间，为None使用页面对象设置，SessionPage中无效|

|返回类型|说明|
|---|---|
|`SessionElement`|`SessionPage`或`SessionElement`查找到的第一个符合条件的元素对象|
|`ChromiumElement`|浏览器页面对象或元素对象查找到的第一个符合条件的元素对象|
|`ChromiumFrame`|当结果是框架元素时，会返回`ChromiumFrame`，但IDE中不会包含该提示|
|`NoneElement`|未找到符合条件的元素时返回|

> [!NOTE]
> * *元组是指`selenium`定位符，例：(By.ID, 'XXXXX')。下同。  
> * `ele('xxxx', index=2)`和`eles('xxxx')[1]`结果一样，不过前者会快很多。

> `eles()`

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str``Tuple[str, str]`|必填|元素的定位信息。可以是查询字符串，或 loc 元组|
|`timeout`|`float`|None|等待元素出现的超时时间，为None使用页面对象设置，SessionPage中无效|

|返回类型|说明|
|---|---|
|`List[SessionElement]`|SessionPage或SessionElement找到的所有元素组成的列表|
|`List[ChromiumElement, ChromiumFrame]`|浏览器页面对象或元素对象找到的所有元素组成的列表|

### 基本用法

|写法|精确匹配|模糊匹配|匹配开头|匹配结尾|说明|
|---|---|---|---|---|---|
|@属性名|@属性名=|@属性名:|@属性名^|@属性名$|按某个属性查找|
|@!属性名|@!属性名=|@!属性名:|@!属性名^|@!属性名$|查找属性不符合指定条件的元素|
|text|text=|text:或不写|text^|text$|按某个文本查找|
|@text()|@text()=|@text():|text()^|text()$|text与@或@@配合使用时改为text()，常用于多条件匹配|
|tag|tag=或tag:|无|无|无|查找某个类型的元素|
|xpath|xpath=或xpath:|无|无|无|用xpath方式查找元素|
|css|css=或css:|无|无|无|用css selector方式查找元素|

### 组合查找

|写法|说明|
|---|---|
|@@属性1@@属性2|匹配属性同时符合多个条件的元素|
|@|属性1@|属性2|匹配属性符合多个条件中任一项的元素|
|@@属性1@!属性2|多属性匹配与否定匹配同时使用|
|tag:xx@属性名|tag与属性匹配共同使用|
|tag:xx@@属性1@@属性2|tag与多属性匹配共同使用|
|tab:@@text()=文本@@属性|tab与文本和属性匹配共同使用|

### 简化写法

|原写法|简化写法|精确匹配|模糊匹配|匹配开头|匹配结尾|备注|
|---|---|---|---|---|---|---|
|`@id`|`#`|`#`或`#=`|`#:`|`#^`|`#$`|简化写法只能单独使用|
|`@class`|`.`|`.`或`.=`|`.:`|`.^`|`.$`|简化写法只能单独使用|
|`tag`|`t`|`t:`或`t=`|无|无|无|只能用在句首|
|`text`|`tx`|`tx=`|`tx:`或不写|`tx^`|`tx$`|无标签时使用模糊匹配文本
|`@text()`|`@tx()`|`@tx()=`|`@tx():`|`@tx()^`|`@tx()$`|
|`xpath`|`x`|`x:`或`x=`|无|无|无|只能单独使用|
|`css`|`c`|`c:`或`c=`|无|无|无|只能单独使用|

### 相对定位⭐

|方法|说明|
|---|---|
|`parent()`|查找当前元素某一级父元素|
|`child()`|查找当前元素的一个直接子节点|
|`children()`|查找当前元素全部符合条件的直接子节点|
|`next()`|查找当前元素之后第一个符合条件的兄弟节点|
|`nexts()`|查找当前元素之后所有符合条件的兄弟节点|
|`prev()`|查找当前元素之前第一个符合条件的兄弟节点|
|`prevs()`|查找当前元素之前所有符合条件的兄弟节点|
|`after()`|查找文档中当前元素之后第一个符合条件的节点|
|`afters()`|查找文档中当前元素之后所有符合条件的节点|
|`before()`|查找文档中当前元素之前第一个符合条件的节点|
|`befores()`|查找文档中当前元素之前所有符合条件的节点|

## 5. 元素交互

## 6. iframe操作

## 7. 自动等待

## 8. 监听数据⭐

# `WebPage`
