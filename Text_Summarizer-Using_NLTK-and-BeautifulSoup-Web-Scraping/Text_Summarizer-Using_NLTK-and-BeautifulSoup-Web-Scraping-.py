import nltk
import heapq
import lxml
nltk.download('punkt')
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import bs4 as bs
import urllib.request
import re
from nltk.tokenize import sent_tokenize,word_tokenize
from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)
@app.route('/')
def login_file():
    return render_template('login.html')

def scrap_Code(URL):
    scraped_data = urllib.request.urlopen(str(URL))
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    paragraphs = parsed_article.find_all('p')
    a= ""
    for p in paragraphs:
        a += p.text
    article_text = re.sub(r'\[[0-9]*\]', ' ', a)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    sentences = sent_tokenize(article_text)
    article_words = word_tokenize(article_text)
    formatted_words = word_tokenize(formatted_text)
    stop_words = stopwords.words('english')
    word_frequencies = {}
    for word in formatted_words:
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    max_freq = max(word_frequencies.values())
    for i in word_frequencies:
        word_frequencies[i] = word_frequencies[i] / max_freq
    # word_frequencies
    sent_score = {}
    for sent in sentences:
        for word in (word_tokenize(sent.lower())):
            if (word in word_frequencies):
                if len(sent.split(' ')) < 50:
                    if sent not in sent_score:
                        sent_score[sent] = word_frequencies[word]
                    else:
                        sent_score[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(7, sent_score, key=sent_score.get)
    summary = ' '.join(summary_sentences)
    return(summary)
@app.route('/login',methods=['POST','GET'])
def login():
   a=request.form['nm']
   summary=scrap_Code(str(a))
   return summary
   #return "jj"
if __name__ == '__main__':
   app.run(port=7000,debug=True)