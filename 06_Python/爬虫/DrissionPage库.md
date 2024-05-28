# 

# ChromiumPage

## 1. 启动或者接管浏览器

### 启动参数

``` python
class ChromiumPage(
    addr_or_opts: str | int | ChromiumOptions = None,
    tab_id: str = None,
    timeout: float = None
)
```

|参数|类型|默认值|说明|
|---|---|---|---|
|`addr_or_opts`|int/str/ChromiumOptions|None|浏览器启动配置或接管信息。传入 'ip: port' 字符串、端口数字或`ChromiumOptions`对象时按配置启动或接管浏览器；为`None`时使用配置文件配置启动浏览器|
|`tab_id`|str|None|要控制的标签页 id，为`None`则控制激活的标签页|
|`timeout`|float|None|整体超时时间，为`None`则从配置文件中读取，默认10|

### 直接创建

> 默认方式

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
```

浏览器启动顺序：

1. 当前路径下浏览器可执行文件路径为'chrome'
2. Windows 系统下程序会在注册表中查找路径。
3. 直接创建时，程序默认读取 ini 文件配置，如 ini 文件不存在，会使用内置配置。

> 指定端口或地址

创建`ChromiumPage`对象时向`addr_or_opts`参数传入端口号或地址，可接管指定端口浏览器，若端口空闲，使用默认配置在该端口启动一个浏览器。

传入端口时用int类型，传入地址时用'address:port'格式。

```pyton
# 接管9333端口的浏览器，如该端口空闲，启动一个浏览器
page = ChromiumPage(9333)
page = ChromiumPage('127.0.0.1:9333')
```

### 通过配置信息创建

如果需要已指定方式启动浏览器，可使用ChromiumOptions

> 使用方法

|初始化参数|类型|默认值|说明|
|---|---|---|---|
|`read_file`|bool|True|是否从ini文件中读取配置信息，如果为False则用默认配置创建|
|`ini_path`|str|None|文件路径，为`None`则读取默认ini文件|

> [!WARNING]
> * 配置对象只有在启动浏览器时生效。
> * 浏览器创建后再修改这个配置是没有效果的。
> * 接管已打开的浏览器配置也不会生效。

```python
# 导入 ChromiumOptions
from DrissionPage import ChromiumPage, ChromiumOptions

# 创建浏览器配置对象，指定浏览器路径
co = ChromiumOptions().set_browser_path(r'D:\chrome.exe')
# 用该配置创建页面对象
page = ChromiumPage(addr_or_opts=co)
```

> 直接指定地址创建

使用这种方式时，如果浏览器已存在，程序会直接接管；如不存在，程序会读取默认配置文件配置，在指定端口启动浏览器。

```python
page = ChromiumPage(addr_or_opts='127.0.0.1:9333')
```

> 使用指定ini文件创建

```python
from DrissionPage import ChromiumPage, ChromiumOptions

# 创建配置对象时指定要读取的ini文件路径
co = ChromiumOptions(ini_path=r'./config1.ini')
# 使用该配置对象创建页面
page = ChromiumPage(addr_or_opts=co)
```

### 接管已打开的浏览器

1. 默认方式启动会接管上一次默认启动的浏览器

2. 手动打开的浏览器指定端口号

`D:\chrome.exe --remote-debugging-port=9222 --remote-allow-origins=*`

3. 或者bat文件启动，写好端口号
`"D:\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=*`

### 多浏览器共存

需要控制多个浏览器时，需要对每个浏览器指定**端口号**和**启动路径**。

1. 每个浏览器用单独的`ChromiumOptions`对象进行设置

```python
from DrissionPage import ChromiumPage, ChromiumOptions   

# 创建多个配置对象，每个指定不同的端口号和用户文件夹路径
do1 = ChromiumOptions().set_paths(local_port=9111, user_data_path=r'D:\data1')
do2 = ChromiumOptions().set_paths(local_port=9222, user_data_path=r'D:\data2')   

# 创建多个页面对象
page1 = ChromiumPage(addr_or_opts=do1)
page2 = ChromiumPage(addr_or_opts=do2)  

# 每个页面对象控制一个浏览器
page1.get('https://www.baidu.com')
page2.get('https://www.bing.com')
```

2. auto_port()方法可以使用空闲的端口和临时文件夹创建浏览器，这种方法创建的浏览器不能重复使用

```python
from DrissionPage import ChromiumPage, ChromiumOptions

co1 = ChromiumOptions().auto_port()
co2 = ChromiumOptions().auto_port()

page1 = ChromiumPage(addr_or_opts=co1)
page2 = ChromiumPage(addr_or_opts=co2)

page1.get('https://www.baidu.com')
page2.get('http://www.163.com')
```

3. 把自动分配的配置记录到ini文件，配置后直接创建即可

```python
from DrissionPage import ChromiumOptions   

ChromiumOptions().auto_port(True).save()
```

> [!TIP]
> * `auto_port()`支持多线程，但不支持多进程。
> * 多进程使用时，可用scope参数指定每个进程使用的端口范围，以免发生冲突。

## 2. 访问网页

### `get()参数`

|参数名|称类型|默认值|说明|
|---|---|---|---|
|`url`|str|必填|目标url，可指向本地文件路径|
|`show_errmsg`|bool|False|连接出错时是否显示和抛出异常|
|`retry`|int|None|重试次数，为`None`时使用页面参数，默认3|
|`interval`|float|None|重试间隔（秒），为`None`时使用页面参数，默认2|
|`timeout`|float|None|加载超时时间（秒）|

**返回值**：bool，是否访问成功

### 加载模式

`normal()`：常规模式，会等待页面加载完毕，超时自动重试或停止，默认使用此模式   
`eager()`： 加载完 DOM 或超时即停止加载，不加载页面资源   
`none()`：  超时也不会自动停止，除非加载完成，加载阶段可自行根据情况执行stop_loading()停止加载。   

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.set.load_mode.eager()  # 设置为eager模式
page.get('https://www.baidu.com')
```

## 3. 获取网页信息

|变量/函数|类型|返回值|说明|
|---|---|---|---|
|页面信息|
|`html`|`str`|/|返回当前页面html文本|
|`json`|`str`|/|此属性把请求内容解析成 json。假如用浏览器访问会返回 *.json 文件的 url，浏览器会把 json 数据显示出来，这个参数可以把这些数据转换为dict格式。如果是API返回的json字符串，请使用 SessionPage 对象而不是 ChromiumPage。|
|`title`|`str`|/|返回当前页面title文本。|
|`user_agent`|`str`|/|返回当前页面 user agent 信息。|
|`browser_version`|`str`|/|返回当前浏览器版本号。|
|`save()`|`path`: 保存路径   `name`: 保存的文件名   `as_pdf`: 为`Ture`保存为 pdf，否则保存为mhtml 且忽略`kwargs`参数   `**kwargs`: pdf 生成参数|`as_pdf`为`False`时返回mhtml文本，为`True`时返回文件字节数据|当前页面保存为文件，同时返回保存的内容。|
|运行状态信息|
|`url`|`str`|\|此属性返回当前访问的 url。|
|`address`|`str`|\|返回当前对象控制的页面地址和端口。|
|`tab_id`|`str`|\|属性返回当前标签页的id|
|`process_id`|`str`|\|此属性返回浏览器进程id。|
|`process_id`|`int` `None`|\|此属性返回浏览器进程id。|
|`states.is_loading`|`bool`|\|返回页面是否正在加载状态。|
|`states.ready_state`|`str`|`connecting`：网页连接中   `loading`：表示文档还在加载中   `interactive`：DOM已加载，但资源未加载完成  `complete`：所有内容已完成加载|此属性返回页面当前加载状态|
|`url_available`|`bool`|\|值返回当前链接是否可用。|
|`states.has_alert`|`bool`|\|返回页面是否存在弹出框。|
|窗口信息|
|`rect.size`|`Tuple[int, int]`|\|返回页面大小，格式：(宽, 高)|
|`rect.window_size`|`Tuple[int, int]`|\|返回页面大小，格式：(宽, 高)|
|`rect.window_location`|`Tuple[int, int]`|\|返回窗口在屏幕上的坐标，左上角为(0, 0)。|
|`rect.window_state`|`str`|\|此属性以返回窗口当前状态，有`normal`、`fullscreen`、`maximized`、 `minimized`几种|
|`rect.viewport_size`|`Tuple[int, int]`|\|返回视口大小，不含滚动条。|
|`rect.viewport_size_with_scrollbar`|`Tuple[int, int]`|\|返回浏览器窗口大小，含滚动条，格式：(宽, 高)|
|`rect.page_location`|`Tuple[int, int]`|\|返回页面左上角在屏幕中坐标，左上角为(0, 0)。|
|`rect.viewport_location`|`Tuple[int, int]`|\|返回视口在屏幕中坐标，左上角为(0, 0)。|
|配置参数信息|
|`timeout`|`int`、`float`|\|整体默认超时时间，包括元素查找、点击、处理提示框、列表选择等需要用到超时设置的地方，都以这个数据为默认值。默认为 10，可对其赋值。|
|`timeouts`|`base`：与`timeout`属性是同一个值   `page_load`：用于等待页面加载   `script`：用于等待脚本执行|\|此属性以字典方式返回三种超时时间。|
|`retry_times`|`int`|\|网络连接失败时的重试次数。默认为 3，可对其赋值。|
|`retry_interval`|`int`|\|网络连接失败时的重试等待间隔秒数。默认为 2，可对其赋值。|
|`load_mode`|`str`|`normal`：等待页面所有资源完成加载   `eager`：DOM加载完成即停止   `none`：页面完成连接即停止|页面加载策略|
|cookies和缓存信息|
|`cookies()`|`as_dict`: 是否以字典方式返回结果。为`True`时返回dict，且`all_info`参数无效；为`False`返回cookie组成的list   `all_domains`: 是否返回所有cookies，为`False`只返回当前url的   `all_info`: 返回的cookies是否包含所有信息，`False`时只包含name、value、domain信息|`dict`: `as_dict`为`True`时，返回字典格式cookies   `list`: `as_dict`为`False`时，返回cookies组成的列表|返回 cookies 信息。|
|`session_storage()`|`item`: 要获取的项目，为`None`则返回全部项目组成的字典|`dict`: `item`参数为`None`时返回所有项目   `str`: 指定`item`时返回该项目内容|获取`sessionStorage`信息，可获取全部或单个项。|
|`local_storage()`|`item`: 要获取的项目，为`None`则返回全部项目组成的字典|`dict`: `item`参数为`None`时返回所有项目   `str`: 指定`item`时返回该项目内容|获取`sessionStorage`信息，可获取全部或单个项。|获取`localStorage`信息，可获取全部或单个项|
|内嵌对象|
|` driver`|`Driver`|\|``返回当前页面对象使用的Driver对象。|

## 4. 页面交互

### 页面跳转

> `get()`

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`url`|`str`|必填|目标|url|
|`show_errmsg`|`bool`|False|连接出错时是否显示和抛出异常|
|`retry`|`int`|None|重试次数，为None时使用页面参数，默认3|
|`interval`|`float`|None|重试间隔（秒），为None时使用页面参数，默认2|
|`timeout`|`float`|None|加载超时时间（秒）|

|返回类型|说明|
|---|---|
|bool|是否连接成功|

> back()

浏览历史中后退若干步。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`steps`|int|1|后退步数|

> forward()

在浏览历史中前进若干步。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`steps`|int|1|后退步数|

> refresh()

刷新当前页面。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`ignore_cache`|`bool`|False|刷新时是否忽略缓存|

>  stop_loading()

此方法用于强制停止当前页面加载。

> set.blocked_urls()

设置忽略的连接。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`urls`|`str` `list` `tuple` `None`|必填|要忽略的url，可传入多个，可用'*'通配符，传入None时清空已设置的项|

```python
# 设置不加载css文件
page.set.blocked_urls('*.css')  
```

### 元素管理

> add_ele()

创建一个元素。可选择是否插入到DOM。

`html_or_info`传入元素完整html文本时，会插入到DOM。如`insert_to`参数为`None`，插入到body元素。

传入元素信息（格式：(`tag, {name: value}`)）时，如`insert_to`参数为`None`，不插入到 DOM。此时返回的元素需用js方式点击。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`html_or_info`|`str` `Tuple[str, dict]`|必填|新元素的html文本或信息；为tuple可新建不加入到DOM的元素|
|`insert_to`|`str` `ChromiumElement` `Tuple[str, str]`|None|插入到哪个元素中，可接收元素对象和定位符；如为`None`，`html_or_info`是`str`时添加到body，否则不添加到DOM|
|`before`|`str` `ChromiumElement` `Tuple[str, str]`|None|在哪个子节点前面插入，可接收对象和定位符，为None插入到父元素末尾|

|返回类型|说明|
|---|---|
|`ChromiumElement`|新建的元素对象|

```python
from DrissionPage import ChromiumPage

# 添加一个可见元素
page = ChromiumPage()
page.get('https://www.baidu.com')
html = '<a href="https://DrissionPage.cn" target="blank">DrissionPage </a> '
ele = page.add_ele(html, '#s-top-left', '新闻')  # 插入到导航栏
ele.click()

# 添加一个不可见元素
page = ChromiumPage()
info = ('a', {'innerText': 'DrissionPage', 'href': 'https://DrissionPage.cn', 'target': 'blank'})
ele = page.add_ele(info)
ele.click('js')  # 需用js点击
```

> remove_ele()

此方法用于从页面上删除一个元素。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`loc_or_ele`|`str` `Tuple[str, str]` `ChromiumElement`|必填|要删除的元素，可以是元素或定位符|

```python
# 删除一个已获得的元素
ele = page('tag:a')
page.remove_ele(ele)

# 删除用定位符找到的元素
page.remove_ele('tag:a')
```

### 执行脚本或命令

> run_js()

执行 js 脚本。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`script`|`str`|必填|js脚本文本或脚本文件路径|
|`*args`|-|无|传入的参数，按顺序在js文本中对应arguments[0]、arguments[1]...|
|`as_expr`|`bool`|False|是否作为表达式运行，为True时args参数无效|
|`timetout`|`float`|None|js 超时时间，为None则使用页面timeouts.script设置|

|返回类型|说明|
|---|---|
|Any|脚本执行结果|

> run_js_loaded()

此方法用于运行 js 脚本，执行前等待页面加载完毕。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`script`|`str`|必填|js脚本文本或脚本文件路径|
|`*args`|-|无|传入的参数，按顺序在js文本中对应arguments[0]、arguments[1]...|
|`as_expr`|`bool`|False|是否作为表达式运行，为True时args参数无效|
|`timetout`|`float`|None|js 超时时间，为None则使用页面timeouts.script设置|

|返回类型|说明|
|---|---|
|Any|脚本执行结果|

> run_async_js()

以异步方式执行 js 代码。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`script`|`str`|必填|js脚本文本或脚本文件路径|
|`*args`|-|无|传入的参数，按顺序在js文本中对应arguments[0]、arguments[1]...|
|`as_expr`|`bool`|False|是否作为表达式运行，为True时args参数无效|

> run_cdp()

执行 Chrome DevTools Protocol 语句。

cdp 用法详见[Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`cmd`|`str`|必填|协议项目|
|`**cmd_args`|-|无|项目参数|

|返回类型|说明|
|---|---|
|dict|执行返回的结果|

> run_cdp_loaded()

此方法用于执行 Chrome DevTools Protocol 语句，执行前先确保页面加载完毕。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`cmd`|`str`|必填|协议项目|
|`**cmd_args`|-|无|项目参数|

|返回类型|说明|
|---|---|
|dict|执行返回的结果|

### cookies及缓存

> set.cookies()

此方法用于设置 cookie。可设置一个或多个。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`cookies`|`CookieJar` `list` `tuple` `str` `dict`|必填|cookies 信息|

返回：`None`

> set.cookies.clear()

清除所有 cookie。

参数： 无

返回：`None`

> set.cookies.remove()

删除一个 cookie。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`name`|`str`|必填|cookie的name字段|
|`name`|`str`|`None`|cookies的url字段|
|`name`|`str`|`None`|cookies的domain字段|
|`name`|`str`|`None`|cookies的path字段|

> set.session_storage()

此方法用于设置或删除某项sessionStorage信息。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`item`|`str`|必填|要设置的项|
|`value`|`str` `False`|必填|为`False`时，删除该项|

> set.local_storage()

用于设置或删除某项 localStorage 信息。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`item`|`str`|必填|要设置的项|
|`value`|`str` `False`|必填|为`False`时，删除该项|

> clear_cache()

用于清除缓存，可选择要清除的项。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`session_storage`|`bool`|`True`|是否清除 sessionstorage|
|`local_storage`|`bool`|`True`|是否清除 localStorage|
|`cache`|`bool`|`True`|是否清除 cache|
|`cache`|`bool`|`True`|是否清除 cookies|

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

### 滚动设置

页面滚动有两种方式，一种是滚动时直接跳到目标位置，第二种是平滑滚动，需要一定时间。后者滚动时间难以确定，容易导致程序不稳定，点击不准确的问题。

|函数|功能|
|---|---|
|`set.scroll.smooth()`|是否开启平滑滚动。建议关闭|
|`set.scroll.wait_complete()`|设置滚动后是否等待滚动结束|

### 弹出消息处理

> handle_alert()

此方法用于处理提示框。
它能够设置等待时间，等待提示框出现才进行处理，若超时没等到提示框，返回`False`。
也可只获取提示框文本而不处理提示框。 还可以处理下一个出现的提示框，这在处理离开页面时触发的弹窗非常有用。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`accept`|`bool` `None`|`True`|`True`表示确认，`False`表示取消，`None`不会按按钮但依然返回文本值|
|`send`|`str`|`None`|处理prompt提示框时可输入文本|
|`timeout`|`float`|`None`|等待提示框出现的超时时间，为`None`时使用页面整体超时时间|
|`next_one`|`bool`|`False`|是否处理下一个出现的弹窗，为`True`时timeout参数无效|

|`返回类型`|说明|
|`str`|提示框内容文本|
|`False`|未等到提示框则返回False|

```python
# 确认提示框并获取提示框文本
txt = page.handle_alert()

# 点击取消
page.handle_alert(accept=False)

# 给 prompt 提示框输入文本并点击确定
page.handle_alert(accept=True, send='some text')

# 不处理提示框，只获取提示框文本
txt = page.handle_alert(accept=None)
```

> set.auto_handle_alert()

设置自动处理该tab的提示框，使提示框不会弹窗而直接被处理掉

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`on_off`|`bool`|`True`|开或关|
|`accept`|`bool`|`True`|确定还是取消|

> set.auto_handle_alert()

用于指定是否全局设置自动处理

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`on_off`|`bool`|`True`|开或关|
|`accept`|`bool`|`True`|确定还是取消|
|`all_tabs`|`bool`|`False`|是否为全局设置|

### 关闭及重连

|函数|功能|
|---|---|
|`disconnect()`|页面对象断开与页面的连接，但不关闭标签页|
|`reconnect`|关闭与页面连接，然后重建一个新连接|
|`quit()`|关闭浏览器|

## 5. 查找元素

见下方[查找元素](#查找元素)章节

## 6. 获取元素信息

### ⭐常用属性表

|属性或方法|说明|
|---|---|
|`html`|此属性返回元素的outerHTML文本|
|`inner_html`|此属性返回元素的innerHTML文本|
|`tag`|此属性返回元素的标签名|
|`text`|此属性返回元素内所有文本组合成的字符串|
|`raw_text`|此属性返回元素内原始文本|
|`texts()`|此方法返回元素内所有直接子节点的文本，包括元素和文本节点|
|`comments`|此属性以列表形式返回元素内的注释|
|`attrs`|此属性以字典形式返回元素所有属性及值|
|`attr()`|此方法返回元素某个属性值|
|`link`|此方法返回元素的`href`属性或`src`属性|
|`page`|此属性返回元素所在的总控页面对象|
|`xpath`|此属性返回当前元素在页面中xpath的绝对路径|
|`css_path`|此属性返回当前元素在页面中css selector的绝对路径|

### 大小和位置

|属性或方法|说明|
|---|---|
|`rect.size`|以元组形式返回元素的大小|
|`rect.location`|以元组形式返回元素左上角在整个页面中的坐标|
|`rect.midpoint`|以元组形式返回元素中点在整个页面中的坐标|
|⭐`rect.click_point`|以元组形式返回元素点击点在整个页面中的坐标|
|`rect.viewport_location`|以元组形式返回元素左上角在当前视口中的坐标|
|`rect.viewport_midpoint`|以元组形式返回元素中点在当前视口中的坐标|
|`rect.viewport_click_point`|以元组形式返回元素点击点在当前视口中的坐标|
|`rect.screen_location`|以元组形式返回元素左上角在屏幕中的坐标|
|`rect.screen_midpoint`|以元组形式返回元素中点在屏幕中的坐标|
|⭐`rect.screen_click_point`|以元组形式返回元素点击点在屏幕中的坐标|
|`rect.screen_click_point`|以列表形式返回元素四个角在页面中的坐标，顺序：左上、右上、右下、左下|
|`rect.viewport_corners`|此属性以列表形式返回元素四个角在视口中的坐标，顺序：左上、右上、右下、左下|
|`rect.viewport_rect`|以列表形式返回元素四个角在视口中的坐标，顺序：左上、右上、右下、左下|

### ⭐属性和内容

> pseudo.before/pseudo.after

文本形式返回当前元素的`::before`/`::after`伪元素内容

> style()

返回元素css样式属性值，可获取伪元素的属性

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`style`|`str`|必填|样式名称|
|`pseudo_ele`|`str`|''|伪元素名称（如有）|

|返回类型|说明|
|---|---|
|`str`|样式属性值|

```python
# 获取 css 属性的 color 值
prop = ele.style('color')

# 获取 after 伪元素的内容
prop = ele.style('content', 'after')
```

> property()

返回`property`属性值

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`name`|`str`|必填|属性名称|

|返回类型|说明|
|---|---|
|`str`|属性值|

> shadow_root

返回元素内的`shadow-root`对象，没有的返回`None`

### 状态信息

> ⭐states.is_in_viewport

元素是否在视口中，以元素可以接受点击的点为判断

> ⭐states.is_whole_in_viewport

元素是否整个在视口中

> ❓states.is_alive

当前元素是否仍可用, 用于判断d模式下是否因页面刷新而导致元素失效

> ❓states.is_enabled

返回元素是否可用

> states.is_checked

表单单选或多选元素是否选中

> states.is_selected

`<select>`元素中的项是否选中

> states.is_displayed

返回元素是否可见

> states.is_covered

元素是否被其它元素覆盖。如被覆盖，返回覆盖元素的 id，否则返回False

> states.is_clickable

回元素是否可被模拟点击，从是否有大小、是否可用、是否显示、是否响应点击判断，不判断是否被**遮挡**

> states.has_rect

元素是否拥有大小和位置信息，有则返回四个角在页面上的坐标组成的列表，没有则返回`False`

### ⭐保存元素

> src()

返回元素`src`属性所使用的资源。base64 的可转为`bytes`返回，其它的以`str`返回。无资源的返回`None`。

例如，可获取页面上图片字节数据，用于识别内容，或保存到文件。`<script>`标签也可获取js文本。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`timeout`|`float`|None|等待资源加载超时时间，为None时使用元素所在页面timeout属性|
|`base64_to_bytes`|`bool`|True|为True时，如果是 base64 数据，转换为bytes格式|

|返回类型|说明|
|---|---|
|`str`|资源字符串|
|`None`|无资源的返回None|

> ⭐save()

用于保存`src()`方法获取到的资源到文件

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`path`|`str` `Path`|None|文件保存路径，为None时保存到当前文件夹|
|`name`|`str`|None|文件名称，需包含后缀，为None时从资源 url 获取|
|`timeout`|`float`|None|等待资源加载超时时间，为None时使用元素所在页面timeout属性|
|`rename`|`bool`|True|遇到重名文件时是否自动重命名|

|返回类型|说明|
|---|---|
|`str`|保存路径|

## 7. 元素交互

### 点击元素

> click()和click.left()

左键点击元素。可选择模拟点击或js点击，**在模拟点击前，程序会先尝试把元素滚动到视口中**

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`by_js`|`bool`|False|指定点击行为方式。为None时，如不被遮挡，用模拟点击，否则用 js 点击，为True时直接用 js 点击；为False时强制模拟点击，被遮挡也会进行点击|
|`timeout`|`float`|1.5|模拟点击的超时时间，等待元素可见、可用、进入视口|
|`wait_stop`|`bool`|True|点击前是否等待元素停止运动|

|返回值|说明|
|---|---|
|`False`|`by_js`为`False`，且元素不可用、不可见时，返回`False`|
|`True`|除以上情况，其余情况都返回`True`|

> click.right()

右键单击元素

> click.middle()

中键单击元素

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`get_tab`|`bool`|True|是否返回新出现的Tab对象|

|返回值|说明|
|---|---|
|`ChromiumTab`|`get_tab`参数为`True`时，`ChromiumPage`返回的`Tab`对象|
|`WebPageTab`|`get_tab`参数为`True`时，`WebPage`返回的`Tab`对象|
|`None`|`get_tab`参数为`False`时|

> click.multi()

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`times`|`int`|2|点击次数|

返回：`None`

> click.at()

此方法用于带偏移量点击元素，偏移量相对于元素左上角坐标。不传入`offset_x`和`offset_y`时点击元素中间点。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`offset_x`|`float`|None|相对元素左上角坐标的 x 轴偏移量，向下向右为正|
|`offset_y`|`float`|None|相对元素左上角坐标的 y 轴偏移量，向下向右为正|
|`button`|`str`|'left'|要点击的键，传入'left'、'right'、'middle'、'back'、'forward'|
|`count`|`int`|1|点击次数|

> click.for_new_tab()

在预期点击后会出现新 tab 的时候，可用此方法点击，会等待并返回新 tab 对象

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`by_js`|`bool`|False|是否用 js 方式点击，逻辑与`click()`一致|

|返回类型|说明|
|---|---|
|`ChromiumTab`|使用`ChromiumPage`时返回|
|`WebPageTab`|使用`WebPage`时返回|

### 输入内容

> clear()

此方法用于清空元素文本，可选择模拟按键或 js 方式。

模拟按键方式会自动输入ctrl-a-del组合键来清除文本框，js 方式则直接把元素value属性设置为''。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`by_js`|`bool`|False|是否用 js 方式清空|

> input()

此方法用于向元素输入文本或组合键，也可用于输入文件路径到上传控件。可选择输入前是否清空元素。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`vals`|`Any`|False|文本值或按键组合，对文件上传控件时输入路径字符串或其组成的列表|
|`clear`|`bool`|False|输入前是否清空文本框|
|`by_js`|`bool`|False|是否用js方式输入，为`True`时不能输入组合键|

> [!NOTE]
> 有些文本框可以接收回车代替点击按钮，可以直接在文本末尾加上'\n'。   
> 会自动把非`str`数据转换为`str`。是否用js方式输入，为True时不能输入组合键

> 输入组合键

组合键或要传入特殊按键前，先要导入按键类`Keys`

```python
from DrissionPage.common import Keys
```

`Keys`内置了5个常用组合键，分别为`CTRL_A`、`CTRL_C`、`CTRL_X`、`CTRL_V`、`CTRL_Z`、`CTRL_Y`。

> focus()

用于使元素获取焦点

### 拖拽和悬停

> drag()

拖拽元素到相对于当前的一个新位置，可以设置速度

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`offset_x`|`int`|0|x轴偏移量，向下向右为正|
|`offset_y`|`int`|0|y轴偏移量，向下向右为正|
|`duration`|`float`|0.5|用时，单位秒，传入0即瞬间到达|

> drag_to()

拖拽元素到另一个元素上或一个坐标上

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`ele_or_loc`|`ChromiumElement` `Tuple[int, int]`|0|另一个元素对象或坐标元组|
|`duration`|`float`|0.5|用时，单位秒，传入0即瞬间到达|

> hover()

模拟鼠标悬停在元素上，可接受偏移量，偏移量相对于元素左上角坐标。不传入offset_x和offset_y值时悬停在元素中点

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`offset_x`|`int`|0|x轴偏移量，向下向右为正|
|`offset_y`|`int`|0|y轴偏移量，向下向右为正|

## 8. ⭐监听网络数据

### 等待并获取

> [!WARNING]
> 要先启动监听，再执行动作，listen.start()之前的数据包是获取不到的。

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://gitee.com/explore/all')  # 访问网址，这行产生的数据包不监听

page.listen.start('gitee.com/explore')  # 开始监听，指定获取包含该文本的数据包
for _ in range(5):
    page('@rel=next').click()  # 点击下一页
    res = page.listen.wait()  # 等待并获取一个数据包
    print(res.url)  # 打印数据包url
```

输出：

```term
https://gitee.com/explore/all?page=2   
https://gitee.com/explore/all?page=3   
https://gitee.com/explore/all?page=4   
https://gitee.com/explore/all?page=5  
https://gitee.com/explore/all?page=6  
```

### 实时获取

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.listen.start('gitee.com/explore')  # 开始监听，指定获取包含该文本的数据包
page.get('https://gitee.com/explore/all')  # 访问网址

i = 0
for packet in page.listen.steps():
    print(packet.url)  # 打印数据包url
    page('@rel=next').click()  # 点击下一页
    i += 1
    if i == 5:
        break
```

# 查找元素

## 1. 基本用法

### 查找元素方法

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

### 匹配模式

|模式|符号|说明|
|---|---|---|
|精确匹配|`=`|匹配完全符合的文本或属性|
|模糊匹配|`:`|匹配含有指定字符串的文本或属性|
|匹配开头|`^`|匹配开头为指定字符串的文本或属性|
|匹配结尾|`$`|匹配结尾为指定字符串的文本或属性|

### 查找语法

|匹配符|匹配方式|说明|
|---|---|---|
|`#`|id 匹配符|只在语句最前面且单独使用时生效|
|`.`|class 匹配符|只在语句最前面且单独使用时生效|
|`@`|单属性匹配符|只匹配一个属性。可单独使用，也可与tag配合使用。|
|`@@`|多属性与匹配符|匹配同时符合多个条件的元素时使用，每个条件前面添加@@作为开头。|
|`@\|`|多属性或匹配符|匹配符合多个条件中任一项的元素时使用，每个条件前面添加@|作为开头，可单独使用，也可与tag配合使用|
|`@!`|属性否定匹配符|用于否定某个条件，可与@@或@|混用，也可单独使用。|
|`text`|文本匹配符|没有任何匹配符时，默认匹配文本|
|`text`|文本匹配符|作为查找属性时使用的文本关键字，必须与@或@@配合使用|
|`tag`|类型匹配符|表示元素的标签，只在语句最前面且单独使用时生效|
|`css`|css selector匹配符|css selector 方式查找元素|
|`xpath`|xpath 匹配符|表示用 xpath 方式查找元素，`xpath:`与`xpath=`效果一致，没有xpath^和xpath$语法|
|loc 元组|selenium 的 loc 元组|查找方法能直接接收 selenium 原生定位元组进行查找，便于项目迁移|

```python
from DrissionPage.common import By

# selenium
shipfinderDriver.find_element(By.ID, 'ais-mmsi')

# loc 元组
loc1 = (By.ID, 'ais-mmsi')
ele = page.ele(loc1)
```

### 相对定位

> `parent()`: 此方法获取当前元素某一级父元素，可指定筛选条件或层数。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`level_or_loc`|``int``str``Tuple[str, str]`|1|第几级父元素，从1开始，或用定位符在父元素中进行筛选|
|`index`|`int`|1|当`level_or_loc`传入定位符，使用此参数选择第几个结果，从当前元素往上级数；当`level_or_loc`传入数字时，此参数无效|

|返回类型|说明|
|---|---|
|`SessionElement`|找到的元素对象|
|`NoneElement`|未获取到结果时返回`NoneElement`|

> `child()`: 此方法返回当前元素的一个直接子节点，可指定筛选条件和第几个。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str``Tuple[str, str]``int`|''|用于筛选节点的查询语法，为int类型时index参数无效|
|`index`|`int`|1|查询结果中的第几个，从1开始，可输入负数表示倒数|
|`timeout`|`float`|None|无实际作用|
|`ele_only`|`bool`|True|是否只查找元素，为`False`时把文本、注释节点也纳入查找范围|

|返回类型|说明|
|---|---|
|`SessionElement`|找到的元素对象|
|`str`|获取非元素节点时返回字符串|
|`NoneElement`|未获取到结果时返回`NoneElement`|

> `children()`: 此方法返回当前元素全部符合条件的直接子节点组成的列表，可用查询语法筛选。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str``Tuple[str, str]`|''|用于筛选节点的查询语法|
|`timeout`|`float`|None|无实际作用|
|`ele_only`|`bool`|True|是否只查找元素，为`False`时把文本、注释节点也纳入查找范围|

|返回类型|说明|
|---|---|
|`List[SessionElement, str]`|结果列表|

> `next()`: 此方法返回当前元素后面的某一个同级节点，可指定筛选条件和第几个。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str/Tuple[str, str]/int`|''|用于筛选节点的查询语法，为int类型时index参数无效|
|`index`|`int`|1|查询结果中的第几个，从1开始，可输入负数表示倒数|
|`timeout`|`float`|None|无实际作用|
|`ele_only`|`bool`|True|是否只查找元素，为`False`时把文本、注释节点也纳入查找范围|

|返回类型|说明|
|---|---|
|`SessionElement`|找到的元素对象|
|`str`|获取非元素节点时返回字符串|
|`NoneElement`|未获取到结果时返回`NoneElement`|

> `nexts()`: 此方法返回当前元素后面全部符合条件的同级节点组成的列表，可用查询语法筛选。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str``Tuple[str, str]`|''|用于筛选节点的查询语法|
|`timeout`|`float`|None|无实际作用|
|`ele_only`|`bool`|True|是否只查找元素，为`False`时把文本、注释节点也纳入查找范围|

|返回类型|说明|
|---|---|
|`List[SessionElement, str]`|结果列表|

> `prev()`: 此方法返回当前元素前面的某一个同级节点，可指定筛选条件和第几个。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str/Tuple[str, str]/int`|''|用于筛选节点的查询语法，为int类型时index参数无效|
|`index`|`int`|1|查询结果中的第几个，从1开始，可输入负数表示倒数|
|`timeout`|`float`|None|无实际作用|
|`ele_only`|`bool`|True|是否只查找元素，为`False`时把文本、注释节点也纳入查找范围|

|返回类型|说明|
|---|---|
|`SessionElement`|找到的元素对象|
|`str`|获取非元素节点时返回字符串|
|`NoneElement`|未获取到结果时返回`NoneElement`|

> `prevs()`: 此方法返回当前元素前面全部符合条件的同级节点组成的列表，可用查询语法筛选。

|参数名称|类型|默认值|说明|
|---|---|---|---|
|`locator`|`str``Tuple[str, str]`|''|用于筛选节点的查询语法|
|`timeout`|`float`|None|无实际作用|
|`ele_only`|`bool`|True|是否只查找元素，为`False`时把文本、注释节点也纳入查找范围|

|返回类型|说明|
|---|---|
|`List[SessionElement, str]`|结果列表|

> `after()`: 此方法返回当前元素后面的某一个节点，可指定筛选条件和第几个。查找范围不限同级节点，而是整个 DOM 文档。

> `afters()`: 此方法返回当前元素后面符合条件的全部节点组成的列表，可用查询语法筛选。查找范围不限同级节点，而是整个 DOM 文档。

参数、返回值与之前相同

> `before()`: 此方法返回当前元素前面的某一个符合条件的节点，可指定筛选条件和第几个。查找范围不限同级节点，而是整个 DOM 文档。

> `befores()`: 此方法返回当前元素前面全部符合条件的节点组成的列表，可用查询语法筛选。查找范围不限同级节点，而是整个 DOM 文档。

参数、返回值与之前相同
