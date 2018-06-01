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

@app.route('/<team_id>/')
@app.route('/<team_id>/roster/')
def showRoster(team_id):
    roster = session.query(Players).filter_by(team_id=team_id).order_by(asc(Players.name))
    return render_template('roster.html', roster=roster, team_id=team_id)


if __name__ == '__main__':
    app.secret_key = "supersekrit"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000, threaded = False)
