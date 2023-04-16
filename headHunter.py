from itertools import count
from statistics import mean

import requests

from common import predict_salary


def predict_salary_hh(vacancy):
    salary = vacancy['salary']
    if not salary or salary['currency'] != 'RUR':
        return None
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']
    return predict_salary(salary_from, salary_to)


def fetch_vacancies_hh(language):
    moscow = '1'
    days = 30
    request_url = "https://api.hh.ru/vacancies"

    params = {
        'area': moscow,
        'text': f'программист {language}',
        'period': days,
    }

    vacancies = []
    found = 0

    for page in count():
        params['page'] = page
        page_response = requests.get(request_url, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()

        vacancies.extend(page_payload['items'])

        if page >= page_payload['pages']:
            found = page_payload['found']
            break

    return {'vacancies': vacancies, 'found': found}


def get_salary_by_language_hh(language):
    vacancies = fetch_vacancies_hh(language)
    salaries = []
    for vacancy in vacancies['vacancies']:
        salary = predict_salary_hh(vacancy)
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
