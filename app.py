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

@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def add_new_user(name):
    data_manager.create_user(name)
    return f"New user {name} created."

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_list_of_fav_movies(user_id):
    return str(data_manager.get_movies(user_id))

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_new_fav_movie(movie, user_id):
    movie["user_id"] = user_id
    data_manager.add_movie(movie)
    return f"For this user ID I created this {movie}"

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def change_movie_title(title, user_id, movie_id):
    data_manager.update_movie(movie_id, title)
    return "Successfully updated."


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_fav_movie(user_id, movie_id):
    data_manager.delete_movie(user_id)
    return "Successfully deleted."

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


