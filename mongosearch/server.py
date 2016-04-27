import re

from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo


app = Flask(__name__, template_folder=".")
app.config['MONGO_DBNAME'] = 'douban-group-database'
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    include = request.args.get('include')
    exclude = request.args.get('exclude')
    if None in (include, exclude):
        return "include or exclude is empty"
    include = str2list(include)
    exclude = str2list(exclude)
    include_cond = [re.compile(s) for s in include]
    exclude_cond = [{'title' : {'$not' : re.compile("^.*%s.*" % s)}} for s in exclude]

    i, e = len(include) != 0, len(exclude) != 0
    if not (i or e):
        data = mongo.db.group_topics.find()
    elif i and not e:
        data = mongo.db.group_topics.find({'title': {'$all': include_cond}})
    elif not i and e:
        data = mongo.db.group_topics.find({'$and': exclude_cond})
    else:
        data = mongo.db.group_topics.find({'$and': [
                {'title': {'$all': include_cond}},
                {'$and': exclude_cond}
            ]})
    return render_template('search_result.html', topic_list=data)


def str2list(s):
    s = set(s.strip().split(' '))
    s.discard('')
    return list(s)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug=True)
