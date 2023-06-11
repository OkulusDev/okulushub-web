# -*- coding:utf-8 -*-
import sys
from flask import Flask, url_for, render_template, request
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
ARTICLE_DIR = 'articles'

HOST = '0.0.0.0'
PORT = 8000
app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route('/')
def index():
	posts = [p for p in flatpages if p.path.startswith(ARTICLE_DIR)]
	posts.sort(key=lambda item: item['date'], reverse=True)
	return render_template('index.html', posts=posts)


@app.route('/manuals')
def manuals():
	return render_template('manuals.html')


@app.route("/posts")
def posts():
	tags = ['новости сайта', 'безопасность', 'анонимность', 'сеть']
	posts = [p for p in flatpages if p.path.startswith(ARTICLE_DIR)]
	tag = request.args.get('tag')
	if tag not in tags:
		tag = 'all'

	posts.sort(key=lambda item: item['date'], reverse=True)
	if tag:
		return render_template('posts.html', posts=posts, tag=tag, tags=tags)
	else:
		return render_template('posts.html', posts=posts, tag='all', tags=tags)


@app.route('/pygments.css')
def pygments_css():
	return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


@app.route('/posts/<name>')
def post(name):
	path = '{}/{}'.format(ARTICLE_DIR, name)
	post = flatpages.get_or_404(path)
	return render_template('post.html', post=post)


@app.route('/download')
def download():
	return render_template('download.html')


@app.errorhandler(400)
def bad_request(e):
	return render_template('400.1')


if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == "build":
		freezer.freeze()
	else:
		app.run(debug=DEBUG, host=HOST, port=PORT)
