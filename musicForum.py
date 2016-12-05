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
    votesTotal = db.Column(db.Integer)


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

@app.route('/boards')
def boardsList():
    return render_template('boardsList.html')


@app.route('/profile/<user>')
def profile_page(user):
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    manager.run()
