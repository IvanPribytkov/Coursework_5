import requests


def get_companies():
    """Получает список компаний и их ID."""
    companies_data = {
        'Тинькофф': 78638,
        'Яндекс': 1740,
        'Билайн': 4934,
        'Сбербанк': 1473866,
        'Банк ВТБ': 4181,
        'Газпромнефть': 39305,
        'Альфа-банк': 80,
        'СберТех': 3529,
        'ФинТех IQ': 5898393,
        'Айтеко': 872178
    }

    data = []
    for company_name, company_id in companies_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {'company_id': company_id, 'company_name': company_name, 'company_url': company_url}
        data.append(company_info)

    return data


def get_vacancies(data):
    """Получает информацию о вакансиях для каждой компании."""
    vacancies_info = []
    for company_data in data:
        company_id = company_data['company_id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()['items']
            vacancies_info.extend(vacancies)
        else:
            print(f"Ошибка при запросе к API для компании {company_data['company_name']}: {response.status_code}")
    return vacancies_info


def get_vacancies_list(data):
    """Формирует список словарей с данными для БД."""
    vacancies = []
    for item in data:
        company_id = item['employer']['id']
        company_name = item['employer']['name']
        company_url = item['employer']['url']
        job_title = item['name']
        link_to_vacancy = item['alternate_url']
        salary = item['salary']
        currency = salary['currency'] if salary else ''
        salary_from = salary['from'] if salary and salary['from'] else 0
        description = item['snippet']['responsibility']
        requirement = item['snippet']['requirement']

        vacancies.append({
            "company_id": company_id,
            "company_name": company_name,
            "company_url": company_url,
            "job_title": job_title,
            "link_to_vacancy": link_to_vacancy,
            "salary_from": salary_from,
            "currency": currency,
            "description": description,
            "requirement": requirement
        })
    return vacancies
