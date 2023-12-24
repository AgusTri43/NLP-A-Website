from flask import Flask, render_template, request, jsonify
import os
import joblib
import operator
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
# Memuat model dari file
model = joblib.load("nlpmodel.pkl")
tfidf_vectorizer = joblib.load("vectorizer.pkl")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sentimen")
def sentimenpage():
    return render_template('sentimen.html')

@app.route("/textsum")
def textsumpage():
    return render_template('textsum.html')

# Sentimen Analysis
@app.route('/predict', methods=['POST', 'GET'])
def predict():
     data = request.get_json()
     teks = data['teks']
     
     # Praproses teks menggunakan TF-IDF Vectorizer
     teks_vectorized = tfidf_vectorizer.transform([teks])
     
     #melakukan prediksi
     hasil_prediksi = model.predict(teks_vectorized)
     
     # Mendapatkan label sentimen dari hasil prediksi
     label_sentimen = "Positif" if hasil_prediksi[0] == 1 else "Negatif"
     
     # Mengembalikan hasil prediksi
     return jsonify({'sentimen': hasil_prediksi[0]})

#Text Summarization
def load_stopWords():
    url = "https://raw.githubusercontent.com/Wayan123/Sentiment-Analysis/main/stopwordlist.txt"
    ina_stopword = requests.get(url).content
    return ina_stopword.split()

def cleanData(sentence):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stopwords = load_stopWords()
    ret = []
    sentence = stemmer.stem(sentence)
    for word in sentence.split():
        if word not in stopwords:
            ret.append(word)
    return " ".join(ret)

def calculateSimilarity(sentence, doc):
    if doc == []:
        return 0
    vocab = {}
    for word in sentence:
        vocab[word] = 0

    docInOneSentence = ''
    for t in doc:
        docInOneSentence += (t + ' ')
        for word in t.split():
            vocab[word] = 0

    cv = CountVectorizer(vocabulary=vocab.keys())

    docVector = cv.fit_transform([docInOneSentence])
    sentenceVector = cv.fit_transform([sentence])
    return cosine_similarity(docVector, sentenceVector)[0][0]

@app.route('/predict1', methods=['GET', 'POST'])
def predicttextsum():
    summary = ''
    percentage = 50
    if request.method == 'POST':
        text_input = request.form['text_input']
        if 'percentage' in request.form:
            percentage = int(request.form['percentage'])
        texts = text_input.split('\n')

        sentences = []
        clean = []
        originalSentenceOf = {}

        for line in texts:
            parts = line.split('.')
            for part in parts:
                cl = cleanData(part)
                sentences.append(part)
                clean.append(cl)
                originalSentenceOf[cl] = part

        setClean = set(clean)
        scores = {}
        for data in clean:
            temp_doc = setClean - set([data])
            score = calculateSimilarity(data, list(temp_doc))
            scores[data] = score

        n = percentage * len(sentences) / 100
        alpha = 0.5
        summarySet = []
        while n > 0:
            mmr = {}

            for sentence in scores.keys():
                if sentence not in summarySet:
                    mmr[sentence] = alpha * scores[sentence] - (1-alpha) * calculateSimilarity(sentence, summarySet)
            selected = max(mmr.items(), key=operator.itemgetter(1))[0]
            summarySet.append(selected)
            n -= 1

        summary = '\n'.join([originalSentenceOf[sentence].lstrip(' ') for sentence in summarySet])

    return render_template('textsum.html', summary=summary, text_input=text_input)

if __name__ == '__main__':
    app.run(debug=True)