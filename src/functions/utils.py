from ..headhunter import HeadHunter
from ..vacancy import Vacancy
from ..dbmanager import DBManager
from .print_table import print_prettytable
from data.config import config
import psycopg2
from data.constants import DB_NAME


def print_operations():
    """
    Метод для отображения вариантов использования приложения пользователем
    """
    print("1. Ввести ключевое слово для поиска;\n"
          "2. Получить топ N вакансий по зарплате;\n"
          "3. Назад.\n")


def parser_start(dbmanager, params, platform, employers_id):
    conn = None
    dbmanager.create_database(params, DB_NAME)
    params.update({'dbname': DB_NAME})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                dbmanager.create_employers_table(cur)
                dbmanager.create_vacancies_table(cur)
                dbmanager.add_employers_data(cur, platform, employers_id)
                conn.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def print_result_search(res, sorty="id"):
    return print_prettytable(res, sorty)


def user_interface():
    """
    Метод для работы с пользователем и получения основной информации от пользователя
    :return:
    """

    global res
    global vacancies

    conn = None
    flag = True
    platform = HeadHunter()
    dbmanager = DBManager()
    params = config()
    favorites_employers_id = ('78638', '1740', '873105', '250', '5390761', '3202769', '2851802', '2180', '3529', '4181')
    parser_start(dbmanager, params, platform, favorites_employers_id)
    for row in dbmanager.get_favorites_employers(params):
        for i in range(len(row)):
            print(row[i])
    # Блок приветствия пользователя и получения основной информации от пользователя
    print('Вас приветствует "Парсер вакансий"')
    user_name = input("Как Вас зовут?\n")
    print(f'Здравствуйте, {user_name}')
    while flag:
        platform_choice = input("Где будем искать вакансии?\n"
                                "1. HeadHunter.ru\n"
                                "3. Ничего не искать и выйти\n"
                                "--Выберите вариант цифрой--\n")
        if platform_choice in ["1"]:
            print(f"Выбран сайт {platform}\n")

            while True:
                user_choice = input("1. Ввести ключевое слово для поиска;\n"
                                    "2. Получить топ N вакансий по зарплате;\n"
                                    "3. Назад\n"
                                    "--Выберите вариант цифрой--\n")
                if user_choice == '1':
                    search_query = input("Введите поисковый запрос:\n")
                    res = platform.get_search_vacancies(search_query)
                    try:
                        with psycopg2.connect(**params) as conn:
                            with conn.cursor() as cur:
                                dbmanager.add_vacancies_data(cur, res)

                                vacancies_with_keyword = dbmanager.get_vacancies_with_keyword(cur)
                                conn.commit()
                                conn.close()
                    except(Exception, psycopg2.DatabaseError) as error:
                        print(error)
                    finally:
                        if conn is not None:
                            conn.close()
                    print(print_result_search(res)[0])
                    vacancies = []
                    for vac in print_result_search(res)[1]:
                        vacancy = Vacancy(vac['id'], vac['name'], vac['salary'], vac['description'], vac['url'])
                        vacancies.append(vacancy)
                    input("Нажмите ENTER, чтобы продолжить!\n")
                    break
                elif user_choice == "2":
                    search_query = input("Введите какую зарплату искать: \n")
                    n_salary = int(input("Сколько получить вакансий по зарплате? \n"))
                    if 0 < int(n_salary) < 100:
                        res = platform().get_search_vacancies(search_query, n_salary)
                    elif int(n_salary) < 0:
                        res = platform().get_search_vacancies(search_query, 10)
                    else:
                        res = platform().get_search_vacancies(search_query, 100)
                    print(print_result_search(res, sorty="Зарплата")[0])
                    input("Нажмите ENTER, чтобы продолжить!\n")
                    break
                elif user_choice == "3":
                    break
                else:
                    print("\nНеверный ввод\n")
                    continue

            # Блок сохранения полученных данных в файл

            filename = "../../data/vacancies.json"
            js_file = JSONSaver(filename)
            file_path = js_file.add_vacancy(res)

            # Блок работы с сохраненными данными

            while True:
                user_choice = input("1 - Посмотреть вакансии\n"
                                    "2 - Удалить вакансию по id\n"
                                    "0 - Назад\n")

                if user_choice == "1":
                    print(js_file.get_vacancies())

                elif user_choice == "2":
                    del_vacancy = input("id вакансии: \n")
                    js_file.remove_vacancy([del_vacancy])
                elif user_choice == "0":
                    break
                input("Нажмите ENTER, чтобы продолжить!\n")

        elif platform_choice == "3":
            flag = False
            print(f"До свидания, {user_name}, возвращайтесь!")
        else:
            print("Неверный ввод")
