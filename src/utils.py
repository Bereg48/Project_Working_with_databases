
from typing import Any

import psycopg2


class DBManager:

    def __init__(self, database_name, params) -> None:
        self.params = params
        self.database_name = database_name

    def _create_table(self):
        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            stars INT,
            forks INT,
            language VARCHAR(255)
            );
            """)

    def get_companies_and_vacancies_count(self) -> list[tuple, Any]:
        """Метод get_companies_and_vacancies_count получает список всех компаний и количество вакансий у каждой
        компании."""
        conn = psycopg2.connect(database=self.database_name, **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT employer_name, COUNT(*) AS vacancies_quantity 
                    FROM vacancies
                    GROUP BY employer_name
                    ORDER BY vacancies_quantity DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """Метод get_all_vacancies получает список всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(database=self.database_name, **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT employer_name, vacancy_name, (salary_from + salary_to) / 2 AS avg_salary, vacancy_url 
                    FROM vacancies
                    ORDER BY avg_salary DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        """Метод get_avg_salary получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(database=self.database_name, **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT  AVG((salary_from + salary_to) / 2) 
                    FROM vacancies
                    """
                )
                result = cur.fetchone()
        conn.close()
        return int(result[0])

    def get_vacancies_with_higher_salary(self):
        """Метод get_vacancies_with_higher_salary получает список всех вакансий, у которых зарплата выше средней по
        всем вакансиям."""
        conn = psycopg2.connect(database=self.database_name, **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, (salary_from + salary_to) / 2 AS salary, vacancy_url  
                    FROM vacancies
                    WHERE (salary_from + salary_to) / 2 > {self.get_avg_salary()}
                    ORDER BY salary DESC
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self):
        """Метод get_vacancies_with_keyword получает список всех вакансий, в названии которых содержатся переданные в
        метод слова, например “python”."""
        conn = psycopg2.connect(database=self.database_name, **self.params)

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, (salary_from + salary_to) / 2 AS salary, vacancy_url  
                    FROM vacancies
                    WHERE vacancy_name LIKE '%{keyword}%'
                    """
                )
                result = cur.fetchall()
        conn.close()
        return result

