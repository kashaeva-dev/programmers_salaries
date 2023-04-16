import os
from statistics import mean

from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable

from fetch_vacancies import fetch_vacancies_hh, fetch_vacancies_sj
from predict_salary import predict_salary_hh, predict_salary_sj


def get_salary_by_language_sj(languages, token):
    salary_by_language = []

    for language in languages:

        vacancies = fetch_vacancies_sj(language, token)
        salaries = []
        for vacancy in vacancies['vacancies']:
            salary = predict_salary_sj(vacancy)
            if salary:
                salaries.append(salary)
        if salaries:
            salary_by_language.append([
                language,
                vacancies['found'],
                len(salaries),
                int(mean(salaries)),
            ])
        else:
            salary_by_language.append([
                language,
                vacancies['found'],
                len(salaries),
                'Неизвестно',
            ])

    return salary_by_language


def get_salary_by_language_hh(language):
    salary_by_language = []
    vacancies = fetch_vacancies_hh(language)
    salaries = []
    for vacancy in vacancies['vacancies']:
        salary = predict_salary_hh(vacancy)
        if salary:
            salaries.append(salary)
    if salaries:
        salary_by_language.append([
            language,
            vacancies['found'],
            len(salaries),
            int(mean(salaries)),
        ])
    else:
        salary_by_language.append([
            language,
            vacancies['found'],
            len(salaries),
            'Неизвестно',
        ])

    return salary_by_language


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


def main():
    languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP',
        'C++', 'C', 'Go', 'Swift', 'TypeScript', '1C',
    ]
    try:
        load_dotenv(find_dotenv())
        token = os.environ['SUPERJOB_KEY']
    except KeyError:
        print('Не получается найти переменную окружения SUPERJOB_KEY')
    else:
        salaries_by_languages_sj = []
        salaries_by_languages_hh = []
        for language in languages:
            salaries_by_languages_sj += get_salary_by_language_sj(language, token)
            salaries_by_languages_hh += get_salary_by_language_hh(language)
        salary_table_output(salaries_by_languages_sj, 'SuperJob Moscow')
        salary_table_output(salaries_by_languages_hh, 'HeadHunter Moscow')


if __name__ == "__main__":
    main()
