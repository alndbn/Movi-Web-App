from flask import Flask, render_template, request, redirect, url_for
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
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return render_template('users.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        success = data_manager.create_user(name)

        if success:
            return redirect(url_for('list_users'))
        else:
            return f"Error creating user '{name}'. Please try again.", 500


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_list_of_fav_movies(user_id):
    all_users = data_manager.get_users()
    user_movies = data_manager.get_movies_by_user(user_id)
    return render_template('movies.html', users=all_users, current_user_id=user_id, movies=user_movies)



@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_new_fav_movie(user_id):
    title = request.form.get('title')
    year = request.form.get('year')
    data_manager.add_movie(title=title, year=year, user_id=user_id)
    return redirect(url_for('get_list_of_fav_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def change_movie_title(user_id, movie_id):
    new_title = request.form.get('new_title')
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('get_list_of_fav_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_fav_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_list_of_fav_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        try:
            data_manager.create_user(name='TestUser')
            print("First User (TestUser) successfully created.")
        except Exception as e:
            print(f"Error creating test user: {e}")
    app.run(port=8000, debug=True)




