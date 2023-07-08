import json
from hh_api import HeadHunterAPI
import psycopg2


class DBManager:
    @staticmethod
    def get_companies_and_vacancies_count():
        """
        Функция получает список всех компаний и количество вакансий у каждой компании.
        """
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT company_id, COUNT(*)
                FROM vacancies
                GROUP BY company_id;
                """)
                return cur.fetchall()

    @staticmethod
    def get_all_vacancies():
        """
        Функция получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        """
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT companies.company_name,
                 vacancies.title,
                  vacancies.salary_from,
                   vacancies.salary_to,
                    vacancies.url
                from vacancies
                JOIN companies ON companies.company_id=vacancies.company_id
                """)
                return cur.fetchall()

    @staticmethod
    def get_avg_salary():
        """
        Функция получает среднюю зарплату по вакансиям.
        """
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT ROUND(AVG(salary_from + salary_to) / 2)
                as middle_salary
                FROM vacancies
                """)
                return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT *
                FROM vacancies
                WHERE salary_to > %s
                """, self.get_avg_salary())
                return cur.fetchall()

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT *
                FROM vacancies
                WHERE title LIKE %s
                """,
                            ('%' + keyword + '%',)
                            )
                result = cur.fetchall()
                return result

    @staticmethod
    def create_table():
        """
        Функция для создания таблицы хранящей в себе данные о работодателе
        и таблицы хранящей в себе данные о вакансиях
        """
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                company_id INT PRIMARY KEY,
                company_name TEXT NOT NULL,
                url VARCHAR(100)
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INT PRIMARY KEY,
                title TEXT NOT NULL,
                company_id INT REFERENCES companies(company_id) ON DELETE CASCADE,
                salary_from INT,
                salary_to INT,
                url VARCHAR(100) NOT NULL
                )
                """)
                conn.commit()

    @staticmethod
    def add_companies(id_company):
        """
        Функция для заполнения данными таблицы "companies"
        """
        hh = HeadHunterAPI()
        for i in id_company:
            company = hh.get_company_info(i)
            data = {
                'id': company['id'],
                "name_company": company['name'],
                'url': company['alternate_url']
            }
            with psycopg2.connect(
                    host='localhost',
                    database='head_hunter',
                    user='postgres',
                    password=''
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(' INSERT INTO companies VALUES (%s, %s, %s)',
                                (data['id'],
                                 data['name_company'],
                                 data['url']))
                    conn.commit()
        conn.close()

    @staticmethod
    def add_vacancies(id_company):
        """
        Функция для заполнения таблицы "vacancies"
        """
        hh = HeadHunterAPI()
        for i in id_company:
            vacancies = hh.get_vacancies_info(i)
            for vac in vacancies['items']:
                data = {
                    'id': vac['id'],
                    "name_vacancy": vac['name'],
                    'company_id': vac['employer']['id'],
                    'salary_to': vac['salary']['to'],
                    'salary_from': vac['salary']['from'],
                    'url': vac['alternate_url']
                }
                with psycopg2.connect(
                        host='localhost',
                        database='head_hunter',
                        user='postgres',
                        password=''
                ) as conn:
                    with conn.cursor() as cur:
                        cur.execute(' INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)',
                                    (data['id'],
                                     data['name_vacancy'],
                                     data['company_id'],
                                     data['salary_to'],
                                     data['salary_from'],
                                     data['url']))
                        conn.commit()
        conn.close()

    @staticmethod
    def drop_table():
        with psycopg2.connect(
                host='localhost',
                database='head_hunter',
                user='postgres',
                password=''
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                DROP TABLE IF EXISTS vacancies
                """)
                cur.execute("""
                DROP TABLE IF EXISTS companies
                """)
                conn.commit()

    @staticmethod
    def file_with_id_company():
        """
        Функция для открытия файла со списком id интересующих нас компаний
        """
        with open('company_id.json', 'r') as file:
            data = json.load(file)
            return data
