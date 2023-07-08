import requests


class HeadHunterAPI:

    @staticmethod
    def get_company_info(employer_id):
        """
        Функция для взаимодействия с API HeadHunter
        """
        req = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        return req.json()

    @staticmethod
    def get_vacancies_info(employer_id):
        params = {
            'only_with_salary': True,
            "per_page": 100,
            'area': 113
        }
        req = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        info_vacancies = requests.get(req.json()['vacancies_url'], params=params)
        return info_vacancies.json()
