import datetime
import os
import sys

import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service_django.settings'

django.setup()
from scraping.models import Vacancy, Error, Url
from scraping_service_django.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject = f'Inbox for {today}'
text_content = f'Inbox vacancies {today}'
from_email = EMAIL_HOST_USER
empty = '<h2> Unfortunately for today\'s vacancies not available :(</h2>'
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for item in qs:
    users_dict.setdefault((item['city'], item['language']), [])
    users_dict[(item['city'], item['language'])].append(item['email'])
if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        print(pair)
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params).values()[:10]
    vacancies = {}
    print(qs)
    for item in qs:
        print(item)
        vacancies.setdefault((item['city_id'], item['language_id']), [])
        vacancies[(item['city_id'], item['language_id'])].append(item)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5><a href="{row["url"]}"> {row["title"]} </a></h5>'
            html += f'<p> {row["description"]}</p>'
            html += f'<p> {row["company"]}</p> <br> <hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email,
                                         [to])
            msg.attach_alternative(_html, 'text/html')
            msg.send()
            print('Done!')
qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    _html = ''
    if data:
        _html += '<hr>'
        _html += '<h2> User willing </h2>'
    for item in data:
        _html += f'<p>City: {item["city"]}, Language: {item["language"]}</p>'
    subject = f'User will: {today}'
    text_content = f'User will'
    data = error.data.get('user_data', [])
    to = ADMIN_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email,
                                 [to])
    msg.attach_alternative(_html, 'text/html')
    msg.send()
    print('Done!')

qs = Url.objects.all().values('city', 'language')
urls_dict = {(item['city'], item['language']): True for item in qs}
urls_error = ''
for keys in users_dict.keys():
    if keys not in urls_dict:
        urls_error += f'<p>For the city: {keys[0]} and for PL: {keys[1]} doesn\'t exist urls </p>'
if urls_error:
    subject += 'Urls doesn\'t exist'
    _html += urls_error
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email,
                                 [to])
    msg.attach_alternative(_html, 'text/html')
    msg.send()
    print('Done!')
