from flask import request, redirect, url_for, render_template, flash
from pyns import app, db
from pyns.models import Entry
import os

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    entry = Entry(
            title=request.form['title'],
            text=request.form['text']
            )
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

# css reload at change
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
