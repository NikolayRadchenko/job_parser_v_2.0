import psycopg2
import json
from data.constants import DB_NAME


class DBManager:
    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self, cur):
        try:
            cur.execute(f"""
                            SELECT * FROM vacancies;
                        """)
            return cur.fetchall()
        except Exception as error:
            print(error)

    def get_favorites_employers(self, params):
        try:
            with psycopg2.connect(**params) as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM employers;""")
                    records = cur.fetchall()
                return records
        except Exception as error:
            print(error)

    def add_employers_data(self, cur, platform, employers_id) -> None:
        """Добавляет данные из suppliers в таблицу suppliers."""
        try:
            for employer_id in employers_id:
                data_json = platform.get_search_employers(employer_id)
                cur.execute(f"""
                                INSERT INTO employers(employer_id, company_name, company_url, open_vacancies, url_hh) 
                                VALUES ('{data_json["id"]}', '{data_json["name"]}', '{data_json["site_url"]}', 
                                '{data_json["open_vacancies"]}', '{data_json["alternate_url"]}');
                            """)
        except Exception as error:
            print(error)

    def add_vacancies_data(self, cur, data_json) -> None:
        """Добавляет данные из suppliers в таблицу suppliers."""
        try:
            for vacancy in data_json['items']:
                cur.execute(f"""
                                INSERT INTO employers(vacancy_id, employer_id, vacancy_name, salary, vacancy_url, description) 
                                VALUES ('{vacancy["id"]}', '{vacancy["employer"]["id"]}', '{vacancy["name"]}', 
                                '{vacancy["salary"]}', '{vacancy["alternate_url"]}', '{vacancy["snippet"]["requirement"]}');
                            """)
        except Exception as error:
            print(error)

    def create_database(self, params, db_name) -> None:
        """Создает новую базу данных."""
        connection = psycopg2.connect(dbname='postgres', **params)
        connection.autocommit = True
        cur = connection.cursor()

        cur.execute(f"""DROP DATABASE {db_name};""")
        cur.execute(f"""CREATE DATABASE {db_name};""")

        connection.commit()
        cur.close()
        connection.close()

    def create_employers_table(self, cur) -> None:
        """Создает таблицу employers."""
        cur.execute("""
                    CREATE TABLE employers(
                        employer_id serial PRIMARY KEY,
                        company_name VARCHAR NOT NULL,
                        open_vacancies VARCHAR,
                        company_url VARCHAR,
                        url_hh VARCHAR
                        );
                    """)

    def create_vacancies_table(self, cur) -> None:
        """Создает таблицу vacancies."""
        cur.execute("""
                    CREATE TABLE vacancies(
                        vacancy_id int PRIMARY KEY,
                        employer_id int NOT NULL,
                        vacancy_name VARCHAR,
                        salary VARCHAR,
                        vacancy_url VARCHAR,
                        description VARCHAR
                        );
                    """)

    def add_foreign_keys(self, cur) -> None:
        """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
        cur.execute(f"""
                        ALTER TABLE ONLY products
                        ADD CONSTRAINT fk_products_suppliers FOREIGN KEY(supplier_id) REFERENCES suppliers;
                    """)
