from models import db, User, Movie

class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        users = db.session.execute(db.select(User)).scalars()
        return users


    def get_movies(self, user_id):
        movies_by_user = db.session.execute(db.select(Movie).where(Movie.user_id == user_id))
        return movies_by_user


    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()


    def update_movie(self, movie_id, new_title):
        movie = db.get_or_404(Movie, movie_id)
        movie.name = new_title
        db.session.commit()


    def delete_movie(self, movie_id):
        movie = db.get_or_404(Movie, movie_id)
        db.session.delete(movie)
        db.session.commit()
