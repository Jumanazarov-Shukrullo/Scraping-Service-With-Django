# run_scraping.py

import asyncio
import codecs
import os
import sys
import datetime as dt

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service_django.settings'

from django.contrib.auth import get_user_model
from django.db import DatabaseError
import django

django.setup()

from scraping.parser import *
from scraping.models import (
    Url,
    Vacancy,
    Error, City, Language
)

User = get_user_model()

parsers = ((hh_uz, 'hh_uz'),)
jobs, errors = [], []

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
            urls.append(tmp)
    return urls

async def main(value):
    func, ur, city, language = value
    jo, err = await loop.run_in_executor(None, func, ur, city, language)
    errors.extend(err)
    jobs.extend(jo)

settings = get_settings()
url_list = get_urls(settings)
city_instance = City.objects.filter(slug='tashkent').first()
language_instance = Language.objects.filter(slug='python').first()

import time

start = time.time()

loop = asyncio.get_event_loop()
tmp_tasks = [(
    func, data['url_data'][key], data['city'], data['language'])
    for data in url_list
    for func, key in parsers
]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

# Remove the direct for loop to prevent duplicate scraping
# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         print(url)
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        err = Error(data=f'errors:{errors}').save()
