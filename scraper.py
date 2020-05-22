import os
import random
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from requests_html import HTMLSession
from models import Base, Success, TestedURLs, URLsToTest

# app config
DATABASE_URL = os.environ.get('DATABASE_URL')

# database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def main(event, context):
    """
    Primary function that checks a website to determine if it is Django or Wagtail.
    """
    Base.metadata.create_all(engine)
    url = get_random_url()
    print(url)

    if url and not url_already_tested(url):
        save_tested_url(url)
        result = try_admin_dashboard(url)
        save_result(result)


def get_random_url():
    session = Session()
    urls = session.query(URLsToTest).filter(URLsToTest.tested!=True).all()

    if urls:
        url = random.choice(urls)

        # save as tested
        url.tested = True
        session.commit()

        result = url.url
    else:
        result = None

    return result


def url_already_tested(url):
    session = Session()
    return session.query(TestedURLs.id).filter_by(url=url).scalar()


def save_tested_url(url):
    session = Session()
    new_url = TestedURLs(url=url)
    session.add(new_url)
    session.commit()


def try_admin_dashboard(url):
    session = HTMLSession()
    r = session.get(url + '/admin')
    if r.status_code == 200:
        html = r.html.html
        if is_django(html) or is_wagtail(html):
            result = {
                'is_django': is_django(html),
                'is_wagtail': is_wagtail(html),
                'title_text': get_title_text(url),
                'url': url
            }
            print(result)
            return result


def is_django(html):
    return 'csrfmiddlewaretoken' in html


def is_wagtail(html):
    return 'Wagtail' in html


def get_title_text(url):
    time.sleep(1)
    session = HTMLSession()
    r = session.get(url)
    return r.html.find('title', first=True).text


def save_result(result):
    if result:
        session = Session()
        new_success = Success(**result)
        session.add(new_success)
        session.commit()


if __name__ == '__main__':
    main("", "")
