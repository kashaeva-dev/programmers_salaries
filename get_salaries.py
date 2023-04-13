import os
from statistics import mean

from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable

from fetch_vacancies import fetch_vacancies_hh, fetch_vacancies_sj
from predict_salary import predict_salary_hh, predict_salary_sj


def get_salaries_by_languages(languages, service):
    job_search_services = {
        'hh': {
            'fetch': fetch_vacancies_hh,
            'predict': predict_salary_hh,
        },
        'sj': {
            'fetch': fetch_vacancies_sj,
            'predict': predict_salary_sj,
        },
    }
    salaries_by_language = []

    for language in languages:
        vacancies = job_search_services[service]['fetch'](language)
        salaries = []
        for vacancy in vacancies['vacancies']:
            salary = job_search_services[service]['predict'](vacancy)
            if salary:
                salaries.append(salary)
        salaries_by_language.append([
            language,
            vacancies['found'],
            len(salaries),
            int(mean(salaries))
        ])

    return salaries_by_language

