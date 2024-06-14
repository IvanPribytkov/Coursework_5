import psycopg2
from get_vacancy import get_vacancies, get_companies, get_vacancies_list

data = get_vacancies(get_companies())
vacancies = get_vacancies_list(data)


def create_db(name, params):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {name}')
        cur.execute(f'CREATE DATABASE {name}')
        conn.close()

        conn = psycopg2.connect(dbname=name, **params)
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS employers '
                        f'(company_id int, company_name varchar(100), company_url varchar (100))')
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS vacancies (company_name varchar (100), job_title varchar(100), '
                        f'link_to_vacancy varchar(100), salary_from int, currency varchar(10), '
                        f'description text, requirement text)')
        conn.commit()
        conn.close()

        return "База данных и таблицы успешно созданы."

    except Exception as e:
        return f"Произошла ошибка: {e}"


def insert_data(conn, info: str):
    """Сохранение данных о компаниях и вакансиях в БД pgAdmin."""

    insert_query = """
    INSERT INTO vacancies (company_name, job_title, link_to_vacancy, salary_from, currency, description, requirement)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with conn.cursor() as cur:
        for record in vacancies:
            cur.execute(
                """
                INSERT INTO employers (company_id, company_name, company_url) VALUES (%s, %s, %s)
                """,
                (record['company_id'], record['company_name'], record['company_url']))
            cur.execute(insert_query, (record['company_name'], record['job_title'], record['link_to_vacancy'],
                                       record['salary_from'], record['currency'], record['description'],
                                       record['requirement']))
        conn.commit()
        conn.close()