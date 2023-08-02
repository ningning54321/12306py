# !/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from datetime import datetime
from datetime import time as time0
import time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

#=================配置选项开始====================#
seatOption = os.environ['SEAT_OPTION']
trainNo = os.environ['TRAIN_NO']
startStation = os.environ['START_STATION']
endStation = os.environ['END_STATION']
leaveDate = os.environ['LEAVE_DATE']
runTime= os.environ['RUNTIME']
autoConfirm = os.environ['AUTO_CONFIRM']
uname = os.environ['NAME']
passwd = os.environ['PASS']
passengers = os.environ['PASSENGERS']
delay = os.environ['DELAY']
#=================配置选项结束====================#

LOGIN_URL = 'https://kyfw.12306.cn/otn/resources/login.html'


# 创建一个参数对象，用来控制 浏览器以无界面模式打开
bro_options = Options()
bro_options.add_experimental_option('excludeSwitches', ['enable-automation'])
bro_options.add_experimental_option("detach", True)
# 禁用启用Blink运行时的功能
bro_options.add_argument('--disable-blink-features=AutomationControlled')
bro = webdriver.Chrome(options=bro_options)
bro.get(LOGIN_URL)

# 解决特征识别, 用来解决滑块出错，验证问题
script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
bro.execute_script(script)

# 根据id获取用户账号输入框、密码输入框，并输入账号密码
try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.ID, 'J-login')))
except TimeoutException:
    print("等待显示用户-密码,超时")
bro.find_element(By.ID, 'J-userName').send_keys(uname)
bro.find_element(By.ID, 'J-password').send_keys(passwd)

# 根据id获取登录按钮并点击
bro.find_element(By.ID, 'J-login').click()

# 处理滑块验证
try:
    WebDriverWait(bro, 4).until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
    span = bro.find_element(By.ID, 'nc_1_n1z')

    # 定义动作链，点击并拖拽
    aco = ActionChains(bro)
    # 点击并长按
    aco.click_and_hold(span)
    # perform()立即执行动作链操作

    for i in range(10):
        aco.move_by_offset(36,0).perform()
        time.sleep(0.2)
        
    # 释放动作链
    aco.release()
    time.sleep(2)

    # 点击登录后的弹窗 确定 按钮
    bro.find_element(by='class name', value='ok').click()
except TimeoutException:
    print("等待滑块,超时")
except:
    pass

# 登录成功，准备转到车票查询页面
while True:
    time.sleep(10)#
    try:
        WebDriverWait(bro, 2).until(EC.presence_of_element_located((By.ID, 'link_for_ticket')))
        break
    except TimeoutException:
        print("等待显示订票按钮,超时")
bro.find_element(by='id', value='link_for_ticket').click()

try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.ID, 'fromStationText')))
except TimeoutException:
    print("等待显示始发站,超时")

# 配置始发站，终点站和出发日期
fs = bro.find_element(By.ID, 'fromStationText')
fs.click()
fs.send_keys(startStation)
bro.find_element(By.XPATH, f"//div[@id='search_div']/div[@id='form_cities']/div[@id='panel_cities']/div/span[text()='{startStation}']").click()

es = bro.find_element(By.ID, 'toStationText')
es.click()
es.send_keys(endStation)
bro.find_element(By.XPATH, f"//div[@id='search_div']/div[@id='form_cities']/div[@id='panel_cities']/div/span[text()='{endStation}']").click()

td = bro.find_element(By.ID, "train_date")
td.clear()
td.send_keys(leaveDate)

time.sleep(2)
query = bro.find_element(By.ID, 'query_ticket')
query.click()
try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.XPATH, f'//ul[@id="from_station_ul"]/li/input[@value="{startStation}"]')))
except TimeoutException:
    print("等待显示过滤,超时")

bro.find_element(By.XPATH, f'//ul[@id="from_station_ul"]/li/input[@value="{startStation}"]').click()
bro.find_element(By.XPATH, f'//ul[@id="to_station_ul"]/li/input[@value="{endStation}"]').click()

# 找到列车对应的一行
try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.XPATH, f'//a[text()="{trainNo}"]')))
except TimeoutException:
    print("等待显示预定按钮1,超时")

sa = bro.find_element(By.XPATH, f'//a[text()="{trainNo}"]')
# 找到代表这一行的父元素
tr = sa.find_element(By.XPATH, "../../../../..")
trId = tr.get_attribute("id")

# 在查询页面等待, 到出票时间再次点击查询按钮
startTime = time0(*(map(int, runTime.split(':'))))
i = 0
while startTime > datetime.today().time():
    time.sleep(0.5)#
    i += 1
    # 保活
    if i == 120:
        query.click()
        i = 0
query.click()

try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.XPATH, f'//tr[@id="{trId}"]/td/a')))
except TimeoutException:
    print("等待显示预定按钮,超时")

bro.find_element(By.XPATH, f'//tr[@id="{trId}"]/td/a').click()

# 跳转到添加乘客页面
try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.ID, 'normalPassenger_0')))
except TimeoutException:
    print("等待显示乘客,超时")

for idx in passengers:
    bro.find_element(By.XPATH, f'//input[@id="normalPassenger_{idx}"]').click()

try:
    for i in range(len(passengers)):
        Select(bro.find_element(By.ID, f'seatType_{i+1}')).select_by_value(seatOption)
    #Select(bro.find_element(By.ID, f'seatType_4')).select_by_value("1")
except:
    print("抱歉,抢票失败")

# 提交订单
bro.find_element(By.ID, "submitOrder_id").click()

# 等待确认页面
try:
    WebDriverWait(bro, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a#qr_submit_id.btn92s')))
except TimeoutException:
    print("等待显示乘客确认,超时")

#bro.find_element(By.ID, 'back_edit_id').click()
if autoConfirm:
    bro.find_element(By.ID, 'qr_submit_id').click()
    print("订单已经提交,请尽快完成付款")


exit(0)

#time.sleep(50)
#bro.quit()
