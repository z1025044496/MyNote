#

# 1. Scrapy框架简介

## 概述

> Scrapy 是用 Python 实现的一个为了爬取网站数据、提取结构性数据而编写的应用框架。
> Scrapy 常应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。
> 通常我们可以很简单的通过 Scrapy 框架实现一个爬虫，抓取指定网站的内容或图片。

## 组件

![](../../image/scrapy_架构图.png)

* **Scrapy Engine**(引擎): 负责Spider、ItemPipeline、Downloader、Scheduler中间的通讯，信号、数据传递等。
* **Scheduler**(调度器): 它负责接受引擎发送过来的Request请求，并按照一定的方式进行整理排列，入队，当引擎需要时，交还给引擎。
* **Downloader**（下载器）：负责下载Scrapy Engine(引擎)发送的所有Requests请求，并将其获取到的Responses交还给Scrapy Engine(引擎)，由引擎交给Spider来处理，
* **Spider**（爬虫）：它负责处理所有Responses,从中分析提取数据，获取Item字段需要的数据，并将需要跟进的URL提交给引擎，再次进入Scheduler(调度器).
* **Item Pipeline**(管道)：它负责处理Spider中获取到的Item，并进行进行后期处理（详细分析、过滤、存储等）的地方。
* **Downloader Middlewares**（下载中间件）：你可以当作是一个可以自定义扩展下载功能的组件。
* **Spider Middlewares**（Spider中间件）：你可以理解为是一个可以自定扩展和操作引擎和Spider中间通信的功能组件（比如进入Spider的Responses;和从Spider出去的Requests）

> [!WARNING]
> 只有当调度器中不存在任何request了，整个程序才会停止，（也就是说，对于下载失败的URL，Scrapy也会重新下载。）

## 数据处理流程
1. 引擎从调度器中取出一个链接(URL)用于接下来的抓取
2. 引擎把URL封装成一个请求(Request)传给下载器
3. 下载器把资源下载下来，并封装成应答包(Response)
4. 爬虫解析Response
5. 解析出实体（Item）,则交给实体管道进行进一步的处理
6. 解析出的是链接（URL）,则把URL交给调度器等待抓取

# 2. 创建项目

创建项目

```term
(python35) PS C:\Users\zhaohaifei5.HIK\Desktop\Scrapy测试>$ scrapy startproject test_01
(python35) PS C:\Users\zhaohaifei5.HIK\Desktop\Scrapy测试>$ scrapy genspider douban douban.com
```

# 3. 命令行工具

* 项目目录结构

```term
scrapy.cfg
myproject/
    __init__.py
    items.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
```

`scrapy.cfg`存放的目录被认为是项目的根目录。该文件中包含python模块名的字段定义了项目的设置。例如:

```ini
[settings]
default = myproject.settings
```

## 1. 创建项目

```shell
scrapy startproject myproject
```

该命令将会在*myproject*目录中创建一个*Scrapy*项目。

进入项目目录后，即可使用`scrapy`命令来管理和控制项目了。

## 2. 可用的工具命令

`scrapy <command> -h`: 获取关于*command*命令的详细内容

`scrapy -h`: 查看所有可用的命令

Scrapy提供了两种类型的命令。一种必须在Scrapy项目中运行(针对项目(Project-specific)的命令)，另外一种则不需要(全局命令)。全局命令在项目中运行时的表现可能会与在非项目中运行有些许差别(因为可能会使用项目的设定)。

*全局命令*:

* `startproject`
* `settings`
* `runspider`
* `shell`
* `fetch`
* `view`
* `version`

*项目命令*:

* `crawl`
* `check`
* `list`
* `edit`
* `parse`
* `genspider`
* `bench`

### `startproject`

* 语法: `scrapy startproject <project_name>`
* 是否需要项目: no

*在`project_name`文件夹下创建一个名为`project_name`的Scrapy项目。*

### `genspider`

* 语法: `scrapy genspider [-t template] <name> <domain>`
* 是否需要项目: yes

*在当前项目中创建spider。*

> [!NOTE]
> 这仅仅是创建spider的一种快捷方法。该方法可以使用提前定义好的模板来生成spider。也可以自己创建spider的源码文件。

### `crawl`

* 语法: `scrapy crawl <spider>`
* 是否需要项目: yes

*使用spider进行爬取。*

### `check`

* 语法: `scrapy check [-l] <spider>`
* 是否需要项目: yes

*运行contract检查。*

### `list`

* 语法: `scrapy list`
* 是否需要项目: yes

*列出当前项目中所有可用的spider。每行输出一个spider。*

### `edit`

* 语法: `scrapy edit <spider>`
* 是否需要项目: yes

*使用`EDITOR`中设定的编辑器编辑给定的spider*

> ![NOTE]
> 这个命令没啥用，自己找个编辑器敲代码就成

### `fetch`

* 语法: `scrapy fetch <url>``
* 是否需要项目: no

*使用Scrapy下载器(downloader)下载给定的URL，并将获取到的内容送到标准输出。*

> ![NOTE]
> 该命令以spider下载页面的方式获取页面。例如，如果spider有 USER_AGENT 属性修改了 User Agent，该命令将会使用该属性。
> 可以使用该命令来查看spider如何获取某个特定页面。
> 该命令如果非项目中运行则会使用默认Scrapy downloader设定。

### `view`

* 语法: `scrapy view <url>`
* 是否需要项目: no

*在浏览器中打开给定的URL，并以Scrapy spider获取到的形式展现。 有些时候spider获取到的页面和普通用户看到的并不相同。 因此该命令可以用来检查spider所获取到的页面，并确认这是您所期望的。*

### `shell`

* 语法: `scrapy shell [url]`
* 是否需要项目: no

*以给定的URL(如果给出)或者空(没有给出URL)启动Scrapy shell。 查看 Scrapy终端(Scrapy shell) 获取更多信息。*

### `parse`

* 语法: `scrapy parse <url> [options]`
* 是否需要项目: yes

*获取给定的URL并使用相应的spider分析处理。如果您提供 --callback 选项，则使用spider的该方法处理，否则使用`parse()`。*

*支持的选项*:

`--spider=SPIDER`: 跳过自动检测spider并强制使用特定的spider
`--a NAME=VALUE`: 设置spider的参数(可能被重复)
`--callback` or `-c`: spider中用于解析返回(response)的回调函数
`--pipelines`: 在pipeline中处理item
`--rules` or `-r`: 使用 CrawlSpider 规则来发现用来解析返回(response)的回调函数
`--noitems`: 不显示爬取到的item
`--nolinks`: 不显示提取到的链接
`--nocolour`: 避免使用pygments对输出着色
`--depth` or `-d`: 指定跟进链接请求的层次数(默认: 1)
`--verbose` or `-v`: 显示每个请求的详细信息

### `settings`

* 语法: `scrapy settings [options]`
* 是否需要项目: no

*获取Scrapy的设定, 在项目中，该命令将会输出当前项目的设定值，否则输出Scrapy默认设定。*

### `runspider`

* 语法: scrapy runspider <spider_file.py>
* 是否需要项目: no

*在未创建项目的情况下，运行一个编写在Python文件中的spider。*

### `version`

* 语法: `scrapy version [-v]`
* 是否需要项目: no

*输出Scrapy版本。配合 -v 运行时，该命令同时输出Python, Twisted以及平台的信息，方便bug提交。*

### `bench`

* 语法: `scrapy bench`
* 是否需要项目: no

*运行benchmark测试。[Benchmarking](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/benchmarking.html#benchmarking)*

# 4. spider

对spider来说，爬取的循环类似下文:

1. 以初始的URL初始化`Request`，并设置回调函数。 当该`request`下载完毕并返回时，将生成`response`，并作为参数传给该回调函数。   
spider中初始的request是通过调用 start_requests() 来获取的。 start_requests() 读取 start_urls 中的URL， 并以 parse 为回调函数生成 Request 。
2. 在回调函数内分析返回的(网页)内容，返回`Item`对象、`dict`、`Request`或者一个包括三者的可迭代容器。 返回的`Request`对象之后会经过Scrapy处理，下载相应的内容，并调用设置的callback函数(函数可相同)。
3. 在回调函数内，您可以使用 选择器(`Selectors`) (您也可以使用`BeautifulSoup`, `lxml`或者您想用的任何解析器) 来分析网页内容，并根据分析的数据生成`item`。
4. 最后，由`spider`返回的`item`将被存到数据库(由某些`Item Pipeline`处理)或使用`Feed exports`存入到文件中。

## 1. `scrapy.Spider`

> classscrapy.spiders.Spider

`scrapy.Spider`是最简单的spider。每个其他的spider必须继承自该类(包括Scrapy自带的其他spider以及您自己编写的spider)。`Spider`并没有提供什么特殊的功能。 其仅仅提供了 `start_requests()`的默认实现，读取并请求spider属性中的 `start_urls`, 并根据返回的结果(`resulting` `responses`)调用spider的`parse()`方法。

* `name`

定义spider名字的字符串(string)。spider的名字定义了Scrapy如何定位(并初始化)spider，所以其必须是唯一的。不过可以生成多个相同的spider实例(instance)，这没有任何限制。`name`是spider最重要的属性，而且是必须的。

* `allowed_domains`

可选。包含了spider允许爬取的域名列表。 当 `OffsiteMiddleware`启用时， 域名不在列表中的URL不会被跟进。

* `start_urls`

URL列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。 因此，第一个被获取到的页面的URL将是该列表之一。 后续的URL将会从获取到的数据中提取。

* `custom_settings`

该设置是一个dict.当启动spider时,该设置将会覆盖项目级的设置. 由于设置必须在初始化前被更新,所以该属性 必须定义为class属性.

* `crawler`

该属性在初始化class后,由类方法`from_crawler()`设置, 并且链接了本spider实例对应的`Crawler`对象.

`Crawler`包含了很多项目中的组件,作为单一的入口点 (例如插件,中间件,信号管理器等). 请查看[Crawler API](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/api.html#topics-api-crawler)来了解更多.

* `settings`

运行此spider的配置, 这是一个setting实例，请参阅[Settings](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/settings.html#topics-settings)以获取有关此主题的详细介绍。

* `logger`

以`Spider`的名字创建的Python日志。您可以使用它来通过它发送日志消息，如从[Logging from Spiders](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/spiders.html)中所述。

* `from_crawler(crawler, *args, **kwargs)`

Scrapy用于创建Spider的类方法。

* `start_requests()`

该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个`Request`。

当spider启动爬取并且未制定URL时，该方法被调用。 当指定了URL时，`make_requests_from_url()`将被调用来创建`Request`对象。 该方法仅仅会被Scrapy调用一次，因此您可以将其实现为生成器。

该方法的默认实现是使用`start_urls`的url生成Request。

如果您想要修改最初爬取某个网站的`Request`对象，您可以重写该方法。

* `make_requests_from_url(url)`

该方法接受一个URL并返回用于爬取的`Request`对象。 该方法在初始化request时被`start_requests()`调用，也被用于转化url为request。

默认未被重写的情况下，该方法返回的`Request`对象中，`parse()`作为回调函数，`dont_filter`参数也被设置为开启。 (详情参见[Request](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/request-response.html#scrapy.http.Request)).

* `parse(response)`

当`response`没有指定回调函数时，该方法是Scrapy处理下载的`response`的默认方法。

* `log(message[, level, component])`

使用`scrapy.log.msg()`方法记录日志。 log中自动带上该spider的`name`属性。 更多数据请参见[Logging](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/logging.html#topics-logging)。 封装了通过Spiders的`logger`来发送log消息的方法，并且保持了向后兼容性。

* `closed(reason)`

当spider关闭时，该函数被调用。 该方法提供了一个替代调用`signals.connect()`来监听`spider_closed`信号的快捷方式。

## 2. 通用spider

### ① CrawlSpider

爬取一般网站常用的spider。其定义了一些规则(rule)来提供跟进link的方便的机制。

* `rules`

包含一个(或多个)`Rule`对象的集合(list)。 每个`Rule`对爬取网站的动作定义了特定表现。`Rule`对象在下边会介绍。如果多个`Rule`匹配了相同的链接，则根据他们在本属性中被定义的顺序，第一个会被使用。

该spider也提供了一个可重写的方法:

* `parse_start_url(response)`

当`start_url`的请求返回时，该方法被调用。该方法分析最初的返回值并必须返回一个`Item`对象或者一个`Request`对象或者一个可迭代的包含二者对象。

> 爬取规则

```python
classscrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)
```

`link_extractor`是一个[Link Extractor](https://scrapy-chs.readthedocs.io/zh-cn/1.0/topics/link-extractors.html#topics-link-extractors)对象。 其定义了如何从爬取到的页面提取链接。

`callback`是一个`callable`或`string`(该spider中同名的函数将会被调用)。 从`link_extractor`中每获取到链接时将会调用该函数。该回调函数接受一个`response`作为其第一个参数， 并返回一个包含`Item`以及(或) `Request`对象(或者这两者的子类)的列表(list)。

> [!WARNING]
> 当编写爬虫规则时，请避免使用`parse`作为回调函数。 由于`CrawlSpider`使用`parse`方法来实现其逻辑，如果您覆盖了`parse`方法，`crawl spider`将会运行失败。

`cb_kwargs`包含传递给回调函数的参数(keyword argument)的字典。

`follow`是一个布尔(boolean)值，指定了根据该规则从`response`提取的链接是否需要跟进。如果`callback`为None，`follow`默认设置为`True`，否则默认为`False`。

`process_links`是一个`callable`或`string`(该spider中同名的函数将会被调用)。 从`link_extractor`中获取到链接列表时将会调用该函数。该方法主要用来过滤。

`process_request`是一个`callable`或`string`(该spider中同名的函数将会被调用)。 该规则提取到每个`request`时都会调用该函数。该函数必须返回一个`request`或者`None`。 (用来过滤`request`)

> 例子

```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
```

# 5. 下载中间件

下载器中间件是介于`Scrapy`的`request/response`处理的钩子框架。是用于全局修改`Scrapy request/response`的一个轻量、底层的系统。

## 1. 激活下载中间件

```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
}
```

`DOWNLOADER_MIDDLEWARES`设置会与Scrapy定义的`DOWNLOADER_MIDDLEWARES_BASE`设置合并(但不是覆盖)， 而后根据顺序(order)进行排序，最后得到启用中间件的有序列表: 第一个中间件是最靠近引擎的，最后一个中间件是最靠近下载器的。

将其复制为`None`可以将`DOWNLOADER_MIDDLEWARES_BASE`中的中间件关闭，例如：

```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
```

上述代码关闭了user-agent中间件

## 2. 下载中间件函数说明

* `process_request(request, spider)`

当每个`request`通过下载中间件时，该方法被调用。

*返回值*:

`None`: Scrapy将继续处理该request，执行其他的中间件的相应方法，直到合适的下载器处理函数(download handler)被调用， 该request被执行(其response被下载)。

`Response`: Scrapy将不会调用任何其他的`process_request()`或`process_exception()`方法，或相应地下载函数.

`Request`: Scrapy停止调用`process_request()`方法并重新调度返回的request。

`IgnoreRequest`: 安装的下载中间件的`process_exception()`方法会被调用。如果没有任何一个方法处理该异常，则request的`errback(Request.errback)`方法会被调用。如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。


*参数*:

`request`(`Request`对象): 处理的request

`spider`(`Spider`对象): 该request对应的spider

* process_response(request, response, spider)

*返回值*:

`Response`: 可以与传入的response相同，也可以是全新的对象；该response会被在链中的其他中间件的`process_response()`方法处理。

`Request`: 则中间件链停止， 返回的request会被重新调度下载。

`IgnoreRequest`: 调用`request`的`errback(Request.errback)`。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。

*参数*:

`request`(`Request`对象): 处理的request

`response`(`Response`对象) – 被处理的response

`spider`(`Spider`对象): 该request对应的spider

* `process_exception(request, exception, spider)`

当下载处理器(download handler)或`process_request()`(下载中间件)抛出异常(包括`IgnoreRequest`异常)时， Scrapy调用`process_exception()`。

*返回值*

`None`: Scrapy将会继续处理该异常，接着调用已安装的其他中间件的`process_exception()`方法，直到所有中间件都被调用完毕，之后则调用默认的异常处理。

`Response`对象: 调用已安装的`process_response()`方法，将不会调用任何其他中间件的`process_exception()`方法。

`Request`对象: 返回的request将会被重新调用下载，将不会调用任何其他中间件的`process_exception()`方法。

*参数*

`request`(是`Request`对象) – 产生异常的request

`exception`(`Exception`对象) – 抛出的异常

`spider`(`Spider`对象) – request对应的spider

# 重试

