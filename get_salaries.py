from statistics import mean

from fetch_vacancies import fetch_vacancies_hh
from predict_salary import predict_salary_hh


def get_salaries_by_languages(languages):
    salaries_by_language = []

    for language in languages:
        vacancies = fetch_vacancies_hh(language)
        salaries = []
        for vacancy in vacancies['vacancies']:
            salary = predict_salary_hh(vacancy)
            if salary:
                salaries.append(salary)
        salaries_by_language.append([
            language,
            vacancies['found'],
            len(salaries),
            int(mean(salaries))
        ])

    return salaries_by_language

