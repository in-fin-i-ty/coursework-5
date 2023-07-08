--- sql-запрос, который получает список всех компаний и количество вакансий у каждой компании.
SELECT company_id, COUNT(*)
FROM vacancies
GROUP BY company_id
--- sql-запрос, который получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT companies.company_name,
vacancies.title,
vacancies.salary_from,
vacancies.salary_to,
vacancies.url
from vacancies
JOIN companies ON companies.company_id=vacancies.company_id
--- sql-запрос, который получает среднюю зарплату по вакансиям.
SELECT ROUND(AVG(salary_from + salary_to) / 2)
as middle_salary
FROM vacancies
--- sql-запрос, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT *
FROM vacancies
WHERE salary_to > %s
--- sql-запрос, который получает список всех вакансий, в названии которых содержатся переданные в метод слова
SELECT *
FROM vacancies
WHERE title LIKE %s
--- sql-запрос на создание таблицы с данными о работодателе
CREATE TABLE IF NOT EXISTS companies (
company_id INT PRIMARY KEY,
company_name TEXT NOT NULL,
url VARCHAR(100)
--- sql-запрос на создание таблицы с данными о вакансиях
CREATE TABLE IF NOT EXISTS vacancies (
vacancy_id INT PRIMARY KEY,
title TEXT NOT NULL,
company_id INT REFERENCES companies(company_id) ON DELETE CASCADE,
salary_from INT,
salary_to INT,
url VARCHAR(100) NOT NULL
--- sql-запрос на заполнение данными таблицы о работодателях
INSERT INTO companies VALUES (%s, %s, %s)
--- sql-запрос на заполнение данными таблицы о вакансиях
INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)