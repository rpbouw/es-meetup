from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

elasticsearch = Elasticsearch()
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


@app.route('/morelikethis', methods=['GET'])
def more_like_this():
    id = request.args['id']
    keyword = request.args['keyword']

    if id:
        body = {
            "query": {
                "more_like_this": {
                    "fields": [
                        "plot.simple"
                    ],
                    "like": [
                        {
                            "_index": "movies",
                            "_id": id
                        }
                    ],
                    "min_term_freq": 1,
                    "max_query_terms": 30
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
