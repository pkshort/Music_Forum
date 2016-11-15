import os, unicodedata
from sqlalchemy.orm import load_only
from flask import Flask, render_template, flash, url_for, session
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'forumData.sqlite')

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    homeTown = db.Column(db.String(64))
    bio = db.Column(db.String(64))
    isMusician = db.Column(db.Boolean())
    boards = db.relationship('UserToBoard')

    def __repr__(self):
        return self.userName

class UserToBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    board = db.Column(db.Integer, db.ForeignKey("board.id"))

class Board(db.Model):
    __tablename = 'board'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    posts = db.relationship('posts')

    def __repr__(self):
        return self.title

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    timeStamp = db.Column(db.DateTime)
    boardId = db.relationship('board.id', backref='board', lazy='dynamic')
    votes = db.Column(db.Integer)

    def __repr__(self):
        return self.title

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    votes = db.Column(db.Integer)
    postId = db.relationship('posts.id', backref='posts', lazy='dynamic')



@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


#class NameForm(Form):
#    genres = Genre.query.filter()
#    genreList = []
#    count = 1
#    for i in genres:
#        genreList.append((count, i))
#        count += 1
#    artistName = StringField('Artist name')
#    artistGenre = SelectField(label='Genres', choices=genreList, validators=None)
#    artistDesc = StringField('Description')
#    submit = SubmitField('Submit')


#class GenreForm(Form):
#    genre = StringField('Genre name', validators=[Required()])
#    submit = SubmitField('Submit')

#@app.route('/newartist', methods=['GET', 'POST'])
#def new_artist():
#    form = NameForm()
#    if form.is_submitted():
#        artist = form.artistName.data
#        unicodedata.normalize('NFKD', artist)
#        check = Artist.query.filter_by(artistName=artist).first()
#        if check is None:
#            newArtist = Artist()
#            newArtist.artistName = form.artistName.data
#            newArtist.desc = form.artistDesc.data
#            temp_id = Genre.query.filter_by(id=form.artistGenre.data).first()
#            newArtist.genre_id = temp_id.id
#            db.session.add(newArtist)
#            flash('New band submitted')
#            db.session.commit()
#            return render_template('newartist.html', form=form, artistName=newArtist)
#        else:
#            flash('Band already in system..')
#            return render_template(url_for('newartist.html', form=form))
#    return render_template('newartist.html', form=form)


#def addItem(artist, desc):
#    my_dict = session['bands']
#    my_dict[artist] = desc
#    session['bands'] = my_dict


#@app.route('/artistPage/<artistName>', methods=['GET'])
#def artist_page(artistName):
#    artist = Artist.query.filter_by(artistName=artistName).first()
#    genres = Genre.query.filter_by(id=artist.genre_id)
#    temp = Artist.query.filter_by(desc=artist.desc).first()
#    description = temp.desc
#    return render_template('artistPage.html', name=artist, genre=genres, desc=description)


#@app.route('/newgenre', methods=['GET', 'POST'])
#def new_genre():
#    form = GenreForm()
#    if form.validate_on_submit():
#        temp_genre = form.genre.data
#        unicodedata.normalize('NFKD', temp_genre)
#        check = Genre.query.filter_by(genreName=temp_genre).first()
#        if check is None:
#            newGenre = Genre()
#            newGenre.genreName = temp_genre
#            flash('New Genre Submitted')
#            db.session.add(newGenre)
#            db.session.commit()
#            return render_template('newGenre.html', form=form)
#        flash('Genre already in database..')
#        return render_template('newGenre.html', form=form)
#
#    return render_template('newGenre.html', form=form)



#@app.route('/artistlist', methods=['GET'])
#def artistlist():
#    myArtists = Artist.query.all()
#    return render_template('artistList.html', artists=myArtists)


if __name__ == '__main__':
    db.create_all()
    manager.run()
