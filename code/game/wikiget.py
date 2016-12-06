# coding: utf-8
import codecs
import mwclient


def get_page_names():
    site = mwclient.Site('ru.wikipedia.org')
    category = site.Pages[u'Категория:Населённые пункты по алфавиту']
    return (page.name for page in category)


def is_letter(c):
    return u'а' <= c.lower() <= u'я'


def starts_and_ends_with_letter(name):
    first = name[0]
    last = name[-1]
    return is_letter(first) and is_letter(last)


def remove_braces(name):
    return name.split('(')[0].strip()


def get_cities():
    used_cities = set()
    for name in get_page_names():
        city = remove_braces(name)
        if starts_and_ends_with_letter(city) and city not in used_cities:
            used_cities.add(city)
            yield city


with codecs.open('cities.txt', 'w', 'utf8') as f:
    for city in get_cities():
        f.write(city + '\n')
