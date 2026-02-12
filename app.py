import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("hour_analysis.csv")
    return df


df = load_data()

df['year'] = df['yr'].map({0: 2011, 1: 2012})

season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

df['season'] = df['season'].map(season_map)
df['weather'] = df['weathersit'].map(weather_map)

st.sidebar.title("Filter Dashboard")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=df['year'].unique(),
    default=df['year'].unique()
)

df_filtered = df[df['year'].isin(selected_year)]

st.title("🚲 Bike Sharing Business Dashboard")
st.markdown("Analisis Pelanggan 2011–2012")

total_rental = df_filtered['cnt'].sum()
total_registered = df_filtered['registered'].sum()
total_casual = df_filtered['casual'].sum()

dominasi = "Registered" if total_registered > total_casual else "Casual"

growth = (
        df.groupby('year')['cnt'].sum().pct_change().iloc[-1] * 100
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{int(total_rental):,}")
col2.metric("Total Registered", f"{int(total_registered):,}")
col3.metric("Total Casual", f"{int(total_casual):,}")
col4.metric("Growth 2012 vs 2011", f"{growth:.2f}%")

st.divider()

st.subheader("📊 Perbandingan Registered vs Casual per Tahun")

yearly_users = df_filtered.groupby('year')[['casual', 'registered']].sum().reset_index()

fig1, ax1 = plt.subplots()
yearly_users.set_index('year').plot(kind='bar', ax=ax1)
plt.xticks(rotation=0)
plt.ylabel("Jumlah Penyewaan")
st.pyplot(fig1)

# Insight otomatis
if yearly_users['registered'].sum() > yearly_users['casual'].sum():
    st.success("Registered users mendominasi dibanding casual users.")
else:
    st.warning("Casual users lebih tinggi dari registered users.")

st.divider()

st.subheader("🌤️ Total Rental Berdasarkan Musim")

season_data = df_filtered.groupby('season')['cnt'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
sns.barplot(x=season_data.index, y=season_data.values, ax=ax2)
plt.xticks(rotation=45)
plt.ylabel("Total Rental")
st.pyplot(fig2)

best_season = season_data.idxmax()
st.info(f"Musim dengan rental tertinggi adalah **{best_season}**.")

st.divider()

st.subheader("🌦️ Total Rental Berdasarkan Cuaca")

weather_data = df_filtered.groupby('weather')['cnt'].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots()
sns.barplot(x=weather_data.index, y=weather_data.values, ax=ax3)
plt.xticks(rotation=45)
plt.ylabel("Total Rental")
st.pyplot(fig3)

best_weather = weather_data.idxmax()
st.info(f"Cuaca dengan rental tertinggi adalah **{best_weather}**.")

st.divider()

st.subheader("📌 Business Insight")

st.markdown(f"""
- Pelanggan **{dominasi}** mendominasi sistem rental.
- Terjadi pertumbuhan sebesar **{growth:.2f}%** dari 2011 ke 2012.
- Musim terbaik: **{best_season}**
- Cuaca terbaik: **{best_weather}**

🎯 **Rekomendasi:**
- Fokuskan promosi pada musim {best_season}.
- Tingkatkan konversi casual menjadi registered.
- Buat promo khusus saat cuaca {best_weather}.
""")
