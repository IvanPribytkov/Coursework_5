import psycopg2
from db_manager import DBManager
from config import config
from get_vacancy import get_companies, get_vacancies, get_vacancies_list
from database import create_db, insert_data


def main():
    params = config()

    # Получаем данные о компаниях и их вакансиях
    companies_data = get_companies()
    vacancies_data = get_vacancies(companies_data)
    vacancies_list = get_vacancies_list(vacancies_data)

    # Создаем базу данных и таблицы
    create_db('best_vacancies', params)

    # Подключаемся к базе данных и вставляем данные
    conn = psycopg2.connect(dbname='best_vacancies', **params)
    insert_data(conn, vacancies_list)

    # Инициализация менеджера базы данных
    db_manager = DBManager("best_vacancies", params)

    while True:
        print(
            "Выберите запрос либо введите слово 'стоп': \n"
            "1 - Список всех компаний и количество вакансий у каждой компании\n"
            "2 - Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
            "3 - Средняя зарплата по вакансиям\n"
            "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
            "5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
        )

        user_request = input()

        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for company, count in companies_vacancies_count.items():
                print(f"{company}: {count}")
        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print("Список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию:")
            for vacancy in vacancy_list:
                print(vacancy)
        elif user_request == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}")
        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям:")
            for vacancy in vacancies_with_higher_salary:
                print(vacancy)
        elif user_request == '5':
            user_input = input("Введите слово: ")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"Список всех вакансий, в названии которых содержатся '{user_input}':")
            for vacancy in vacancies_with_keyword:
                print(vacancy)
        elif user_request.lower() == 'стоп':
            break
        else:
            print("Введён неверный запрос")

    db_manager.close()


if __name__ == "__main__":
    main()
