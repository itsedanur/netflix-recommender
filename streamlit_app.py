import streamlit as st
import pandas as pd
import numpy as np
import requests
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 🔑 TMDb API Key
TMDB_API_KEY = "dd2e466bad73988907d3fd73a492a03d"

# 📥 Stopwords yükle
nltk.download('stopwords')
english_stop_words = stopwords.words('english')

# 📁 Veri yükle
df = pd.read_csv("netflix_titles.csv")
df['description'] = df['description'].fillna('')
df['cast'] = df['cast'].fillna('')
df['listed_in'] = df['listed_in'].fillna('')
df['metadata'] = df['description'] + ' ' + df['listed_in'] + ' ' + df['cast']

# 🎯 TF-IDF ve benzerlik matrisi
tfidf = TfidfVectorizer(stop_words=english_stop_words)
tfidf_matrix = tfidf.fit_transform(df['metadata'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# 🧠 Giriş sistemi
users = {"eda": "1234", "guest": "0000"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Giriş Yap")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if username in users and users[username] == password:
            st.success(f"Hoş geldin, {username}!")
            st.session_state.logged_in = True
            st.session_state.user = username
        else:
            st.error("Hatalı kullanıcı adı veya şifre.")
    st.stop()

# 🗂️ Oturum içi veri tanımları
if "favorites" not in st.session_state:
    st.session_state['favorites'] = []

if "comments" not in st.session_state:
    st.session_state.comments = {}

if "likes" not in st.session_state:
    st.session_state.likes = {}

# 🖼️ Poster çekme fonksiyonu
def get_poster(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# 🎬 Öneri fonksiyonu
def get_recommendations(title, cosine_sim=cosine_sim, df=df):
    if title not in indices:
        return pd.DataFrame()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df.iloc[movie_indices]

# 🧭 Sayfa Başlığı
st.title("🎬 Netflix Film Öneri Sistemi")
st.markdown("Bu sistem, seçtiğiniz filme benzer içerikleri önerir. Poster, açıklama, yorum, beğeni ve favori özellikleri içerir.")

# 🎛️ Sidebar filtreleme
with st.sidebar:
    st.header("🔍 Filtreleme")
    selected_type = st.selectbox("Tür", ["Hepsi"] + sorted(df['type'].dropna().unique()))
    selected_country = st.selectbox("Ülke", ["Hepsi"] + sorted(df['country'].dropna().unique()))
    selected_year = st.selectbox("Yıl", ["Hepsi"] + sorted(df['release_year'].dropna().unique(), reverse=True))

# 🎞️ Film seçimi
film_adlari = sorted(df['title'].dropna().unique())
secilen_film = st.selectbox("Bir film seçin:", film_adlari)

# 📡 Öneri butonu
if st.button("🎯 Önerileri Göster"):
    onerilenler = get_recommendations(secilen_film)

    # Filtreleri uygula
    if selected_type != "Hepsi":
        onerilenler = onerilenler[onerilenler['type'] == selected_type]
    if selected_country != "Hepsi":
        onerilenler = onerilenler[onerilenler['country'] == selected_country]
    if selected_year != "Hepsi":
        onerilenler = onerilenler[onerilenler['release_year'] == selected_year]

    if onerilenler.empty:
        st.warning("⚠️ Filtrelere uyan sonuç bulunamadı.")
    else:
        st.subheader("🎥 Önerilen Filmler:")
        for _, row in onerilenler.iterrows():
            st.markdown(f"### ✅ {row['title']}")
            poster_url = get_poster(row['title'])
            if poster_url:
                st.image(poster_url, width=200)
            st.caption(row['description'])

            # ❤️ Favorilere ekle
            if st.button(f"❤️ Favorilere Ekle: {row['title']}", key="fav_" + row['title']):
                if row['title'] not in st.session_state['favorites']:
                    st.session_state['favorites'].append(row['title'])

            # 👍 Beğeni
            if row['title'] not in st.session_state.likes:
                st.session_state.likes[row['title']] = 0
            if st.button(f"👍 Beğen ({st.session_state.likes[row['title']]})", key="like_" + row['title']):
                st.session_state.likes[row['title']] += 1

            # 💬 Yorum
            yorum = st.text_input(f"💬 Yorum yaz ({row['title']})", key="comment_" + row['title'])
            if st.button("Gönder", key="comment_btn_" + row['title']):
                st.session_state.comments.setdefault(row['title'], []).append((st.session_state.user, yorum))

            # 🗣️ Yorumları göster
            if row['title'] in st.session_state.comments:
                st.markdown("📌 Yorumlar:")
                for kullanici, metin in st.session_state.comments[row['title']]:
                    st.write(f"🗣️ {kullanici}: {metin}")

            st.markdown("---")

# ⭐ Favori listesi
if st.session_state['favorites']:
    st.sidebar.subheader("⭐ Favori Listen:")
    for fav in st.session_state['favorites']:
        st.sidebar.write("✅", fav)
