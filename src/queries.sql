-- Создание БД, если она уже создана, тогда удалить её и создать заново.

DROP DATABASE IF EXISTS head_hunter_bd;
CREATE DATABASE head_hunter_bd

-- Создаем таблицу по работодателям
--создаем таблицу по вакансиям

CREATE TABLE IF NOT EXISTS vacancies
(
vacancy_id int PRIMARY KEY,
vacancy_name varchar(200),
vacancy_city varchar(100),
salary_from int,
salary_to int,
vacancy_url varchar(100),
employer_id int,
employer_name varchar(100),
employer_url varchar(100)
);