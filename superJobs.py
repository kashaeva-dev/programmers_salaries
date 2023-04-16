from itertools import count
from statistics import mean

import requests

from common import predict_salary


def predict_salary_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    return predict_salary(salary_from, salary_to)


def fetch_vacancies_sj(language, token):
    moscow = 4
    programming = 48
    request_url = 'https://api.superjob.ru/2.0/vacancies'

    headers = {
        'X-Api-App-Id': token,
    }

    params = {
        'town': moscow,
        'keyword': language,
        'catalogues': programming,
        'count': 100,
    }

    vacancies = []
    found = 0

    for page in count():

        params['page'] = page

        page_response = requests.get(request_url, params=params, headers=headers)
        page_response.raise_for_status()
        page_payload = page_response.json()

        vacancies.extend(page_payload['objects'])

        if not page_payload['more']:
            found = page_payload['total']
            break

    return {'vacancies': vacancies, 'found': found}


def get_salary_by_language_sj(languages, token):
    for language in languages:

        vacancies = fetch_vacancies_sj(language, token)
        salaries = []
        for vacancy in vacancies['vacancies']:
            salary = predict_salary_sj(vacancy)
            if salary:
                salaries.append(salary)
        if salaries:
            mean_salary = int(mean(salaries))
        else:
            mean_salary = 'Неизвестно'

        return [
                language,
                vacancies['found'],
                len(salaries),
                mean_salary,
            ]
