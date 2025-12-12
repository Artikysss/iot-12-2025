from enum import Enum
from datetime import datetime, date
import sys

class MovieType(Enum):
    ACTION = "boyovick"
    COMEDY = "comedy"
    DRAMA = "drama"
    FANTASY = "fantasy"
    HORROR = "horror"

class Movie:
    def __init__(self, movie_id: int, title: str, movie_type: MovieType, 
                 ranking: float, release_date: str, character_number: int, 
                 ticket_price: float, comment: str):
        self._id = movie_id
        self._title = title
        self._movie_type = movie_type
        self._ranking = ranking
        self._release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        self._character_number = character_number
        self._ticket_price = ticket_price
        self._comment = comment
   
        self._sales_history = {}
        print(f"Construct: film '{self._title}' created.")

    def __del__(self):
        print(f"destrucktor: film '{self._title}' deleted.")

    @property
    def title(self):
        return self._title

    @property
    def movie_type(self):
        return self._movie_type

    @property
    def ranking(self):
        return self._ranking

    @property
    def release_date(self):
        return self._release_date

    @property
    def ticket_price(self):
        return self._ticket_price

    def add_sales(self, day_str: str, quantity: int) -> None:
       sales_date = datetime.strptime(day_str, "%Y-%m-%d").date()
        self._sales_history[sales_date] = self._sales_history.get(sales_date, 0) + quantity  

    def get_sales_for_day(self, day: date) -> int:
        return self._sales_history.get(day, 0)

    def __str__(self):
        return (f"ID: {self._id} | name: {self._title} | genre: {self._movie_type.value} | "
                f"rating: {self._ranking} | Дата: {self._release_date} | "
                f"price: {self._ticket_price} usd")

class Cinema:
    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location
        self._movies = []
        print(f"cinema '{self._name}' open {self._location}.")

    def __del__(self):
        print(f"cinema '{self._name}' closed.")

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def display_schedule(self):
        print(f"\n--- schedule '{self._name}' ---")
        for movie in self._movies:
            print(movie)
        print("-" * 40)

    def calculate_profit(self, movie: Movie, day_str: str):
        target_date = datetime.strptime(day_str, "%Y-%m-%d").date()
        tickets_sold = movie.get_sales_for_day(target_date)
        profit = tickets_sold * movie.ticket_price
        
        print(f"film income '{movie.title}' by {target_date}: {profit} usd ({tickets_sold} tickets).")
        return profit

    def recommend_movie(self, preferred_type: MovieType, min_ranking: float) -> None:
        print(f"\nsearch for films (genre: {preferred_type.value}, rating > {min_ranking})...")
       recommendations = [
            m for m in self._movies
            if m.movie_type == preferred_type and m.ranking >= min_ranking
        ]
        
        if recommendations:
            for movie in recommendations:
                print(f" -> recommend: {movie.title} (rating: {movie.ranking})")
        else:
            print(" -> unfortunately, suggested film not found.")


    def sort_movies_by_date(self):
        print("\nsorting by release...")
        self._movies.sort(key=lambda x: x.release_date) 


def main():
    
    my_cinema = Cinema("Multiplex", "Київ, вул. Хрещатик, 1")

    m1 = Movie(1, "Месники", MovieType.ACTION, 8.5, "2012-05-04", 20, 150.0, "Епічний фільм")
    m2 = Movie(2, "Сам удома", MovieType.COMEDY, 9.0, "1990-11-16", 5, 100.0, "Класика")
    m3 = Movie(3, "Інтерстеллар", MovieType.FANTASY, 9.5, "2014-11-07", 8, 200.0, "Наукова фантастика")
    m4 = Movie(4, "Дюна 2", MovieType.FANTASY, 8.9, "2024-03-01", 15, 250.0, "Новинка")

    my_cinema.add_movie(m1)
    my_cinema.add_movie(m2)
    my_cinema.add_movie(m3)
    my_cinema.add_movie(m4)

    my_cinema.display_schedule()

    my_cinema.sort_movies_by_date()
    my_cinema.display_schedule()

    target_day = "2024-12-12"
    m3.add_sales(target_day, 50) 
    m4.add_sales(target_day, 100)

    print("\n--- income  ---")
    my_cinema.calculate_profit(m3, target_day)
    my_cinema.calculate_profit(m4, target_day)

    my_cinema.recommend_movie(MovieType.FANTASY, 9.ч0)

    print("\nending the program...")

if __name__ == "__main__":
    main()

