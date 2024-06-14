import psycopg2

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
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS employers ('
                f'company_id INT PRIMARY KEY, '
                f'company_name VARCHAR(100), '
                f'company_url VARCHAR(100))'
            )
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS vacancies ('
                f'company_name VARCHAR(100), '
                f'job_title VARCHAR(100), '
                f'link_to_vacancy VARCHAR(100), '
                f'salary_from INT, '
                f'currency VARCHAR(10), '
                f'description TEXT, '
                f'requirement TEXT)'
            )
        conn.commit()
        conn.close()

        return "База данных и таблицы успешно созданы."

    except Exception as e:
        return f"Произошла ошибка: {e}"

def insert_data(conn, vacancies):
    """Сохранение данных о компаниях и вакансиях в БД PostgreSQL."""
    insert_query_vacancies = """
    INSERT INTO vacancies (company_name, job_title, link_to_vacancy, salary_from, currency, description, requirement)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    insert_query_employers = """
    INSERT INTO employers (company_id, company_name, company_url)
    VALUES (%s, %s, %s) ON CONFLICT (company_id) DO NOTHING
    """
    with conn.cursor() as cur:
        for record in vacancies:
            cur.execute(
                insert_query_employers,
                (record['company_id'], record['company_name'], record['company_url'])
            )
            cur.execute(
                insert_query_vacancies,
                (
                    record['company_name'], record['job_title'], record['link_to_vacancy'],
                    record['salary_from'], record['currency'], record['description'], record['requirement']
                )
            )
        conn.commit()
        conn.close()
