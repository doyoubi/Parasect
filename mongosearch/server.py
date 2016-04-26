import re

from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo


app = Flask(__name__, template_folder=".")
app.config['MONGO_DBNAME'] = 'douban-group-database'
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    include = request.form.get('include')
    exclude = request.form.get('exclude')
    if None in (include, exclude):
        return "include or exclude is empty"
    include = include.strip()
    exclude = exclude.strip()

    i, e = len(include) != 0, len(exclude) != 0
    if not (i or e):
        data = mongo.db.group_topics.find()
    elif i and not e:
        data = mongo.db.group_topics.find({'title': {'$regex': include}})
    elif not i and e:
        data = mongo.db.group_topics.find({'title': {'$not': re.compile("^.*%s.*" % exclude)}})
    else:
        data = mongo.db.group_topics.find({'title': {
                '$regex': include,
                '$not': re.compile("^.*%s.*" % exclude),
            }})
    return render_template('search_result.html', topic_list=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug=True)
