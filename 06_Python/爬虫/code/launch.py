# 接管浏览器

from DrissionPage import ChromiumPage
from DrissionPage import ChromiumPage, ChromiumOptions

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 接管浏览器
# co = ChromiumOptions().set_local_port(9222)
# co.set_browser_path(r'C:/Program Files/Google/Chrome/Application/chrome.exe')
# page = ChromiumPage(addr_or_opts=co)

# 启动多个浏览器
# for i in range(6222, 6225):
#     page = ChromiumPage(i)

# selenium

page = ChromiumPage()