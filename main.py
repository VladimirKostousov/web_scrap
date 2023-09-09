import requests
import bs4
import fake_headers
import json


def save_json(file):
    with open('vacancy.json', 'w', encoding='utf-8') as v:
        json.dump(file, v, ensure_ascii=False, indent=4, sort_keys=True)


def main():
    pages = 3
    url = 'https://hh.ru/search/vacancy?text=python+django+flask&area=1&area=2&page='
    for i in range(pages):
        main_url = url + str(i + 1)
        headers = fake_headers.Headers(browser='firefox', os='win')
        search_page = requests.get(main_url, headers=headers.generate())
        search_page_text = search_page.text
        search_page_soup = bs4.BeautifulSoup(search_page_text, features='lxml')
        vacancy_list_tag = search_page_soup.find_all('div', class_='vacancy-serp-item__layout')
        vacancy_file = finder(vacancy_list_tag)
        save_json(vacancy_file)


vacancy_table = []


def finder(vacancy_list_tag):
    for vacancy in vacancy_list_tag:
        vacancy_tag = vacancy.find('a', class_='serp-item__title')
        vacancy_title = vacancy_tag.text
        link = vacancy.find('a')['href']
        salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if salary is not None:
            salary = salary.text.replace('\u202f', ' ')
        else:
            salary = 'Не указана'

        company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
        vacancy_table.append(
            {
                'Vacancy:': vacancy_title,
                'Company:': company,
                'Salary:': salary,
                'Link:': link,
                'City:': city
            }
        )
    return vacancy_table


if __name__ == '__main__':
    main()
