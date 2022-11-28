from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from . import db
from .models import Note, Article
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():

    cur = db.session.execute('SELECT * FROM article')
    articles = cur.fetchall()


    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    cur.close()
    return render_template("home.html", title="Home", user=current_user, articles=articles)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", title="Profile", user=current_user)


@views.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('text')
        #img = request.files['img']
        #name = img.filename
        #mimetype = img.mimetype
        user = current_user
        username = user.username
        if len(title) < 1:  
            flash('Please write a title', category='error')
        elif len(content) < 10:
            flash('The article is too short!', category='error')

        else: #add article to database
            print (content, title, user.username)
            new_article = Article(title=title, content=content, user=user, username=username)
            db.session.add(new_article)
            db.session.commit()
            flash('Article added!', category='success')

    return render_template("add_article.html", title="Write an article", user=current_user)


@views.route('/articles/', methods=['GET', 'POST'])
def articles():
    cur = db.session.execute('SELECT * FROM article')
    articles = cur.fetchall()

    cur.close()

    return render_template("article.html", title="Article", user=current_user, articles=articles)

@views.route('/article/<int:id>/', methods=['GET', 'POST'])
def article(id):
    cur = db.session.execute('SELECT * FROM article WHERE id = :id', {'id': id})

    #get article
    articles = cur.fetchall()

    cur.close()
    return render_template("article.html", title="Article", user=current_user, articles=articles)