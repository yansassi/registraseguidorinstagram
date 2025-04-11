import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from supabase import create_client, Client

# Configurações do Supabase
url = "https://irxhzelkcclzlgupwjgd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyeGh6ZWxrY2NsemxndXB3amdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0MDc1NzQsImV4cCI6MjA1OTk4MzU3NH0.eN0l8KuMK57ipLprKtrjjRzDFgdI1I0u79bzVWIaY-Q"
supabase: Client = create_client(url, key)

st.title("📊 Monitor de Seguidores - @megaeletronicosoficial")

# Buscar dados do Supabase
response = supabase.table("seguidores").select("*").order("data", desc=False).execute()
dados = response.data

if not dados:
    st.warning("Nenhum dado disponível.")
else:
    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    # Gráfico
    st.subheader("Evolução diária de seguidores")
    plt.figure(figsize=(10, 4))
    plt.plot(df["data"], df["seguidores"], marker='o')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    # Comparação com o dia anterior
    if len(df) >= 2:
        diff = int(df["seguidores"].iloc[-1]) - int(df["seguidores"].iloc[-2])
        st.metric("📈 Variação de ontem para hoje", f"{diff:+,} seguidores")

    # Crescimento médio semanal
    if len(df) >= 7:
        semanal = df.tail(7)
        media = semanal["seguidores"].diff().mean()
        st.metric("📅 Crescimento médio nos últimos 7 dias", f"{media:.2f} seguidores/dia")

    # Botão de download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar CSV", csv, "seguidores.csv", "text/csv")