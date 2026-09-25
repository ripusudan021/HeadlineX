from flask import Flask, render_template, request
import requests
from config import NEWS_API_KEY

app = Flask(__name__)

@app.route("/")
def home():
    query = request.args.get("query", "latest")

    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    news_data = response.json()

    articles = news_data.get("articles", [])
    filter_articles = [article for article in articles if article.get("description")]

    top_article = None
    rest_articles = []

    if filter_articles:
        top_article = filter_articles[0]
        rest_articles = filter_articles[1:]

    return render_template(
        "index.html",
        articles=rest_articles,
        query=query,
        top_article=top_article
    )

if __name__ == "__main__":
    app.run()