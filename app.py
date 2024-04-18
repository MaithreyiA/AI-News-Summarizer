from flask import Flask, render_template, request, flash
import nltk
from textblob import TextBlob
from newspaper import Article
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key' 
nltk.download('punkt')

@app.route('/')
def index():
    return render_template('index.html', title='', authors='', publish_date='', summary='', sentiment='', top_image='')

@app.route('/', methods=['POST'])
def summarize():
    url = request.form['url']
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title = article.title
        authors = ', '.join(article.authors)
        publish_date = article.publish_date.strftime("%d/%m/%Y") if article.publish_date else ''
        summary = article.summary
        analysis = TextBlob(article.text)
        sentiment = "😊" if analysis.polarity > 0 else "😞" if analysis.polarity < 0 else "😐"
        top_image = article.top_image if hasattr(article, 'top_image') else ''
        return render_template('index.html', title=title, authors=authors, publish_date=publish_date, summary=summary, sentiment=sentiment, top_image=top_image)

    except Exception as e:
        flash("Give Proper URL")
        return render_template('index.html', title='', authors='', publish_date='', summary='', sentiment='', top_image='')

if __name__ == '__main__':
    app.run(debug=True)
