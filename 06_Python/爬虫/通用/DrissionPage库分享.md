# DrissionPage库功能

* `SessionPage`：单纯用于收发数据包的页面对象
* `ChromiumPage`：单纯用于操作浏览器的页面对象
* `WebPage`：整合浏览器控制和收发数据包于一体的页面对象

# `ChromiumPage`

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
    account = '****'
    password = '****************'
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

## 2. 启动或接管浏览器

|初始化参数|类型|默认值|说明|
|---|---|---|---|
|`addr_or_opts`|`str` `int` `ChromiumOptions`|`None`|浏览器启动配置或接管信息, 传入'ip: port'字符串、端口数字或`ChromiumOptions`对象时按配置启动或接管浏览器；为`None`时使用配置文件配置启动浏览器|
|`tab_id`|`str`|`None`|要控制的标签页id，为`None`则控制激活的标签页|
|`timeout`|`float`|`None`|整体超时时间，为`None`则从配置文件中读取，默认10|

### 手动启动浏览器时设置端口和缓存位置

```bat
"C:\Program Files\Google\Chrome\Application\chrome.exe"  --remote-debugging-port=9222  --remote-allow-origins=*  --user-data-dir="C:\Users\10250\AppData\Local\Temp\DrissionPage"
```

### 代码启动浏览器设置端口号

```python
# 设置项启动
co = ChromiumOptions().set_local_port(9222)
co.set_browser_path(r'C:/Program Files/Google/Chrome/Application/chrome.exe')
page = ChromiumPage(addr_or_opts=co)

# 直接启动
page = ChromiumPage(6222)
```

## 3. 访问网页

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

## 4. 网页交互

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

## 5. 查找元素⭐

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
>
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

### selenium转换

selenium查找

``` python
from selenium.webdriver.common.by import By, webdriver

driver = webdriver.Chrome()
driver.get('https://www.shipxy.com')
driver.find_element(By.ID, "txtKey")
```

DrissionPage查找

```python
from DrissionPage import ChromiumPage
from DrissionPage.common import By

page = ChromiumPage()
page.get('https://www.shipxy.com')
page.ele(By.ID, 'txtKey')
page.ele('#txtKey')
```

## 6. 元素交互

### 鼠标点击

|方法|说明|
|---|---|
|`click()`|左键点击元素。可选择模拟点击或js点击，**在模拟点击前，程序会先尝试把元素滚动到视口中**|
|`click.left()`|左键点击元素。可选择模拟点击或js点击，**在模拟点击前，程序会先尝试把元素滚动到视口中**|
|`click.right()`|右键单击元素|
|`click.middle()`|中键单击元素|
|`click.multi()`|左键多次点击元素|
|`click.at()`|带偏移量点击元素，偏移量相对于元素左上角坐标。不传入`offset_x`和`offset_y`时点击元素中间点|
|`click.to_upload()`|点击元素，触发文件选择框并把指定的文件路径添加到网页|
|`click.to_upload()`|点击元素触发下载，并返回下载任务对象|
|`click.for_new_tab()`|点击后会出现新tab的时候，可用此方法点击，会等待并返回新tab对象|

> [!NOTE]
>
> 1. 鼠标点击中`click()`/`click.left()`/`click.to_upload()`/`click.to_download()`/`click.for_new_tab()`可以选择JS点击或者模拟点击
> 2. 模拟点击会先尝试把元素滚动到视口中
> 3. JS点击可以无视元素遮挡

### 输入内容

|方法|说明|
|---|---|
|`clear()`|清空元素文本，可选择模拟按键或js方式|
|`input()`|输入文本或组合键，也可用于输入文件路径到上传控件。可选择输入前是否清空元素，可选择模拟按键或js方式|
|`focus()`|使元素获取焦点|

> [!NOTE]
>
> 1. 模拟按键是模拟键盘的输入
> 2. JS方式不能使用组合键,是直接设置元素value属性

#### 输入组合键

```python
from DrissionPage.common import Keys

ele.input((Keys.CTRL, 'a', Keys.DEL))  # ctrl+a+del

# Keys内置了5个常用组合键，分别为CTRL_A、CTRL_C、CTRL_X、CTRL_V、CTRL_Z、CTRL_Y
ele.input(Keys.CTRL_A)  # 全选
```

### 拖拽和悬停

|方法|说明|
|---|---|
|`drag()`|拖拽元素到相对于当前的一个新位置，可以设置速度|
|`drag_to()`|拖拽元素到另一个元素上或一个坐标上|
|`hover()`|模拟鼠标悬停在元素上，可接受偏移量，偏移量相对于元素左上角坐标。不传入`offset_x`和`offset_y`值时悬停在元素中点|

### *修改元素/执行 js 脚本*

### 元素滚动

|函数|功能|
|---|---|
|`scroll.to_top()`|滚动到元素顶部，水平位置不变|
|`scroll.to_bottom()`|滚动到元素底部，水平位置不变|
|`scroll.to_half()`|滚动到元素垂直中间位置，水平位置不变|
|`scroll.to_rightmost()`|滚动到元素最右边，垂直位置不变|
|`scroll.to_leftmost()`|滚动到元素最左边，垂直位置不变|
|`scroll.to_location()`|元素滚动到指定位置|
|`scroll.up()`|使元素向上滚动若干像素，水平位置不变|
|`scroll.down()`|使元素向下滚动若干像素，水平位置不变|
|`scroll.right()`|使元素内滚动条向右滚动若干像素，垂直位置不变|
|`scroll.left()`|使元素内滚动条向左滚动若干像素，垂直位置不变|
|`scroll.to_see()`|滚动页面直到元素可见|
|`scroll.to_center()`|尽量把元素滚动到视口正中|

### 列表选择

`<select>`下拉列表元素功能在`select`属性中。可自动等待列表项出现再实施选择。

此属性用于对`<select>`元素的操作。非`<select>`元素此属性为None。

<select multiple>
    <option value='value1'>苹果</option>
    <option value='value2'>西瓜</option>
    <option value='value3'>香蕉</option>
</select>

### 模拟点击方式

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
ele = page('t:select')('t:option')
ele.click()
```

### 功能

|函数|功能|
|---|---|
|`select()`和`select.by_text()`|按文本选择列表项。如为多选列表，可多选|
|`select.by_value()`|按`value`属性选择列表项。如为多选列表，可多选|
|`select.by_index()`|按序号选择列表项，从1开始。如为多选列表，可多选|
|`select.by_locator()`|可用定位符筛选选项元素。如为多选列表，可多选|
|`select.by_option()`|选中单个或多个列表项元素。如为多选列表，可多选|
|`select.cancel_by_text()`|文本取消选择列表项。如为多选列表，可取消多项|
|`select.by_valuecancel_by_value()`|按`value`属性取消选择列表项。如为多选列表，可多选|
|`select.cancel_by_index()`|按序号取消选择列表项，从1开始。如为多选列表，可多选|
|`select.cancel_by_locator()`|可用定位符筛选取消选项元素。如为多选列表，可多选|
|`select.cancel_by_option()`|取消选中单个或多个列表项元素。如为多选列表，可多选|
|`select.is_multi`|元素是否多选列表|
|`select.options`|当前列表元素所有选项元素对象|
|`select.selected_option`|当前列表元素所有选项元素对象|

> 多选列表生效

|函数|功能|
|---|---|
|`select.all()`|全选所有项|
|`select.clear()`|取消所有项选中状态|
|`select.invert()`|用于反选|
|`select.selected_options`|当前列表元素所有选项元素对象|

## 7. 自动等待

### 页面自动等待⭐

|函数|功能|
|---|---|
|`wait.load_start()`|用于等待页面进入加载状态|
|`wait.doc_loaded()`|等待页面文档加载完成|
|`wait.eles_loaded()`⭐|等待元素被加载|
|`wait.ele_displayed()`⭐|等待一个元素变成显示状态|
|`wait.ele_hidden()`⭐|等待一个元素变成隐藏状态|
|`wait.ele_deleted()`⭐|等待一个元素被删除|
|`wait.download_begin()`|等待下载开始|
|`wait.upload_paths_inputted()`|等待自动填写上传文件路径|
|`wait.new_tab()`|等待新标签页出现|
|`wait.title_change()`⭐|等待title变成包含或不包含指定文本|
|`wait.title_change()`⭐|等待url变成包含或不包含指定文本|
|`wait()`|等待若干秒|

### 元素对象自动等待

|函数|功能|
|---|---|
|`wait.displayed()`|等待元素从隐藏状态变成显示状态|
|`wait.hidden()`|元素从显示状态变成隐藏状态|
|`wait.deleted()`|等待元素被从删除|
|`wait.covered()`|等待元素被其它元素覆盖|
|`wait.not_covered()`|等待元素不被其它元素覆盖|
|`wait.enabled()`|等待元素变为可用状态|
|`wait.disabled()`|用于等待元素变为不可用状态|
|`wait.stop_moving()`|等待元素运动结束|
|`wait.clickable()`|等待元素可被点击|
|`wait.disabled_or_deleted()`|等待元素变为不可用或被删除|
|`wait()`|等待若干秒|

## 8. 监听数据⭐

### 设置目标和启动监听

#### 📎`listen.start()`

启动监听器，启动同时可设置获取的目标特征

1. 参数

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`targets`|`str`/`list`/`tuple`/`set`|`None`|要匹配的数据包url特征，可用列表指定多个，为`True`时获取所有|
|`is_regex`|`bool`|`None`|设置的target是否正则表达式，为`None`时保持原来设置|
|`method`|`str`/`list`/`tuple`/`set`|`None`|设置监听的请求类型，可指定多个，默认(`GET`, `POST`)，为`True`时监听所有，为`None`时保持原来设置|
|`res_type`|`str`/`list`/`tuple`/`set`|`None`|设置监听的`ResourceType`类型，可指定多个，为`True`时监听所有，为`None`时保持原来设置|

2. 返回值

返回：`None`

> [!NOTE]
>
> 1. 多个特征，符合条件的数据包会被获取
> 2. 监听未停止时调用这个方法，可清除已抓取的队列

> [!WARNING]
>
> 1. 当`targets`不为`None`，`is_regex`会自动设为`False`
> 2. 即如要使用正则，每次设置`targets`时需显式指定`is_regex=True`

#### 📎`listen.set_targets()`

可在监听过程中修改监听目标，也可在监听开始前设置

1. 参数

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`targets`|`str`/`list`/`tuple`/`set`|`None`|要匹配的数据包url特征，可用列表指定多个，为`True`时获取所有|
|`is_regex`|`bool`|`None`|设置的target是否正则表达式，为`None`时保持原来设置|
|`method`|`str`/`list`/`tuple`/`set`|`None`|设置监听的请求类型，可指定多个，默认(`GET`, `POST`)，为`True`时监听所有，为`None`时保持原来设置|
|`res_type`|`str`/`list`/`tuple`/`set`|`None`|设置监听的`ResourceType`类型，可指定多个，为`True`时监听所有，为`None`时保持原来设置|

2. 返回值

返回：`None`

### 等待和获取数据包

#### 📎`listen.wait()`

用于等待符合要求的数据包到达指定数量

> [!NOTE]
> 所有符合条件的数据包都会存储到队列，wait()实际上是逐个从队列中取结果，不用担心页面已刷走而丢包。

1. 参数

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`count`|`int`|1|需要捕捉的数据包数量|
|`timeout`|`float`/`None`|`None`|超时时间，为`None`无限等待|
|`fit_count`|`bool`|`True`|是否必需满足总数要求，如超时，为`True`返回`False`，为`False`返回已捕捉到的数据包|
|`raise_err`|`bool`|`None`|超时时是否抛出错误，为`None`时根据`Settings`设置，如不抛出，超时返回`False`|

2. 返回值

|返回类型|说明|
|---|---|
|`DataPacket`|`count`为1且未超时，返回一个数据包对象|
|`List[DataPacket]`|`count`大于1，未超时或`fit_count`为`False`，返回数据包对象组成的列表|
|`False`|超时且`fit_count`为`True`时|

#### 📎listen.steps()

返回一个可迭代对象，用于for循环，每次循环可从中获取到的数据包

1. 参数

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`count`|`int`|`None`|需捕获的数据包总数，为`None`表示无限|
|`timeout`|`float`/`None`|`None`|超时时间，为`None`无限等待|
|`gap`|`int`|1|每接收到多少个数据包返回一次数据|

2. 返回值

|返回类型|说明|
|---|---|
|`DataPacket`|`count`为1且未超时，返回一个数据包对象|
|`List[DataPacket]`|`count`大于1，未超时或`fit_count`为`False`，返回数据包对象组成的列表|

#### 📎listen.wait_silent()

等待所有指定的请求完成

1. 参数

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`timeout`|`float`/`None`|`None`|等待时间，为None表示无限等待|
|`targets_only`|`bool`|`False`|是否只等待`targets`指定的请求结束|
|`limit`|`int`|0|剩下多少个连接时视为结束|

2. 返回值

|返回类型|说明|
|---|---|
|`bool`|是否等待成功|

### 暂停和恢复

|方法|说明|
|---|---|
|`listen.pause()`|暂停监听,可以选择是否清空已获取队列|
|`listen.resume()`|继续暂停的监听|
|`listen.stop()`|终止监听器的运行，会清空已获取的队列，不清空`targets`|

### DataPacket对象

`DataPacket`对象是获取到的数据包结果对象，包含了数据包各种信息

#### 对象属性

|属性名称|数据类型|说明|
|---|---|---|
|`tab_id`|`str`|产生这个请求的标签页的id|
|`frameId`|`str`|产生这个请求的框架id|
|`target`|`str`|产生这个请求的监听目标|
|`url`|`str`|数据包请求网址|
|`method`|`str`|请求类型|
|`is_failed`|`bool`|是否连接失败|
|`resourceType`|`str`|资源类型|
|`request`|`Request`|保存请求信息的对象|
|`response`|`Response`|保存响应信息的对象|
|`fail_info`|`FailInof`|保存连接失败信息的对象|

#### 📎wait_extra_info()

有些数据包有`extra_info`数据，但这些数据可能会迟于数据包返回，用这个方法可以等待这些数据加载到数据包对象

1. 参数

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`timeout`|`float`/`None`|`None`|等待时间，为None表示无限等待|  

2. 返回值

|返回类型|说明|
|---|---|
|`bool`|是否等待成功|

#### Request对象

`Request`对象是`DataPacket`对象内用于保存请求信息的对象，有以下属性：

|属性名称|数据类型|说明|
|---|---|---|
|`url`|`str`|请求的网址|
|`method`|`str`|请求类型|
|`headers`|`CaseInsensitiveDict`|以大小写不敏感字典返回headers数据|
|`cookies`|`list[dict]`|返回发送的cookies|
|`postData`|`str`/`dict`|post类型的请求所提交的数据，json以`dict`格式返回|

#### Response对象

`Response`对象是`DataPacket`对象内用于保存响应信息的对象，有以下属性：

|属性名称|数据类型|说明|
|---|---|---|
|`url`|`str`|请求的网址|
|`headers`|`CaseInsensitiveDict`|以大小写不敏感字典返回headers数据|
|`body`|`str`/`byte`/`dict`|如果是json格式，转换为`dict`；如果是base64格式，转换为`bytes`，其它格式直接返回文本|
|`raw_body`|`str`|未被处理的body文本|
|`status`|`int`|请求状态|
|`statusText`|`str`|请求状态文本|

#### FailInfo对象

`FailInfo`对象是`DataPacket`对象内用于保存连接失败信息的对象，有以下属性：

|属性名称|数据类型|说明|
|---|---|---|
|`errorText`|`str`|错误信息文本|
|`canceled`|`bool`|是否取消|
|`blockedReason`|`str`|拦截原因|
|`corsErrorStatus`|`str`|cors错误状态|

## 9. iframe操作❓

与`selenium`不同，`DrissionPage`无需切入切出即可处理`<iframe>` 元素。因此可实现跨级元素查找、元素内部单独跳转、同时操作`<iframe>`内外元素、多线程控制多个`<iframe>`等操作，功能更灵活，逻辑更清晰。

> [!NOTE]
> `DrissionPage`通过`get_frame()`函数获取`ChromiumFrame`对象来操作iframe,`ChromiumFrame`操作和``ChromiumPage`操作一致

## 10. 动作链❓

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://www.baidu.com')
page.actions.move_to('#kw').click().type('DrissionPage')
page.actions.move_to('#su').click()
```

>❓  
>鼠标虽然没有移动,但是鼠标样式变了, 不清楚是否能解决反爬

## 11. 截图和录像

|函数|功能|
|---|---|
|`get_screenshot()`(页面)|页面截图,可对整个网页、可见网页、指定范围截图,可选择本地保存或者以字节/base64形式返回图片|
|`screencast.set_mode.video_mode()`|持续录制页面，停止时生成没有声音的视频|
|`screencast.set_mode.frugal_video_mode()`|页面有变化时才录制，停止时生成没有声音的视频|
|`screencast.set_mode.js_video_mode()`|可生成有声音的视频，但需要手动启动|
|`screencast.set_mode.imgs_mode()`|持续对页面进行截图|
|`screencast.set_mode.frugal_imgs_mode()`|页面有变化时才保存页面图像|
|`screencast.set_save_path()`|设置录制结果保存路径|
|`screencast.start()`|开始录制浏览器窗口|
|`screencast.stop()`|停止录取屏幕|
