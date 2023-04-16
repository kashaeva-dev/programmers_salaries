from itertools import count

import requests


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
