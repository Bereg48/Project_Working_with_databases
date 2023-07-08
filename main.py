from colorama import Fore, Back

from src.utils import DBManager
from src.config import config
from src.function import get_request, save_vacancies_to_db, parsing_vacancies, create_database


def main():
    keyword = 'Python'  # Ключевое слово поиска на hh.ru
    page = 0  # Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    per_page = 22  # Кол-во вакансий на 1 странице (max 22)
    database_name = 'hh_bd'  # Название БД
    params = config()  # Параметры получающие данные через конфиг из файла database.ini

    # Получение вакансий по keyword.
    hh_vacancies = parsing_vacancies(get_request(keyword, page, per_page))

    # Создание БД database_name с таблицей и колонами.
    create_database(database_name, params)

    # Сохранение полученных вакансий в БД.
    save_vacancies_to_db(database_name, hh_vacancies, params)

    # Экземпляр класса DBManager для работы с данными в БД.
    dbmanager = DBManager(database_name, params)

    print('Приветствую, выберите действие.')

    while True:

        print(Fore.YELLOW + """
        1 - Список работодателей и кол-во вакансий.
        2 - Список вакансий с указанием названия работодателей, вакансий, ЗП и URL на вакансию.
        3 - Средняя ЗП
        4 - Список вакансий, у которых ЗП выше средней.
        5 - Найти вакансии по ключевому слову.
            """)
        user_answer = input(Back.BLACK + 'Ваш выбор: ')

        if user_answer == '1':
            emp_info = dbmanager.get_companies_and_vacancies_count()
            for i in emp_info:
                print(i)

        elif user_answer == '2':
            all_vac = dbmanager.get_all_vacancies()
            for i in all_vac:
                print(i)

        elif user_answer == '3':
            print(f"Средняя ЗП: {dbmanager.get_avg_salary()}")

        elif user_answer == '4':
            vac = dbmanager.get_vacancies_with_higher_salary()
            for item in vac:
                print(item)

        elif user_answer == '5':
            keyword = input('Введите ключевое слово: ')
            vac = dbmanager.get_vacancies_with_keyword(keyword)
            for item in vac:
                print(item)
        else:
            print("Такого варианта нет")

        print("Продолжить?")
        answer = input("Y/N: ").upper()
        if answer == 'N':
            print("!!До новых встреч!!")
            break


if __name__ == '__main__':
    main()
