from itertools import count

import requests


def fetch_vacancies_hh(page, language):
    request_url = "https://api.hh.ru/vacancies"

    page = 0

    params = {
        'area': '1',
        'text': f'программист {language}',
        'period': 30,
        'page': page,
    }

    vacancies = []
    found = 0

    for page in count():
        page_response = requests.get(request_url, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()

        vacancies.extend(page_payload['items'])

        if page >= page_payload['pages']:
            found = page_payload['found']
            break

    return [vacancies, found]
