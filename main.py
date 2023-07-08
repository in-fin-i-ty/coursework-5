from DB_manager import DBManager

if __name__ == '__main__':
    db = DBManager()
    """
    Для очистки, создания и заполнения таблиц раскомментируйте первые 5 строк кода
    для получения информации из таблиц раскомментируйте одну из последних 5-ти строк кода
    """
    # db.drop_table()
    # file_id = db.file_with_id_company()
    # db.create_table()
    # db.add_companies(file_id)
    # db.add_vacancies(file_id)
    # print(db.get_vacancies_with_higher_salary())  # зп выше средней
    # print(db.get_avg_salary())  # средняя зп
    # print(db.get_all_vacancies())  # все вакансии
    # print(db.get_companies_and_vacancies_count())  # количество вакансий у компаний
    # print(db.get_vacancies_with_keyword('менеджер'))  # поиск по ключевому слову в названиях вакансий
