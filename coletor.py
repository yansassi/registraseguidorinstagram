from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from supabase import create_client, Client
import time
import csv
import os

# Supabase config
url = "https://irxhzelkcclzlgupwjgd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyeGh6ZWxrY2NsemxndXB3amdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0MDc1NzQsImV4cCI6MjA1OTk4MzU3NH0.eN0l8KuMK57ipLprKtrjjRzDFgdI1I0u79bzVWIaY-Q"
supabase: Client = create_client(url, key)

perfil_instagram = "megaeletronicosoficial"
url_insta = f"https://www.instagram.com/{perfil_instagram}/"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(options=options)

try:
    driver.get(url_insta)
    time.sleep(5)

    seguidores = driver.find_element(By.XPATH, '//ul/li[2]/a/div/span').get_attribute('title')
    seguidores = seguidores.replace('.', '').replace(',', '').strip()
    seguidores = int(seguidores)
    data_hoje = datetime.now().date()

    # Salvar no CSV local
    if not os.path.exists("seguidores.csv"):
        with open("seguidores.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["data", "seguidores"])

    with open("seguidores.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data_hoje, seguidores])

    print(f"Registrando {seguidores} seguidores em {data_hoje}...")

    # Enviar para Supabase
    res = supabase.table("seguidores").insert({
        "data": str(data_hoje),
        "seguidores": seguidores
    }).execute()

    print("Registro no Supabase:", res)

finally:
    driver.quit()