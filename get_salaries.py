import os
from statistics import mean

from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable

from fetch_vacancies import fetch_vacancies_hh, fetch_vacancies_sj
from predict_salary import predict_salary_hh, predict_salary_sj


def get_salaries_by_languages(languages, service, token=None):
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
        vacancies = job_search_services[service]['fetch'](language, token)
        salaries = []
        for vacancy in vacancies['vacancies']:
            salary = job_search_services[service]['predict'](vacancy)
            if salary:
                salaries.append(salary)
        if salaries:
            salaries_by_language.append([
                language,
                vacancies['found'],
                len(salaries),
                int(mean(salaries))
            ])
        else:
            salaries_by_language.append([
                language,
                vacancies['found'],
                len(salaries),
                'Неизвестно',
            ])

    return salaries_by_language


def salary_table_output(table_data, table_title):
    headings = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]]
    table_data = headings + table_data
    table_instance = AsciiTable(table_data, table_title)
    print(table_instance.table)
    print()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    token = os.environ['SUPERJOB_KEY']

    languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP',
        'C++', 'C', 'Go', 'Swift', 'TypeScript', '1C',
    ]

    salary_table_output(get_salaries_by_languages(languages, 'sj', token), 'SuperJob Moscow')
