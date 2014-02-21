import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'orgullopr.db'),
	DEBUG=True,
	SECRET_KEY='a',
	USERNAME='admin',
	PASSWORD='admin'
))
app.config.from_envvar('ORGULLOPR_SETTINGS', silent=True)

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

# TODO: set this up in a seperate setup.py file or something
def init_db():
	"""Initializes the application database"""
	with app.app_context():
		db = get_db()
		with app.open_resource('orgullopr.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
	"""Opens a new database connection if there is none yet for the current application context."""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request"""
	if hasattr(g, "sqlite_db"):
		g.sqlite_db.close

@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select name, town, proud_of, pride_in, youtube_link from testimonials')
	entries = cur.fetchall()
	return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	db = get_db()
	db.execute('insert into entries (name, town, proud_of, pride_in, youtube_link) values(?,?,?,?,?)',
					[request.form['name'], request.form['town'], request.form['proud_of'], request.form['pride_in'], request.form['youtube_link']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run(debug=True)
	url_for('static', filename='geotiles/pueblos.json')
	url_for('static', filename='geotiles/barrios.json')
	url_for('static', filename='geotiles/barrios+isla.json')
	url_for('static', filename='geotiles/barrios+isla+pueblos.json')
	url_for('static', filename='geotiles/barrios+pueblos.json')
	url_for('static', filename='geotiles/isla.json')
	url_for('static', filename='geotiles/isla+pueblos.json')
	url_for('static', filename='geotiles/pueblos.json')
	url_for('static', filename='geotiles/puertorico-geo.json')