import os
import requests
from models import db, User, Movie
from sqlalchemy.exc import IntegrityError


OMDB_API_KEY = os.getenv("OMDB_API_KEY")


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
        return db.session.execute(db.select(User)).scalars().all()


    def get_movies_by_user(self, user_id):
        return db.session.execute(db.select(Movie).where(Movie.user_id == user_id)).scalars().all()


    def fetch_movie_data(self, title, year):
        url = "http://www.omdbapi.com/"
        params = {
            "apikey": os.getenv("OMDB_API_KEY"),
            "t": title,
            "y": year
        }

        response = requests.get(url, params=params)
        data = response.json()  # ← GANZ WICHTIG: ()

        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": int(data.get("Year")),
                "director": data.get("Director"),
                "poster_url": data.get("Poster")
            }

        return None

    def add_movie(self, title, year, user_id):
        movie_data = self.fetch_movie_data(title, year)

        if movie_data:
            new_movie = Movie(
                title=movie_data["title"],
                year=movie_data["year"],
                director=movie_data["director"],
                poster_url=movie_data["poster_url"],
                user_id=user_id
            )
        else:
            new_movie = Movie(
                title=title,
                year=year,
                director="Unknown",
                poster_url="https://via.placeholder.com/300x450?text=No+Poster",
                user_id=user_id
            )

        try:
            db.session.add(new_movie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def update_movie(self, movie_id, new_title):
        movie = db.get_or_404(Movie, movie_id)
        movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id):
        movie = db.get_or_404(Movie, movie_id)
        db.session.delete(movie)
        db.session.commit()
