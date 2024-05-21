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

### 元素管理

### 执行脚本或命令

### cookies及缓存

### 运行参数设置

### 窗口管理

### 页面滚动

### 滚动设置

### 弹出消息处理

### 关闭及重连

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
