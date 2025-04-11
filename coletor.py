from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import csv
import os

perfil_instagram = "megaeletronicosoficial"
url = f"https://www.instagram.com/{perfil_instagram}/"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(options=options)

try:
    driver.get(url)
    time.sleep(5)

    seguidores = driver.find_element(By.XPATH, '//ul/li[2]/a/div/span').get_attribute('title')
    seguidores = seguidores.replace('.', '').replace(',', '').strip()

    if not os.path.exists("seguidores.csv"):
        with open("seguidores.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["data", "seguidores"])

    with open("seguidores.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().date(), seguidores])

    print(f"Seguidores registrados: {seguidores}")

finally:
    driver.quit()