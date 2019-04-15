from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

# elasticsearch = Elasticsearch()
elasticsearch = Elasticsearch(['localhost:9200', 'localhost:9201'])
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    if keyword:
        body = {
            "query": {
                "match": {
                    "cast": keyword
                }
            }
        }
    else:
        body = {
            "query": {
                "match_all": {}
            }
        }

    search_result = elasticsearch.search(index="movies", body=body)
    number_of_hits = search_result['hits']['total']['value']

    return render_template('index.html', keyword=keyword, hits=number_of_hits, movies=search_result['hits']['hits'])


app.run(port=5000, debug=True)
