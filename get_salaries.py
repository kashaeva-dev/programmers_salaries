import os

from dotenv import load_dotenv, find_dotenv

from common import display_salary_table
from headHunter import get_salary_by_language_hh
from superJobs import get_salary_by_language_sj


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
            salaries_by_languages_sj.append(get_salary_by_language_sj(language, token))
            salaries_by_languages_hh.append(get_salary_by_language_hh(language))
        display_salary_table(salaries_by_languages_sj, 'SuperJob Moscow')
        display_salary_table(salaries_by_languages_hh, 'HeadHunter Moscow')


if __name__ == "__main__":
    main()
