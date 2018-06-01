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
@app.route('/<team_name>/edit/', methods=['GET','POST'])
def editTeam(team_name):
    teamToUpdate = session.query(Teams).filter_by(name=team_name).one()
    oldName = teamToUpdate.name
    if request.method == 'POST':
        teamToUpdate.name = request.form['newname']
        session.add(teamToUpdate)
        session.commit()
        flash('Successfully renamed %s to %s' % (oldName, teamToUpdate.name))
        return redirect(url_for('showTeams'))
    else:
        return render_template('editTeam.html', oldname=oldName)


# Show team roster
@app.route('/<team_name>/')
@app.route('/<team_name>/roster/')
def showRoster(team_name):
    team = session.query(Teams).filter_by(name=team_name).all()
    team_id = team[0].id
    roster = session.query(Players).filter_by(team_id=team_id).\
             order_by(asc(Players.name))
    return render_template('roster.html', roster=roster, team=team)


if __name__ == '__main__':
    app.secret_key = "supersekrit"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000, threaded = False)
