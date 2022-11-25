import codecs
import json

import requests
from bs4 import BeautifulSoup
# import lxml
from random import randint

__all__ = ('hh_uz', )

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                   'Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'},
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/15.1 Safari/605.1.15'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.83'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36'}
]


def hh_uz(ur, city=None, language=None):
    data_jobs = []
    data_errors = []
    if ur:
        res = requests.get(url=ur, headers=headers[randint(0, 6)])
        with open('../home.html', 'w') as file:
            file.write(res.text)

        with open('../home.html') as file:
            src = file.read()
        if res.status_code == 200:
            soup = BeautifulSoup(src, 'lxml')
            main_div = soup.find('div', {'id': 'a11y-main-content'})
            if main_div:
                # count = 0
                div_lst = soup.find_all('div', class_='serp-item')
                for div in div_lst:
                    h3 = div.find('h3')
                    href = h3.a['href']
                    company = div.find('div', class_='vacancy-serp-item__meta-info-company')
                    # place = div.find_all('div', class_='bloko-text')[1].text
                    content1 = div.find_all('div', class_='bloko-text')[2].text
                    content2 = ''
                    if len(div.find_all('div', class_='bloko-text')) > 3:
                        content2 = div.find_all('div', class_='bloko-text')[3].text
                    # print(company.text)
                    # print(content1 + content2)
                    data_jobs.append(
                        {'url': href, 'title': h3.text, 'company': company.text,
                         'description': content1 + content2,
                         'city_id': city, 'language_id': language
                         }
                    )
                with open('../work.json', 'w') as file:
                    json.dump(data_jobs, file, indent=4, ensure_ascii=False)
                    print('Done!!!')
            else:
                data_errors.append({'url': ur, 'title': "Div doesn't exist"})
        else:
            data_errors.append({'url': ur, 'title': "Page didn't response"})
    return data_jobs, data_errors


if __name__ == '__main__':
    url = 'https://tashkent.hh.uz/search/vacancy?text=python&from=suggest_post&area=2759'
    jobs, errors = hh_uz(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
