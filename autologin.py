import requests, os, time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import traceback

url = "http://www.msftconnecttest.com/redirect"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

response = requests.get(url, headers=header)

print(response.url)

url = response.url

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": 'UserType="FzcXWJZWgmY="; PassWord="wHdEmYCnKwk="; province="FzcXWJZWgmY="; UserName="cVZWINbjH7vqlTU50Z9sGw=="; sto-id-20480=BAFBIFKMJABP; JSESSIONID=0B872941EF21368454A09192B4A03464',
    "Connection": "keep-alive",
    "Host": "wlan.jsyd139.com",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
}

response = requests.get(url, headers=header)  # 上传连接信息至学校服务器

# print(response.text)
tree = etree.HTML(response.content)
src = tree.xpath('//frame[@name="mainFrame"]/@src')[0]
print(src)

paramStr = src.split("paramStr=")[1]
print(paramStr)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

url = "http://wlan.jsyd139.com/style/default_szlan/index.jsp?paramStr=" + paramStr


def get_web_driver():
    # 在pycharm测试的时候可以将chromedriver放在项目目录中，使用路径来寻找
    # 当正式环境中，需要放在python.exe的路径中（如C:\ProgramData\Anaconda3\python.exe），通过系统环境变量来查找

    # chromedriver = "/usr/bin/chromedriver"
    # chromedriver = "D:\Project\Python\CampusNetLogin\chromedriver.exe"
    # s = Service(chromedriver=chromedriver)
    s = Service()
    # os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.implicitly_wait(10)  # 所有的操作都可以最长等待10s
    return driver

username = "xxxxxxx"  # 用户名
password = "xxxxxxx"  # 密码


try:
    driver = get_web_driver()
    driver.get(url)
    time.sleep(6)

    driver.find_element(by=By.XPATH, value='//*[@id="UserName"]').send_keys(username)
    driver.find_element(by=By.XPATH, value='//*[@id="PassWord"]').send_keys(password)

    driver.find_element(by=By.XPATH, value='//*[@id="loginbutton1"]').click()  # 点击"登录"按钮
    time.sleep(2)

    print("移动校园网登录成功")
except Exception as e:
    print(e)
    print(traceback.format_exc())
finally:
    driver.quit()



# url = "http://wlan.jsyd139.com/authServlet"  # 校园网认证网页的网址
#
# data = {
#     # paramStr是会改变的，最好能通过网页来获取最新的值
#     "paramStr": "DUXYMaQq9pOvJYZhsuOTUoTPFAOSuDl2UwnvuGEE71ruxe0Rj6S9hgetK5p641wNXNi9Hpm6pUFDbvob3dvahfuN6MDWQh58Tw1xQYnIPFa4u1oJ0WiQbKI8G86BMkb0kJXQvsVSy4l3DVTAB0jvHrhoJGYyLETvmkL4EI7V01qhttMui0kT56pvcrDWxAWS00DbTLYMmSW10l2IdpUkhk7LmqtSLP%2FDk9EuqthTlBYXZREgrUhyy%2B7a3H4NQm9xcvzuFITzbWbYwVtxr3aG0MvWdvTr7%2B0ZoWdMlp6YzOGnISbYzCOSK9aSJ5Xl2vz22dzGJW80lzwksNYZykxiJkzOTTFHyJtZ%2Brz6BCg29Tp0mQtRznFb0Hkd6%2FtD65gmzMOSxW5Kychean6%2BIrSuJvXl9%2F1OeLht",
#     "pwdType": 1,
#     "serviceType": 301,
#     "isCookie": True,
#     "cookieType": 2,
#     "UserName": "19852895156",
#     "PassWord": "147258",
#     "cookie": 2
# }
#
# header = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Content-Length": "568",
#     "Cookie": 'UserType="FzcXWJZWgmY="; PassWord="wHdEmYCnKwk="; province="FzcXWJZWgmY="; UserName="cVZWINbjH7vqlTU50Z9sGw=="; sto-id-20480=BGFBIFKMJABP; JSESSIONID=5C2786409F7FED0CAEAADA6BC867BD28',
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Host": "wlan.jsyd139.com",
#     "Origin": "http://wlan.jsyd139.com",
#     "Proxy-Connection": "keep-alive",
#     "Referer": "http://wlan.jsyd139.com/style/default_szlan/index.jsp?paramStr=" + "DUXYMaQq9pOvJYZhsuOTUoTPFAOSuDl2UwnvuGEE71ruxe0Rj6S9hgetK5p641wNXNi9Hpm6pUFDbvob3dvahfuN6MDWQh58Tw1xQYnIPFa4u1oJ0WiQbKI8G86BMkb0kJXQvsVSy4l3DVTAB0jvHrhoJGYyLETvmkL4EI7V01qhttMui0kT56pvcrDWxAWS00DbTLYMmSW10l2IdpUkhk7LmqtSLP%2FDk9EuqthTlBYXZREgrUhyy%2B7a3H4NQm9xcvzuFITzbWbYwVtxr3aG0MvWdvTr7%2B0ZoWdMlp6YzOGnISbYzCOSK9aSJ5Xl2vz22dzGJW80lzwksNYZykxiJkzOTTFHyJtZ%2Brz6BCg29Tp0mQtRznFb0Hkd6%2FtD65gmzMOSxW5Kychean6%2BIrSuJvXl9%2F1OeLht",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
# }
#
# response = requests.post(url, data, headers=header)  # 上传连接信息至学校服务器
#
# print(response.text)
#
# print(response.status_code)
