from models import db, User, Movie
from sqlalchemy.exc import IntegrityError

class DataManager():
    def create_user(self, name):
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"ERROR: User '{name}' could not be created due to a database integrity error.")
            return False
        except Exception as e:
            db.session.rollback()
            print(f"An unexpected error occurred during user creation: {e}")
            return False
        return True


    def get_users(self):
        users = db.session.execute(db.select(User)).scalars()
        return users


    def get_movies_by_user(self, user_id):
        movies_by_user = db.session.execute(db.select(Movie).where(Movie.user_id == user_id)).scalars()
        return movies_by_user


    def add_movie(self, title, year, user_id):
        new_movie = Movie(title=title, year=year, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()


    def update_movie(self, movie_id, new_title):
        movie = db.get_or_404(Movie, movie_id)
        movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id):
        movie = db.get_or_404(Movie, movie_id)
        db.session.delete(movie)
        db.session.commit()
