#!/usr/bin/env python3

'''

Youtube Channel Viewer
Developed by : Antonius (www.indodev.asia)
github : https://github.com/indodev-asia
You need this script to use rotating proxies ? just contact me

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def banner():
    print("\n\tYoutube Channel Viewer - dev by : Anton - www.indodev.asia\n")

def wait_seconds(seconds):
    print("[+] waiting ", seconds," seconds for the page to fully loaded")
    time.sleep(seconds)
    print("[+] done waiting")

def load_config():
    with open("config.txt", "r") as f:
        lines = f.readlines()
    config = {}
    for line in lines:
        key, value = line.strip().split("=")
        config[key] = value
    return config["email"], config["password"]

def load_channel_url():
    with open("channel.txt", "r") as f:
        return f.read().strip()

def setup_driver():
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")  
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    return driver

def login_to_youtube(driver, email, password):
    try:
        driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube")
        wait_seconds(8)
        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        wait_seconds(8)
        password_input = driver.find_element("name", "Passwd")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        wait_seconds(8)
    except Exception as e:
        raise e

def watch_channel_videos(driver, channel_url):
    try:
        driver.get(channel_url + "/videos")
        time.sleep(5)
        video_links = driver.find_elements("xpath", '//a[@id="thumbnail" and contains(@href, "watch?v=")]')
        if video_links != None:
            visited = set()
            for video in video_links:
                try:
                    href = video.get_attribute("href")
                    print("got href : ", href)
                    if href and href not in visited:
                        visited.add(href)
                        print("[+] visiting ", href)
                        driver.get(href)
                        print("[+] watch the video for 30 seconds")
                        wait_seconds(30)
                        driver.back()
                        time.sleep(3)
                except:
                    pass
                
                else:
                    print("video already visited")
    except Exception as e:
        raise e
    

def main():
    banner()
    email, password = load_config()
    channel_url = load_channel_url()
    driver = setup_driver()

    try:
        login_to_youtube(driver, email, password)
        watch_channel_videos(driver, channel_url)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
