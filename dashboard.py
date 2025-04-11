import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configurações Supabase
SUPABASE_URL = "https://irxhzelkcclzlgupwjgd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyeGh6ZWxrY2NsemxndXB3amdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0MDc1NzQsImV4cCI6MjA1OTk4MzU3NH0.eN0l8KuMK57ipLprKtrjjRzDFgdI1I0u79bzVWIaY-Q"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def buscar_dados():
    url = f"{SUPABASE_URL}/rest/v1/seguidores?select=*"
    r = requests.get(url, headers=HEADERS)
    return r.json() if r.status_code == 200 else []

def registrar_no_supabase(data, seguidores):
    url = f"{SUPABASE_URL}/rest/v1/seguidores"
    payload = {
        "data": data,
        "seguidores": seguidores
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.status_code == 201

def capturar_seguidores():
    perfil_instagram = "megaeletronicosoficial"
    url = f"https://www.instagram.com/{perfil_instagram}/"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)

    seguidores = None
    try:
        driver.get(url)
        time.sleep(5)
        seguidores = driver.find_element(By.XPATH, '//ul/li[2]/a/div/span').get_attribute('title')
        seguidores = seguidores.replace('.', '').replace(',', '').strip()
        seguidores = int(seguidores)
    finally:
        driver.quit()

    if seguidores:
        hoje = datetime.now().date().isoformat()
        sucesso = registrar_no_supabase(hoje, seguidores)
        if sucesso:
            st.success(f"{seguidores} seguidores registrados com sucesso!")
        else:
            st.error("Erro ao salvar no Supabase.")

st.title("📊 Monitor de Seguidores - @megaeletronicosoficial")

if st.button("📥 Capturar Seguidores Agora"):
    capturar_seguidores()

dados = buscar_dados()
if not dados:
    st.warning("Nenhum dado disponível.")
else:
    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    st.subheader("Evolução diária de seguidores")
    plt.figure(figsize=(10, 4))
    plt.plot(df["data"], df["seguidores"], marker='o')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    if len(df) >= 2:
        diff = int(df["seguidores"].iloc[-1]) - int(df["seguidores"].iloc[-2])
        st.metric("📈 Variação de ontem para hoje", f"{diff:+,} seguidores")

    if len(df) >= 7:
        semanal = df.tail(7)
        media = semanal["seguidores"].diff().mean()
        st.metric("📅 Crescimento médio nos últimos 7 dias", f"{media:.2f} seguidores/dia")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar CSV", csv, "seguidores.csv", "text/csv")