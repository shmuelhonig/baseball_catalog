from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
import random, string

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Teams, Players

# Imports for using Flask_Dance
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)

engine = create_engine('sqlite:///baseball.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# helper function - create user and return user id
def createUser(login_session):
    newUser = Users(name = login_session['name'], email =\
        login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id

# helper function - take in user id and return user object
def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user

# helper function - take in user email and return user id
def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None

# Flask_Dance code for Google sign-in
blueprint = make_google_blueprint(
    client_id="1040126620381-5sem9r51c2qic7l4utomj6hom8a6a4mn.apps.googleusercontent.com",
    client_secret="I9whaUHlwFfkbLQ2U0Od9jku",
    scope=["profile", "email"],
    offline=True,
    redirect_url="http://localhost:8000/teams"
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/google/login")
def googleLogin():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    login_session['provider'] = 'google'
    login_session['name'] = resp.json()['name']
    login_session['email'] = resp.json()['email']
    # check to see if user exists, if not then create one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    # store user_id in session
    login_session['user_id'] = user_id
    assert resp.ok, resp.text
    return redirect("http://localhost:8000/teams")

@app.route("/logout")
def logout():
    if login_session['provider'] == 'google':
        try:
            google.get("https://accounts.google.com/o/oauth2/revoke?token=" + google.access_token)
        except:
            pass
        try:
            del blueprint.token
        except:
            pass
        login_session.pop('name', None)
        login_session.pop('email', None)
        login_session.pop('user_id', None)
    return redirect("http://localhost:8000/teams")


# Show all Teams
@app.route('/')
@app.route('/teams/')
def showTeams():
    teams = session.query(Teams).order_by(asc(Teams.name))
    if not google.authorized:
        return render_template('publicteams.html', teams=teams)
    else:
        return render_template('teams.html', teams=teams)


# Create new team
@app.route('/teams/new/', methods=['GET','POST'])
def newTeam():
    if not google.authorized:
        return "You are not authorized to view this page. Please log in."
    if request.method == 'POST':
        # Check csrf token
        if request.form['csrf_token'] != login_session.pop('csrf_token', None):
            return "You are not authorized to make changes"

        newTeam = Teams(name=request.form['name'],\
            user_id=login_session['user_id'])
        session.add(newTeam)
        session.commit()
        flash('New team %s successfully created' % newTeam.name)
        return redirect(url_for('showTeams'))
    else:
        # Create and store csrf token before rendering template
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)\
            for x in xrange(32))
        login_session['csrf_token'] = state
        return render_template('newTeam.html')

# Edit team name
@app.route('/<team_id>/edit/', methods=['GET','POST'])
def editTeam(team_id):
    teamToUpdate = session.query(Teams).filter_by(id=team_id).one()
    oldName = teamToUpdate.name
    if request.method == 'POST':
        # Check csrf token
        if request.form['csrf_token'] != login_session.pop('csrf_token', None):
            return "You are not authorized to make changes"

        teamToUpdate.name = request.form['newname']
        session.add(teamToUpdate)
        session.commit()
        flash('Successfully renamed %s to %s' % (oldName, teamToUpdate.name))
        return redirect(url_for('showTeams'))
    else:
        if not google.authorized:
            return "You are not authorized to view this page. Please log in."
        else:
            # if owner
            if teamToUpdate.user_id == getUserID(login_session['email']):
                # Create and store csrf token before rendering template
                state = ''.join(random.choice(string.ascii_uppercase\
                    + string.digits) for x in xrange(32))
                login_session['csrf_token'] = state
                return render_template('editTeam.html', oldname=oldName,\
                    team_id=team_id)
            #if not owner
            else:
                return "You are not the owner of the team or player."

# Delete team
@app.route('/<team_id>/delete/', methods=['GET', 'POST'])
def deleteTeam(team_id):
    teamToDelete = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        # Check csrf token
        if request.form['csrf_token'] != login_session.pop('csrf_token', None):
            return "You are not authorized to make changes"

        session.delete(teamToDelete)
        session.commit()
        flash('Successfully deleted the %s' % (teamToDelete.name))
        return redirect(url_for('showTeams'))
    else:
        if not google.authorized:
            return "You are not authorized to view this page. Please log in."
        else:
            # if owner
            if teamToDelete.user_id == getUserID(login_session['email']):
                # Create and store csrf token before rendering template
                state = ''.join(random.choice(string.ascii_uppercase\
                    + string.digits) for x in xrange(32))
                login_session['csrf_token'] = state
                return render_template('deleteTeam.html',\
                    teamToDelete=teamToDelete)
            #if not owner
            else:
                return "You are not the owner of the team or player."


# Show team roster
@app.route('/<team_id>/roster/')
def showRoster(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    roster = session.query(Players).filter_by(team_id=team.id).\
             order_by(asc(Players.name))
    if not google.authorized:
        return render_template('publicroster.html', roster=roster, team=team)
    else:
        # if owner
        if team.user_id == getUserID(login_session['email']):
            return render_template('roster.html', roster=roster, team=team)
        # if not owner
        else:
            return render_template('publicroster.html', roster=roster, team=team)



# Create new player
@app.route('/<team_id>/roster/new/', methods=['GET', 'POST'])
def newPlayer(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        # Check csrf token
        if request.form['csrf_token'] != login_session.pop('csrf_token', None):
            return "You are not authorized to make changes"

        newPlayer = Players(name=request.form['name'],\
            position=request.form['position'], number=request.form['number'],\
            handedness=request.form['handedness'],\
            team_id=team_id, user_id=login_session['user_id'])
        session.add(newPlayer)
        session.commit()
        flash('Successfully added %s' % (newPlayer.name))
        return redirect(url_for('showRoster', team_id=team_id))
    else:
        if not google.authorized:
            return "You are not authorized to view this page. Please log in."
        else:
            # if owner
            if team.user_id == getUserID(login_session['email']):
                # Create and store csrf token before rendering template
                state = ''.join(random.choice(string.ascii_uppercase\
                    + string.digits) for x in xrange(32))
                login_session['csrf_token'] = state
                return render_template('newPlayer.html', team=team,\
                    team_id=team_id)
            #if not owner
            else:
                return "You are not the owner of the team or player."

# Edit player
@app.route('/<team_id>/<player_id>/edit/', methods=['GET', 'POST'])
def editPlayer(team_id, player_id):
    playerToUpdate = session.query(Players).filter_by(id=player_id).one()
    if request.method == 'POST':
        # Check csrf token
        if request.form['csrf_token'] != login_session.pop('csrf_token', None):
            return "You are not authorized to make changes"

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
        if not google.authorized:
            return "You are not authorized to view this page. Please log in."
        else:
            # if owner
            if playerToUpdate.user_id == getUserID(login_session['email']):
                # Create and store csrf token before rendering template
                state = ''.join(random.choice(string.ascii_uppercase\
                    + string.digits) for x in xrange(32))
                login_session['csrf_token'] = state
                return render_template('editPlayer.html', team_id=team_id,\
                    playerToUpdate=playerToUpdate)
            #if not owner
            else:
                return "You are not the owner of the team or player."

# Delete player
@app.route('/<team_id>/<player_id>/delete/', methods=['GET', 'POST'])
def deletePlayer(team_id, player_id):
    playerToDelete = session.query(Players).filter_by(id=player_id).one()
    if request.method == 'POST':
        # Check csrf token
        if request.form['csrf_token'] != login_session.pop('csrf_token', None):
            return "You are not authorized to make changes"

        session.delete(playerToDelete)
        session.commit()
        flash('Successfully deleted %s' % (playerToDelete.name))
        return redirect(url_for('showRoster', team_id=team_id))
    else:
        if not google.authorized:
            return "You are not authorized to view this page. Please log in."
        else:
            # if owner
            if playerToDelete.user_id == getUserID(login_session['email']):
                # Create and store csrf token before rendering template
                state = ''.join(random.choice(string.ascii_uppercase\
                    + string.digits) for x in xrange(32))
                login_session['csrf_token'] = state
                return render_template('deletePlayer.html', team_id=team_id,\
                    playerToDelete=playerToDelete)
            #if not owner
            else:
                return "You are not the owner of the team or player."


# JSON endpoint for teams
@app.route('/teams/api/json/')
def showTeamsJSON():
    teams = session.query(Teams).order_by(asc(Teams.name)).all()
    return jsonify(teams=[t.serialize for t in teams])

#JSON endpoint for rosters
@app.route('/<team_id>/roster/api/json/')
def showRosterJSON(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    roster = session.query(Players).filter_by(team_id=team.id).\
             order_by(asc(Players.name)).all()
    return jsonify(roster=[p.serialize for p in roster])

#JSON endpoint for all players
@app.route('/allplayers/api/json/')
def showAllPlayersJSON():
    allPlayers = session.query(Players).order_by(asc(Players.name)).all()
    return jsonify(allPlayers=[a.serialize for a in allPlayers])


if __name__ == '__main__':
    app.secret_key = "supersekrit"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000, threaded = False)
