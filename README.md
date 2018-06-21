# Baseball Catalog

This project uses Python's Flask framework to create a web app containing a catalog for baseball teams and players. The app allows users to log in and out using Google sign-in, and to add, edit, and delete teams and players from the database. It was created as part of Udacity's Full Stack Web Development Nanodegree program.

## Dependencies

In order to successfully run the baseball catalog app, the following libraries must be installed:
1. Flask
2. SQLAlchemy
3. Flask-Limiter
4. Flask_Dance

Note that for Flask_Dance to work properly, as stated in its documentation, the HTTPS requirement imposed by oauthlib must be disabled:

$ export OAUTHLIB_INSECURE_TRANSPORT=1

Also note that Python 3.6 was used for creating and testing the application.

## Configuration

First, run the populate_database.py file in order to create and populate the baseball database. When ready to begin using the app, run baseball_catalog.py and visit http://localhost:8000/.
