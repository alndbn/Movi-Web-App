from flask import Flask
from data_manager import DataManager
from models import db, Movie, User
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()

@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        try:
            data_manager.create_user(name='TestUser')
            print("Erster Benutzer (TestUser) erfolgreich erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Testbenutzers: {e}")
    app.run(debug=True)

#CREATE TABLE users (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name TEXT NOT NULL
#);


