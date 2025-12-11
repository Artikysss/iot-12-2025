from enum import Enum
from datetime import datetime, date
import sys

# 1. Enum для жанрів фільмів
class MovieType(Enum):
    ACTION = "Бойовик"
    COMEDY = "Комедія"
    DRAMA = "Драма"
    FANTASY = "Фентезі"
    HORROR = "Жахи"

# 2. Клас Movie
class Movie:
    def __init__(self, movie_id: int, title: str, movie_type: MovieType, 
                 ranking: float, release_date: str, character_number: int, 
                 ticket_price: float, comment: str):
        """Конструктор класу Movie"""
        self._id = movie_id
        self._title = title
        self._movie_type = movie_type
        self._ranking = ranking
        # Конвертуємо рядок у об'єкт дати (формат РРРР-ММ-ДД)
        self._release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        self._character_number = character_number
        self._ticket_price = ticket_price
        self._comment = comment
        
        # Словник для збереження продажів квитків: {дата: кількість_проданих}
        # Це потрібно для функції calculateProfit
        self._sales_history = {}
        print(f"Конструктор: Фільм '{self._title}' створено.")

    def __del__(self):
        """Деструктор класу Movie"""
        # У Python деструктор викликається при збірці сміття
        print(f"Деструктор: Фільм '{self._title}' видалено з пам'яті.")

    # --- Функції доступу (Getters & Setters) ---
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
    
    # --- Методи ---
    def add_sales(self, day: str, quantity: int):
        """Метод для імітації продажу квитків на певну дату"""
        sales_date = datetime.strptime(day, "%Y-%m-%d").date()
        if sales_date in self._sales_history:
            self._sales_history[sales_date] += quantity
        else:
            self._sales_history[sales_date] = quantity

    def get_sales_for_day(self, day: date) -> int:
        """Повертає кількість проданих квитків за день"""
        return self._sales_history.get(day, 0)

    def __str__(self):
        """Виведення інформації на екран"""
        return (f"ID: {self._id} | Назва: {self._title} | Жанр: {self._movie_type.value} | "
                f"Рейтинг: {self._ranking} | Дата: {self._release_date} | "
                f"Ціна: {self._ticket_price} грн")

# 3. Клас Cinema
class Cinema:
    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location
        self._movies = [] # Список фільмів
        print(f"Кінотеатр '{self._name}' відкрито за адресою {self._location}.")

    def __del__(self):
        print(f"Кінотеатр '{self._name}' зачинено.")

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def display_schedule(self):
        print(f"\n--- Афіша кінотеатру '{self._name}' ---")
        for movie in self._movies:
            print(movie)
        print("-" * 40)

    # Функція підрахунку прибутку (Movie*, day)
    def calculate_profit(self, movie: Movie, day_str: str):
        target_date = datetime.strptime(day_str, "%Y-%m-%d").date()
        tickets_sold = movie.get_sales_for_day(target_date)
        profit = tickets_sold * movie.ticket_price
        
        print(f"Прибуток фільму '{movie.title}' за {target_date}: {profit} грн ({tickets_sold} квитків).")
        return profit

    # Метод вибору фільму за параметрами (наприклад: жанр та мінімальний рейтинг)
    def recommend_movie(self, preferred_type: MovieType, min_ranking: float):
        print(f"\nПошук фільмів (Жанр: {preferred_type.value}, Рейтинг > {min_ranking})...")
        found = False
        for movie in self._movies:
            if movie.movie_type == preferred_type and movie.ranking >= min_ranking:
                print(f" -> Рекомендуємо: {movie.title} (Рейтинг: {movie.ranking})")
                found = True
        if not found:
            print(" -> На жаль, підходящих фільмів не знайдено.")

    # Сортування фільмів за датою випуску
    def sort_movies_by_date(self):
        print("\nСортування фільмів за датою релізу...")
        # Використовуємо lambda функцію для доступу до дати
        self._movies.sort(key=lambda x: x.release_date) 

# 4. Метод Main
def main():
    # Створення об'єкту кінотеатру
    my_cinema = Cinema("Multiplex", "Київ, вул. Хрещатик, 1")

    # Створення фільмів
    m1 = Movie(1, "Месники", MovieType.ACTION, 8.5, "2012-05-04", 20, 150.0, "Епічний фільм")
    m2 = Movie(2, "Сам удома", MovieType.COMEDY, 9.0, "1990-11-16", 5, 100.0, "Класика")
    m3 = Movie(3, "Інтерстеллар", MovieType.FANTASY, 9.5, "2014-11-07", 8, 200.0, "Наукова фантастика")
    m4 = Movie(4, "Дюна 2", MovieType.FANTASY, 8.9, "2024-03-01", 15, 250.0, "Новинка")

    # Додавання фільмів у кінотеатр
    my_cinema.add_movie(m1)
    my_cinema.add_movie(m2)
    my_cinema.add_movie(m3)
    my_cinema.add_movie(m4)

    # Виведення початкового списку
    my_cinema.display_schedule()

    # Сортування за датою та виведення оновленого списку
    my_cinema.sort_movies_by_date()
    my_cinema.display_schedule()

    # Імітація продажів квитків для підрахунку прибутку
    target_day = "2024-12-12"
    m3.add_sales(target_day, 50) # Продали 50 квитків на Інтерстеллар
    m4.add_sales(target_day, 100) # Продали 100 квитків на Дюну

    # Підрахунок прибутку
    print("\n--- Фінансовий звіт ---")
    my_cinema.calculate_profit(m3, target_day)
    my_cinema.calculate_profit(m4, target_day)

    # Вибір фільму за критеріями
    my_cinema.recommend_movie(MovieType.FANTASY, 9.0)

    print("\nЗавершення роботи програми...")

if __name__ == "__main__":
    main()
