import os
from os import environ
from flask import Flask, render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, g
import datetime
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY") or 'qwerty'


app.permanent_session_lifetime = datetime.timedelta(seconds=10000)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musics.bd'
db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(255), nullable=False)


@app.route('/')
@app.route('/index')
def index():  # put application's code here
    q = request.args.get('q')

    if q:
        music = Music.query.filter(Music.name.contains(q) | Music.content.contains(q))
        return render_template('search.html', data=music)
    else:
        return render_template('index.html')



@app.route('/search')
def search():  # put application's code here
    songs = os.listdir("static/music/")
    q = request.args.get('q')
    if q:
        music = Music.query.filter(Music.name.contains(q))
        songs = os.listdir("static/music/" + Music.content)
        return render_template('search.html', data=music, songs=songs)
    else:
        music = Music.query.order_by(Music.name).all()
    return render_template('search.html', data=music, songs=songs)


@app.route('/add', methods=['POST', 'GET'])
def add():
    # put application's code here
    target = os.path.join(APP_ROOT, 'static/music/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = os.path.join(target, filename)
        print(destination)
        file.save(destination)

    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']

        music = Music(name=name, content=content)

        try:
            db.session.add(music)
            db.session.commit()
            return redirect('/')
        except:
            flash('Путь к файлу: /static/music/(имя файла)', category='success')

            return 'There was an error adding music'

    return render_template('add.html')
@app.route('/all')
def all():
    songs = os.listdir("static/music/")
    return render_template('all.html', songs=songs)


if __name__ == '__main__':
    app.run(debug=True)
