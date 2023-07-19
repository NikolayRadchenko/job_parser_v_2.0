-- Команда для вывода колонок company_name и open_vacancies из таблицы employers
SELECT company_name, open_vacancies FROM employers;

-- Команда для вывода таблицы vacancies
SELECT * FROM vacancies;

-- Команда для вывода средней зарплаты из таблицы vacancies
SELECT AVG(salary::INTEGER) FROM vacancies
WHERE salary <> 'Не указ' AND salary <> 'None';

-- Команда для вывода вакансий из таблицы vacancies по параметрам от пользователя
SELECT * FROM vacancies
WHERE salary NOT IN ('Не указ', 'None')
AND (salary::INTEGER > (SELECT AVG(salary::INTEGER) FROM vacancies
WHERE salary <> 'Не указ' AND salary <> 'None'))
ORDER BY salary::INTEGER DESC
LIMIT {n};

-- Команда для поиска вакансий по параметрам
SELECT * FROM vacancies
WHERE LOWER(vacancy_name) LIKE '%{keyword.lower()}%';

-- Команда для вывода таблицы employers
SELECT * FROM employers;

-- Команда для заполнения таблицы employers
INSERT INTO employers(employer_id, company_name, company_url, open_vacancies, url_hh)
VALUES ('{data_json["id"]}', '{data_json["name"]}', '{data_json["site_url"]}',
        '{data_json["open_vacancies"]}', '{data_json["alternate_url"]}');

-- Команда для заполнения таблицы vacancies
INSERT INTO vacancies(vacancy_id, employer_id, vacancy_name, salary, vacancy_url, description)
VALUES ('{vacancy["id"]}', '{vacancy["employer_id"]}', '{vacancy["name"]}',
        '{vacancy["salary"][:-3]}', '{vacancy["url"]}', '{vacancy["description"]}');

-- Команда для удаления и создания базы данных
DROP DATABASE {db_name};
CREATE DATABASE {db_name};

-- Команда для создания таблицы employers
CREATE TABLE employers(
                       employer_id serial PRIMARY KEY,
                       company_name VARCHAR NOT NULL,
                       open_vacancies VARCHAR,
                       company_url VARCHAR,
                       url_hh VARCHAR
                       );

-- Команда для создания таблицы vacancies
CREATE TABLE vacancies(
                       vacancy_id int PRIMARY KEY,
                       employer_id int NOT NULL,
                       vacancy_name VARCHAR,
                       salary VARCHAR,
                       vacancy_url VARCHAR,
                       description VARCHAR
                       );

-- Команда для создания foreign key между таблицей vacancies и employers
ALTER TABLE ONLY vacancies
ADD CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers;