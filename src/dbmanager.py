import psycopg2


class DBManager:
    def get_companies_and_vacancies_count(self, cur):
        """
        Метод для получения компаний и количества открытых вакансий у каждой компании
        """
        try:
            cur.execute(f"""
                            SELECT company_name, open_vacancies FROM employers;
                        """)
            return cur.fetchall()
        except Exception as error:
            print(error)

    def get_all_vacancies(self, cur):
        """
        Метод для получения всех вакансий
        """
        try:
            cur.execute(f"""
                            SELECT * FROM vacancies;
                        """)
            return cur.fetchall()
        except Exception as error:
            print(error)

    def get_avg_salary(self, cur):
        """
        Метод для нахождения средней зарплаты в вакансиях
        """
        try:
            cur.execute(f"""
                            SELECT AVG(salary::INTEGER) FROM vacancies
                            WHERE salary <> 'Не указана' AND salary <> 'None';
                        """)
            return cur.fetchall()
        except Exception as error:
            print(error)

    def get_vacancies_with_higher_salary(self, cur, n):
        """
        Метод для поиска вакансий по зарплате
        """
        try:
            cur.execute(f"""
                            SELECT * FROM vacancies
                            WHERE salary NOT IN ('Не указана', 'None')
	                        AND (salary::INTEGER > (SELECT AVG(salary::INTEGER) FROM vacancies
	                        WHERE salary <> 'Не указана' AND salary <> 'None'))
	                        ORDER BY salary::INTEGER DESC
	                        LIMIT {n};
                        """)
            return cur.fetchall()
        except Exception as error:
            print(error)

    def get_vacancies_with_keyword(self, cur, keyword):
        """
        Метод для поиска вакансий по ключевому слову
        """
        try:
            cur.execute(f"""
                            SELECT * FROM vacancies
                            WHERE LOWER(vacancy_name) LIKE '%{keyword.lower()}%';
                        """)
            return cur.fetchall()
        except Exception as error:
            print(error)

    def get_favorites_employers(self, params):
        """
        Метод для получения избранных работодателей
        """
        try:
            with psycopg2.connect(**params) as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM employers;""")
                    records = cur.fetchall()
                return records
        except Exception as error:
            print(error)

    def add_employers_data(self, cur, *args) -> None:
        """Добавляет данные из suppliers в таблицу suppliers."""
        try:
            cur.execute(f"""
                            INSERT INTO employers(employer_id, company_name, company_url, open_vacancies, url_hh) 
                            VALUES (%s, %s, %s, %s, %s);
                            """, *args)
        except Exception as error:
            print(error)

    def add_vacancies_data(self, cur, *args) -> None:
        """Добавляет данные из suppliers в таблицу suppliers."""
        try:
            cur.execute(f"""
                            INSERT INTO vacancies(vacancy_id, employer_id, vacancy_name, salary, vacancy_url, description) 
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """, *args)
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
        try:
            cur.execute("""
                        CREATE TABLE employers(
                            employer_id serial PRIMARY KEY,
                            company_name VARCHAR NOT NULL,
                            open_vacancies VARCHAR,
                            company_url VARCHAR,
                            url_hh VARCHAR
                            );
                        """)
        except Exception as error:
            print(error)


    def create_vacancies_table(self, cur) -> None:
        """Создает таблицу vacancies."""
        try:
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
        except Exception as error:
            print(error)

    def add_foreign_keys(self, cur) -> None:
        """Добавляет foreign key со ссылкой на employer_id в таблицу vacancies."""
        try:
            cur.execute(f"""
                            ALTER TABLE ONLY vacancies
                            ADD CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers;
                        """)
        except Exception as error:
            print(error)

