# flask-app

# Setup:

1. Clone this repo and cd into the root level
2. Make a `.env` file, and add a `SECRET_KEY` variable that can be any hard to guess string of characters.`If you are running the app locally, also toss in a DATABASE_URI` with a connection string pointing to an available database.
3. Create a venv: `python3 -m venv venv`
4. Activate: `. venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
3. export FLASK_APP=flaskapp.py

# Run
Via docker-compose:

1. `docker-compose up` from the root level.
2. Migrate the db: `docker-compose run web flask db upgrade`

Locally:
1. Migrate the db (be sure the database name specified in your .env DATABASE_URI exists): `flask db upgrade`
2. Run: `gunicorn -b 0.0.0.0:5000 -w 4 --access-logfile - --error-logfile - flaskapp:app`


The server can be reached at localhost:25000/keys
