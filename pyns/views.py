from flask import request, redirect, url_for, render_template, flash
from pyns import app, db
from pyns.models import Entry

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
