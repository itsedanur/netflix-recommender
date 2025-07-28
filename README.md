#  Netflix Film Öneri Sistemi

Bu proje, seçtiğiniz bir Netflix filmini analiz ederek **benzer içerikleri öneren** bir film öneri sistemidir. İçerikler; film açıklaması, kullanıcı yorumları, tür, ülke ve beğeniler gibi birçok özellik üzerinden değerlendirilir.

##  Özellikler

-  Film seçerek benzer öneriler alma
-  Film açıklamaları ve poster gösterimi
-  Favorilere film ekleyebilme
-  Ülke, Tür, Yıl filtreleme
- NLP (Doğal Dil İşleme) ile içerik analizi

## Canlı Uygulama

Streamlit Cloud üzerinden uygulamayı buradan deneyimleyebilirsiniz:

 [Netflix Film Öneri Sistemi](https://netflix-recommender-xxpq839fbsia6axxzq5cyn.streamlit.app)

## 📂 Proje Yapısı
netflix-film-öneri-sistemi/
│
├── netflix_titles.csv # Veri kümesi
├── main.py # Model eğitim dosyası 
├── streamlit_app.py # Streamlit uygulaması
├── requirements.txt # Bağımlılıklar
└── README.md # 

##  Kullanılan Kütüphaneler

- `pandas`
- `numpy`
- `scikit-learn`
- `nltk`
- `streamlit`
- `requests`

##  Kurulum (Local'de çalıştırmak isteyenler için)

```bash
git clone https://github.com/itsedanur/netflix-recommender.git
cd netflix-recommender
pip install -r requirements.txt
streamlit run streamlit_app.py

 Veri Kümesi

Bu proje, Netflix Movies and TV Shows veri seti kullanılarak oluşturulmuştur.

##  Projeden Ekran Görüntüleri

Aşağıda sistemin çalışırken aldığım ekran görüntüleri yer almakta:

https://github.com/itsedanur/netflix-recommender/blob/main/images/Ekran%20Resmi%202025-07-28%2012.33.57.png?raw=true
https://github.com/itsedanur/netflix-recommender/blob/main/images/Ekran%20Resmi%202025-07-28%2012.34.03.png?raw=true
https://github.com/itsedanur/netflix-recommender/blob/main/images/Ekran%20Resmi%202025-07-28%2012.34.52.png?raw=true
https://github.com/itsedanur/netflix-recommender/blob/main/images/Ekran%20Resmi%202025-07-28%2012.35.03.png?raw=true

👩‍💻 Geliştirici

Ad Soyad: Eda Nur Unal
