from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User
from flask_app.models.idea import Idea

@app.route('/ideas')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    ideas = Idea.get_all_ideas()
    return render_template('all.html', loggedUser = User.get_user_by_id(data), ideas = ideas)

@app.route('/ideas/delete/<int:id>')
def deleteShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    idea = Idea.get_idea_by_id(data)
    if user['id'] == idea['user_id']:
        Idea.delete(data)
    return redirect(request.referrer)

@app.route('/ideas', methods = ['POST'])
def createIdea():
    if 'user_id' not in session:
        return redirect('/')
    if not Idea.validate_idea(request.form):
        return redirect(request.referrer)
    data = {
        'idea': request.form['idea'],
        'user_id': session['user_id'],
    }
    Idea.create(data)
    return redirect('/')

@app.route('/users/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    idea = Idea.get_ideas_for_user(data)
    return render_template('oneuser.html', idea = idea, loggedUser = user)

@app.route('/ideas/edit/<int:id>')
def editIdea(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    idea = Idea.get_idea_by_id(data)
    if idea and idea['user_id'] == session['user_id']:
        return render_template('edit.html', loggedUser = User.get_user_by_id(data), idea = idea)
    return redirect('/')

@app.route('/ideas/edit/<int:id>', methods = ['POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    idea = Idea.get_idea_by_id(data)
    if idea and idea['user_id'] == session['user_id']:
        if not Idea.validate_idea(request.form):
            return redirect(request.referrer)
        data = {
            'idea': request.form['idea'],
            'id': id
        }
        Idea.update(data)
        flash('Idea succesfully updated', 'updateSucces')
        return redirect('/ideas' )
    return redirect('/')

@app.route('/teams/new')
def registerTeam():
    if 'user_id' not in session:
        return redirect('/dashboard')
    data = {
        'id': session['user_id']
    }
    return render_template('teams.html', loggedUser = User.get_user_by_id(data))


@app.route('/teams/new', methods = ['POST'])
def newTeam():
    if 'user_id' not in session:
        return redirect('/')
    if not Idea.validate_team(request.form):
        return redirect(request.referrer)
    team = Idea.get_team_by_id(request.form)
    if team:
        flash('Team must not be empty', 'team')
        return redirect(request.referrer)
    data = {
        'teamName': request.form['teamName'],
        'user_id' : session['user_id']
    }
    Idea.create_team(data)
    return redirect('/teams/new')