# Kütüphanelerin Eklenmesi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords

# NLTK stopwords indir (ilk seferde çalıştırman yeterli)
nltk.download('stopwords')
english_stop_words = stopwords.words('english')

# Verinin Yüklenmesi
netflix_data = pd.read_csv("netflix_titles.csv")  # Dosya adını uygun şekilde güncelle

# TF-IDF vektörleştirme işlemi (Açıklamaları baz alarak içerik benzerliği)
tfidf = TfidfVectorizer(stop_words=english_stop_words)
netflix_data['description'] = netflix_data['description'].fillna('')
tfidf_matrix = tfidf.fit_transform(netflix_data['description'])

# Benzerlik matrisi oluşturma (cosine similarity)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Başlıkları indexleme
indices = pd.Series(netflix_data.index, index=netflix_data['title']).drop_duplicates()

# Öneri Fonksiyonu
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # İlk sonuç kendisi olacağı için atlıyoruz
    movie_indices = [i[0] for i in sim_scores]
    return netflix_data['title'].iloc[movie_indices]

# Örnek kullanım
print("Peaky Blinders benzeri öneriler:\n", get_recommendations("Peaky Blinders"))
print("Dark benzeri öneriler:\n", get_recommendations("Dark"))
print("The Queen's Gambit benzeri öneriler:\n", get_recommendations("The Queen's Gambit"))

# (Opsiyonel) Bazı görseller:
sns.set_style("darkgrid", {"grid.color": "black", "grid.linestyle": ":"})
plt.figure(figsize=(10, 5))
sns.countplot(x="type", data=netflix_data, palette="Set2")
plt.title("İçerik Türü Dağılımı")
plt.show()

plt.figure(figsize=(20, 12))
sns.set(style="dark")
ax = sns.countplot(y="release_year", data=netflix_data, palette="bright",
                   order=netflix_data['release_year'].value_counts().index[:15])
plt.title("En Çok İçerik Çıkan Yıllar")
plt.show()
