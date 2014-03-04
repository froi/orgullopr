import sqlite3
import json
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key="a"

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'orgullopr.db'),
    DEBUG=True,
))
app.config.from_envvar('ORGULLOPR_SETTINGS', silent=True)


def dict_factory(cursor, row):
    """
    Used to substitute the sqlite.Row factory. This is done to avoid the tuple output from sqlite.Row.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = dict_factory
    return rv


# TODO: set this up in a seperate setup.py file or something
def init_db():
    """
    Initializes the application database
    """

    with app.app_context():
        db = get_db()

        # Create development DB
        with app.open_resource('orgullopr.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        # Execute development dummy data
        with app.open_resource('inserts.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def run_query(query, bindings=None):
    db = get_db()
    if bindings and len(bindings):
        cur = db.execute(query, bindings)
    else:
        cur = db.execute(query)
    return cur.fetchall()


def load_towns():
    """
    Loads into session all towns (municipios) in PR
    """
    if not hasattr(g, 'towns'):
        g.towns = run_query('select id, name from municipios')
    return g.towns


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request
    """

    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close


@app.route('/')
def index():
    load_towns()
    return render_template('index.html', towns=g.towns)


@app.route('/videos', methods=['GET'])
def show_videos():
    return render_template('videos.html')


@app.route('/videos/<municipio>', methods=['GET'])
def get_videos(municipio):
    """
    Get all videos from specified city and renders them in the videos view.
    """

    db = get_db()
    # cur = db.execute('select name, youtube_link from testimonials where town=?', [municipio])
    entries = run_query('select name, youtube_link from testimonials where town=?', [municipio])

    if entries and len(entries):
        return render_template('videos.html', videos=entries, municipio=municipio)
    else:
        flash('No se encontraron videos.')
        return render_template('videos.html', municipio=municipio)

@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    print request.form
    # db.execute('INSERT INTO entries (name, town, proud_of, pride_in, youtube_link) VALUES(?,?,?,?,?)',
    #            [request.form['name'], request.form['prof'], request.form['town'], request.form['proudof'],
    #             request.form['pridein'], request.form['pridegov'], request.form['youtubelink']])
    # db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


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