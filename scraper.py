import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from requests_html import HTMLSession
from models import Base, TestedURLs, Success

# app config
DATABASE_URL = os.environ.get('DATABASE_URL')

# database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def main():
    """
    Primary function that checks a website to determine if it is Django or Wagtail.
    """
    Base.metadata.create_all(engine)
    url = 'https://www.liveonny.org/'

    if not url_already_tested(url):
        save_tested_url(url)
        result = try_admin_dashboard(url)
        save_result(result)


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
    main()
