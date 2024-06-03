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
    from DrissionPage import ChromiumPage

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