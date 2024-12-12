# parser.py

import codecs
import json
import random
import time
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests.exceptions import RequestException

__all__ = ('hh_uz',)

def get_random_headers():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    return headers

def fetch_page(url, retries=3, backoff_factor=0.3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=get_random_headers(), timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(backoff_factor * (2 ** attempt))
    return None

def parse_vacancy_card(card, city_id, language_id):
    job = {}
    
    # Extract title and URL
    title_tag = card.find('a', attrs={'data-qa': re.compile(r'serp-item__title')})
    if title_tag:
        job['title'] = title_tag.get_text(strip=True)
        job['url'] = title_tag['href']
    else:
        job['title'] = None
        job['url'] = None
    
    # Extract company name
    company_tag = card.find('a', attrs={'data-qa': re.compile(r'vacancy-serp__vacancy-employer')})
    if company_tag:
        job['company'] = company_tag.get_text(strip=True)
    else:
        job['company'] = None
    
    # Extract experience
    experience_tag = card.find('span', attrs={'data-qa': re.compile(r'vacancy-serp__vacancy-work-experience')})
    if experience_tag:
        job['description'] = experience_tag.get_text(strip=True)
    else:
        job['description'] = None
    
    # Extract city (as string) - Remove this to avoid conflicts
    # city_tag = card.find('span', attrs={'data-qa': re.compile(r'vacancy-serp__vacancy-address')})
    # if city_tag:
    #     job['city'] = city_tag.get_text(strip=True)
    # else:
    #     job['city'] = None
    
    # Assign city_id and language_id from the parameters
    job['city_id'] = city_id
    job['language_id'] = language_id
    
    return job

def hh_uz(url, city=None, language=None):
    data_jobs = []
    data_errors = []
    
    if not url:
        data_errors.append({'url': url, 'title': "No URL provided"})
        return data_jobs, data_errors
    
    page_content = fetch_page(url)
    if not page_content:
        data_errors.append({'url': url, 'title': "Failed to retrieve the page after multiple attempts"})
        return data_jobs, data_errors
    
    soup = BeautifulSoup(page_content, 'lxml')
    
    main_div = soup.find('div', {'id': 'a11y-main-content'})
    if not main_div:
        data_errors.append({'url': url, 'title': "Main content div not found"})
        return data_jobs, data_errors
    
    # Use regex to match 'data-qa' attributes containing 'vacancy-serp__vacancy'
    vacancy_cards = main_div.find_all('div', attrs={'data-qa': re.compile(r'vacancy-serp__vacancy')})
    
    if not vacancy_cards:
        data_errors.append({'url': url, 'title': "No vacancy cards found"})
        return data_jobs, data_errors
    
    for card in vacancy_cards:
        try:
            job = parse_vacancy_card(card, city, language)
            if job['url']:
                data_jobs.append(job)
        except Exception as e:
            print(f"Error parsing a vacancy card: {e}")
            continue
    
    # Save jobs to JSON
    with open('work.json', 'w', encoding='utf-8') as file:
        json.dump(data_jobs, file, indent=4, ensure_ascii=False)
    
    return data_jobs, data_errors

if __name__ == '__main__':
    url = 'https://tashkent.hh.uz/search/vacancy?text=python&from=suggest_post&area=2759'
    # You can set city_id and language_id based on your requirements
    city_id = 2759  # Example city ID for Tashkent
    language_id = 1  # Example language ID
    jobs, errors = hh_uz(url, city=city_id, language=language_id)
    
    # Optionally, save jobs to a text file
    with codecs.open('work.txt', 'w', 'utf-8') as h:
        h.write(str(jobs))
    
    if errors:
        with codecs.open('errors.txt', 'w', 'utf-8') as e:
            e.write(str(errors))
