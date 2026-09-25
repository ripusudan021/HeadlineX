from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    query = request.args.get("query", "latest")
    
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if not news_api_key:
        return "NEWS_API_KEY is not configured.", 500

    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": news_api_key,
        "language": "en",
        "sortBy": "publishedAt"
    }
    
    try:
        response = requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        
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
    except requests.RequestException as e:
        return f"News API request failed: {e}", 500

if __name__ == "__main__":
    app.run()