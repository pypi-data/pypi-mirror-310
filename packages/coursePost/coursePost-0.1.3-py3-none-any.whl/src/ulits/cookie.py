import time

import pymysql
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By


def getCookie():
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    # 启动浏览器
    driver = webdriver.Firefox(options=options)  # 如果你使用的是Firefox浏览器
    # 打开登录页面
    driver.get(
        "https://authserver.hniu.cn/authserver/login?service=https%3A%2F%2Fehall.hniu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.hniu.cn%2Fnew%2Findex.html%3Fbrowser%3Dno")

    # 找到用户名输入框并输入账户
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys("202315310305")

    # 找到密码输入框并输入密码
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys("20050703zrZR")

    # 找到登录按钮并点击
    login_button = driver.find_element(By.CLASS_NAME, 'auth_login_btn')
    login_button.click()

    system_button = driver.find_elements(By.CLASS_NAME, "widget-recommend-item")
    system_button[0].click()

    going_button = driver.find_element(By.ID, "ampDetailEnter")
    going_button.click()

    # 获取登录后的cookie
    time.sleep(10)
    search_window = driver.window_handles
    driver.switch_to.window(search_window[1])
    cookies = driver.get_cookies()
    resultMap = {
        'bzb_jsxsd': '',
        'sdp_app_session-443': '',
        'sdp_app_session-legacy-443': '',
    }
    for c in cookies:
        key = c.get('name')
        if key in resultMap:
            resultMap[key] = c.get('value')
    driver.quit()
    # logger.info("result:{}", result)
    cookie = ''
    for k, v in resultMap.items():
        cookie += f'{k}={v};'
    logger.info("cookie:{}", cookie)
    saveCookie(cookie)
    return cookie


def getCookieForServer():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    # 打开登录页面
    driver.get(
        "https://authserver.hniu.cn/authserver/login?service=https%3A%2F%2Fehall.hniu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.hniu.cn%2Fnew%2Findex.html%3Fbrowser%3Dno")
    time.sleep(3)
    # 找到用户名输入框并输入账户
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys("202315310305")

    # 找到密码输入框并输入密码
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys("20050703zrZR")

    # 找到登录按钮并点击
    login_button = driver.find_element(By.CLASS_NAME, 'auth_login_btn')
    login_button.click()

    time.sleep(10)
    system_button = driver.find_elements(By.CLASS_NAME, "widget-recommend-item")
    system_button[0].click()

    time.sleep(10)
    going_button = driver.find_element(By.ID, "ampDetailEnter")
    print(going_button.text)
    if going_button.is_displayed() and going_button.is_enabled():
        going_button.click()
    else:
        driver.execute_script("arguments[0].click();", going_button)
    # 获取登录后的cookie
    time.sleep(10)
    search_window = driver.window_handles
    driver.switch_to.window(search_window[1])
    cookies = driver.get_cookies()
    result = {
        'bzb_jsxsd': '',
        'sdp_app_session-443': '',
        'sdp_app_session-legacy-443': '',
    }
    for c in cookies:
        key = c.get('name')
        if key in result:
            result[key] = c.get('value')
    driver.quit()
    cookie = ''
    for k, v in result.items():
        cookie += f'{k}={v};'
    logger.info("cookie:{}", cookie)
    saveCookie(cookie)
    return cookie


def saveCookie(cookie: str):
    db = pymysql.connect(host="114.132.175.70", user="Course", password="NRNdLmpmWpx6jMRT", database='course')
    cursor = db.cursor()

    sql = "INSERT INTO `cookies` (`value`) VALUES (%s)"
    cursor.execute(sql, cookie)
    db.commit()
    db.close()


def getSqlCookie():
    db = pymysql.connect(host="114.132.175.70", user="Course", password="NRNdLmpmWpx6jMRT", database='course')
    cursor = db.cursor()
    sql = "SELECT * FROM `cookies` order by id desc limit 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result[0]
