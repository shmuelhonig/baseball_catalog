from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
import random, string

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Teams, Players

app = Flask(__name__)

engine = create_engine('sqlite:///baseball.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all Teams
@app.route('/')
@app.route('/teams/')
def showTeams():
    teams = session.query(Teams).order_by(asc(Teams.name))
    return render_template('teams.html', teams=teams)

# Create new team
@app.route('/teams/new/', methods=['GET','POST'])
def newTeam():
    if request.method == 'POST':
        newTeam = Teams(name=request.form['name'])
        session.add(newTeam)
        session.commit()
        flash('New team %s successfully created' % newTeam.name)
        return redirect(url_for('showTeams'))
    else:
        return render_template('newTeam.html')

# Edit team name
@app.route('/<team_id>/edit/', methods=['GET','POST'])
def editTeam(team_id):
    teamToUpdate = session.query(Teams).filter_by(id=team_id).one()
    oldName = teamToUpdate.name
    if request.method == 'POST':
        teamToUpdate.name = request.form['newname']
        session.add(teamToUpdate)
        session.commit()
        flash('Successfully renamed %s to %s' % (oldName, teamToUpdate.name))
        return redirect(url_for('showTeams'))
    else:
        return render_template('editTeam.html', oldname=oldName, team_id=team_id)

# Delete team
@app.route('/<team_id>/delete/', methods=['GET', 'POST'])
def deleteTeam(team_id):
    teamToDelete = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        session.delete(teamToDelete)
        session.commit()
        flash('Successfully deleted the %s' % (teamToDelete.name))
        return redirect(url_for('showTeams'))
    else:
        return render_template('deleteTeam.html', teamToDelete=teamToDelete)


# Show team roster
@app.route('/<team_id>/')
@app.route('/<team_id>/roster/')
def showRoster(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    roster = session.query(Players).filter_by(team_id=team.id).\
             order_by(asc(Players.name))
    return render_template('roster.html', roster=roster, team=team)

# Create new player
@app.route('/<team_id>/roster/new/', methods=['GET', 'POST'])
def newPlayer(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        newPlayer = Players(name=request.form['name'],\
            position=request.form['position'], number=request.form['number'],\
            handedness=request.form['handedness'],\
            team_id=team_id)
        session.add(newPlayer)
        session.commit()
        flash('Successfully added %s' % (newPlayer.name))
        return redirect(url_for('showRoster', team_id=team_id))
    else:
        return render_template('newPlayer.html', team=team, team_id=team_id)

# Edit player
@app.route('/<team_id>/<player_id>/edit/', methods=['GET', 'POST'])
def editPlayer(team_id, player_id):
    playerToUpdate = session.query(Players).filter_by(id=player_id).one()
    if request.method == 'POST':
        if request.form['name']:
            playerToUpdate.name = request.form['name']
        if request.form['position']:
            playerToUpdate.position = request.form['position']
        if request.form['number']:
            playerToUpdate.number = request.form['number']
        if request.form['handedness']:
            playerToUpdate.handedness = request.form['handedness']
        session.add(playerToUpdate)
        session.commit()
        flash('Successfully updated %s' % (playerToUpdate.name))
        return redirect(url_for('showRoster', team_id=team_id))
    else:
        return render_template('editPlayer.html', team_id=team_id,\
            playerToUpdate=playerToUpdate)

# Delete player
@app.route('/<team_id>/<player_id>/delete/', methods=['GET', 'POST'])
def deletePlayer(team_id, player_id):
    playerToDelete = session.query(Players).filter_by(id=player_id).one()
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        flash('Successfully deleted %s' % (playerToDelete.name))
        return redirect(url_for('showRoster', team_id=team_id))
    else:
        return render_template('deletePlayer.html', team_id=team_id,\
            playerToDelete=playerToDelete)


if __name__ == '__main__':
    app.secret_key = "supersekrit"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000, threaded = False)
