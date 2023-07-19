from ..headhunter import HeadHunter
from ..dbmanager import DBManager
from .print_table import print_prettytable, print_prettytable_avg_salary, print_prettytable_company
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
    """
    Метод для создания базы данных и таблиц vacancies и employers
    """
    vacancies = {}
    conn = None
    dbmanager.create_database(params, DB_NAME)
    params.update({'dbname': DB_NAME})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                dbmanager.create_employers_table(cur)
                dbmanager.create_vacancies_table(cur)
                for employer_id in employers_id:
                    vacancies[f'{employer_id}'] = (platform.get_vacancies(employer_id)['items'])
                for employer_id in employers_id:
                    data_employer = platform.get_employer_data(platform.get_employers(employer_id))
                    dbmanager.add_employers_data(cur, data_employer)
                for key, vacancy in vacancies.items():
                    for item in platform.get_vacancy_data(vacancy):
                        dbmanager.add_vacancies_data(cur, item)
                dbmanager.add_foreign_keys(cur)
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
    flag = True
    platform = HeadHunter()
    dbmanager = DBManager()
    params = config()
    favorites_employers_id = ('78638', '1740', '873105', '250', '5390761', '3202769', '2851802', '2180', '3529', '4181')
    parser_start(dbmanager, params, platform, favorites_employers_id)
    print('Вас приветствует "Парсер вакансий"')
    user_name = input("Как Вас зовут?\n")
    print(f'Здравствуйте, {user_name}')
    while flag:
        user_choice = input("1. Показать все вакансии избранных работодателей;\n"
                            "2. Ввести ключевое слово для поиска вакансий;\n"
                            "3. Получить топ N вакансий по зарплате;\n"
                            "4. Получить среднюю зарплату по вакансиям;\n"
                            "5. Получить количество открытых вакансий по компаниям;\n"
                            "6. Выход\n"
                            "--Выберите вариант цифрой--\n")
        if user_choice == '1':
            try:
                with psycopg2.connect(**params) as conn:
                    with conn.cursor() as cur:
                        vacancies = dbmanager.get_all_vacancies(cur)
                        print(print_result_search(vacancies))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        elif user_choice == '2':
            try:
                with psycopg2.connect(**params) as conn:
                    with conn.cursor() as cur:
                        keyword = input("Введите поисковый запрос:\n")
                        vacancies = dbmanager.get_vacancies_with_keyword(cur, keyword)
                        print(print_result_search(vacancies))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        elif user_choice == '3':
            try:
                with psycopg2.connect(**params) as conn:
                    with conn.cursor() as cur:
                        n_salary = int(input("Введите сколько показать вакансий:\n"))
                        vacancies = dbmanager.get_vacancies_with_higher_salary(cur, n_salary)
                        print(print_result_search(vacancies, sorty="Зарплата"))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        elif user_choice == '4':
            try:
                with psycopg2.connect(**params) as conn:
                    with conn.cursor() as cur:
                        print(print_prettytable_avg_salary(dbmanager.get_avg_salary(cur)))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        elif user_choice == '5':
            try:
                with psycopg2.connect(**params) as conn:
                    with conn.cursor() as cur:
                        print(print_prettytable_company(dbmanager.get_companies_and_vacancies_count(cur)))
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        elif user_choice == "6":
            flag = False
            print(f"До свидания, {user_name}, возвращайтесь!")
        else:
            print("\nНеверный ввод\n")
            continue
