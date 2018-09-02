from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time


"""
1.单个节点：browser.find_element_by_
多种方式，定位网页元素
"""
# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input1=browser.find_element_by_id('q')
# input2=browser.find_element_by_css_selector('#q')
# input3=browser.find_element_by_xpath('//*[@id="q"]')
#
# input1_1=browser.find_element(By.ID,'q')#相当于以上的通用版函数
# print(input1,input1_1,input2,input3)
# browser.close()


"""
2.多个节点：browser.find_elements

"""
# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input4=browser.find_elements_by_xpath('//ul[@class="service-bd"]//li')
# print(input4)
# browser.close()

"""
3.交互式操作
browser.send_keys()输入文字
browser.clear()清空输入框
button=browser.fine_element_by_class_name()定位点击
button.click()点击操作
"""
# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input=browser.find_element_by_id('q')
# input.send_keys('htc')
# time.sleep(2)
# input.clear()
# input.send_keys('dell')
# button=browser.find_element_by_xpath('//button[@class="btn-search tb-bg"]')
# button1=browser.find_element_by_class_name('btn-search tb-bg')#等价于上一个语句，直接用类名来定位
# button.click()
# browser.close()

"""
4.动作链
鼠标拖拽，键盘按键等操作
"""
# browser=webdriver.Chrome()
# browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
# browser.switch_to.frame('iframeResult')#我们要将browser切换到这个框架页面中去!!!输入值在源码中找【iframe是网页中的一个元素，和div，a，ima，什么的差不多】
# source=browser.find_element_by_id('draggable')
# target=browser.find_element_by_id('droppable')
# actions=ActionChains(browser)
# actions.drag_and_drop(source,target)
# actions.perform()
# browser.close()
"""
5.执行javascript
有些操作，selenium没有提供api，但是能够模拟操作
我们模拟JavaScript的操作
"""
# browser=webdriver.Chrome()
# browser.get('http://zhihu.com/explore')
# browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')#执行JavaScript的语句
# browser.execute_script('alert("To Bottom")')

"""
6.获取节点信息
"""
#获取属性
# browser=webdriver.Chrome()
# browser.get('http://zhihu.com/explore')
# logo=browser.find_element_by_id('zh-top-link-logo')
# print(logo)
# print(logo.get_attribute('class'))

#获取文本值，相当于xpath的text（）
# browser=webdriver.Chrome()
# browser.get('http://zhihu.com/explore')
# input=browser.find_element_by_id('zu-top-add-question')
# print(input.text)


#获取id，位置，标签名，大小
# browser=webdriver.Chrome()
# browser.get('http://zhihu.com/explore')
# input=browser.find_element_by_class_name('zu-top-add-question')
# print(input.id,input.tag_name,input.location,input.size)#是指selenium的webelement的节点id，非网页元素的id
# print(input.get_attribute('id'))#这个才是网页元素的id

"""
7.获取节点信息
iframe网页中的子页面
"""
# browser=webdriver.Chrome()
# browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
# browser.switch_to.frame('iframeResult')
# try:
#     input=browser.find_element_by_class_name('logo')
# except NoSuchElementException:
#     print('no logo')
# browser.switch_to.parent_frame()
# input=browser.find_element_by_class_name('logo')#navbar-header logo前面的navbar-header不作为class的名？？？
# print(input)
# print(input.text,input.location)

"""
8.延时等待【网页加载ajax的请求】
  a。隐式等待
  b  显示等待
"""
#隐式等等
# browser=webdriver.Chrome()
# browser.implicitly_wait(10)#隐式等待，在查找节点没有立即出现时，在等待10
# browser.get('http://zhihu.com/explore')#get（）方法会在网页框架加载完成后执行
# input=browser.find_element_by_class_name('zu-top-add-question')
# print(input)

#显示等待:指定查找节点，设置最大等待时间

# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# wait=WebDriverWait(browser,10)
# input=wait.until(EC.presence_of_element_located((By.ID,'q')))
# button=wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="search-button"]')))#可点击的
# print(input,button)


"""
9.前进后退 当然在一个页面
back
forward
"""
# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# browser.get('https://zhihu.com')
# browser.get('https://www.baidu.com')
# browser.back()
# time.sleep(2)
# browser.forward()

"""
9.cookies
"""
# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# print(browser.get_cookies())#获得cookies
# browser.add_cookie({'name':'jess','domain':'www.taobao.com','value':'jess'})#添加，保证domain和网址的url一致
# print(browser.get_cookies())
# browser.delete_all_cookies()#清空cookie
# print(browser.get_cookies())#清空后，就没有了


"""
10.选项卡管理：标签页管理
"""
# browser=webdriver.Chrome()
# browser.get('https://www.taobao.com')
# browser.execute_script('window.open()')#javascript语句
# print(browser.window_handles)
# browser.switch_to.window(browser.window_handles[1])
# browser.get('https://www.baidu.com')
# browser.switch_to.window(browser.window_handles[0])


"""
11.异常处理
try：
except
捕获异常：就是把各种异常conn.exceptions 放在except中
"""
browser=webdriver.Chrome()
browser.get('https://www.taobao.com')
try:
   input=browser.find_element_by_id('q')
except NoSuchElementException:
    print('no such nodes')
try:
    browser.get('https://www.google.com')
except TimeoutException:
    print('time out')
finally:
    browser.get('https://www.baidu.com')

