from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

RSS_FEEDS = {
    'The Tyee': 'https://thetyee.ca/rss2.xml',
    # 'CBC': 'https://www.cbc.ca/webfeed/rss/rss-canada-britishcolumbia',
    'Daily Hive': 'https://dailyhive.com/feed/vancouver',
    'The Province': 'https://theprovince.com/feed'
}


@app.route('/')
def index():
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)

    # may have to add error handling here. not every rss feed has
    # a published_parsed field
    articles = sorted(articles, key=lambda x: x[1].published_parsed,
                      reverse=True)

    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]

    return render_template('index.html',
                           articles=paginated_articles, page=page,
                           total_pages=total_articles // per_page + 1)


@app.route('/search')
def search():
    query = request.args.get('q')
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)
    results = [article for article in articles if query.lower() in article[1].title.lower()]

    return render_template('search.html', articles=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
