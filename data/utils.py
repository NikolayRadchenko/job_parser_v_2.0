from headhunter import HeadHunter
from superjob import SuperJob
from vacancy import Vacancy
from json_saver import JSONSaver
from print_table import print_prettytable_sj, print_prettytable_hhru


def print_operations():
    """
    Метод для отображения вариантов использования приложения пользователем
    """
    print("1. Ввести ключевое слово для поиска;\n"
          "2. Получить топ N вакансий по зарплате;\n"
          "3. Назад.\n")


def print_result_search(platform, res, sorty="id"):
    if f"{platform()}" == "headhunter.ru":
        return print_prettytable_hhru(res, sorty)
    elif f"{platform()}" == "superjob.ru":
        return print_prettytable_sj(res, sorty)


def user_interface():
    """
    Метод для работы с пользователем и получения основной информации от пользователя
    :return:
    """
    global res
    global vacancies

    flag = True
    hh = HeadHunter
    sj = SuperJob
    list_platforms = [hh, sj]
    # Блок приветствия пользователя и получния основной информации от пользователя
    print('Вас приветствует "Парсер вакансий"')
    user_name = input("Как Вас зовут?\n")
    print(f'Здравствуйте, {user_name}')
    while flag:
        platform_choice = input("Где будем искать вакансии?\n"
                                "1. HeadHunter.ru\n"
                                "2. SuperJob.ru\n"
                                "3. Ничего не искать и выйти\n"
                                "--Выберите вариант цифрой--\n")
        if platform_choice in ["1", "2"]:
            platform = list_platforms[int(platform_choice) - 1]
            print(f"Выбран сайт {platform()}\n")

            while True:
                user_choice = input("1. Ввести ключевое слово для поиска;\n"
                                    "2. Получить топ N вакансий по зарплате;\n"
                                    "3. Назад\n"
                                    "--Выберите вариант цифрой--\n")
                if user_choice == '1':
                    search_query = input("Введите поисковый запрос:\n")
                    res = platform().get_search_vacancies(search_query)
                    print(print_result_search(platform, res)[0])
                    vacancies = []
                    for vac in print_result_search(platform, res)[1]:
                        vacancy = Vacancy(vac['id'], vac['name'], vac['salary'], vac['description'], vac['url'])
                        vacancies.append(vacancy)
                    input("Нажмите ENTER, чтобы продолжить!")
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
                    print(print_result_search(platform, res, sorty="Зарплата")[0])
                    input("Нажмите ENTER, чтобы продолжить!\n")
                    break
                elif user_choice == "3":
                    break
                else:
                    print("\nНеверный ввод\n")
                    continue

            # Блок сохранения полученных данных в файл

            filename = "vacancies.json"
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
                    js_file.remove_vacancy([del_vacancy], str(platform()))
                elif user_choice == "0":
                    break
                input("Нажмите ENTER, чтобы продолжить!\n")

        elif platform_choice == "3":
            flag = False
            print(f"До свидания, {user_name}, возвращайтесь!")
        else:
            print("Неверный ввод")
