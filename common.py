from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None


def display_salary_table(salaries, table_title):
    headings = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]]
    salaries_with_headings = headings + salaries
    table_instance = AsciiTable(salaries_with_headings, table_title)
    print(table_instance.table)
    print()
