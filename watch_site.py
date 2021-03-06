import datetime
import os
import re
import sys
import time
from urllib.parse import (
    urlsplit,
    urlunsplit,
)

import htmlmin
import requests
from bs4 import BeautifulSoup

import urls


class WaitMore(Exception):
    pass


def print_with_time(text: str):
    print(f"{datetime.datetime.now()} - {text}")


def watch_mass_immunization(site_name: str, site_url: str, page: int = 1):
    """
    Watches the mass immunization site
    """
    print_with_time(f"============= {site_name} page {page}")
    try:
        resp = requests.get(site_url)
    except Exception:
        print_with_time(f"==> Error requesting from site {site_name}")
        raise WaitMore()

    if not resp.ok:
        print_with_time(f"==> Error {resp.status_code} from site {site_name}")
        raise WaitMore()
    minified = htmlmin.minify(resp.text, remove_empty_space=True)
    soup = BeautifulSoup(minified, 'html.parser')
    all_availability = soup.body.find_all('strong', text=re.compile("Available Appointments"))

    appointmants_available = False
    for location in all_availability:
        location_name = location.parent.parent.contents[0].text.strip()
        number_of_spots = location.parent.contents[1].strip()
        try:
            number_of_spots = int(number_of_spots)
        except ValueError:
            print_with_time(f'wrong number of spots {number_of_spots} for {location_name}')
            continue
        if number_of_spots <= 0:
            continue
        link_node = location.parent.parent.find('a')
        if not link_node:
            print_with_time(f'wrong link node for {location_name}')
            continue
        link_params = link_node.attrs.get('href')
        if not link_params:
            print_with_time(f'wrong link href for {location_name}')
            continue
        parsed_base_url = urlsplit(site_url)
        full_url = urlunsplit((
            parsed_base_url.scheme,
            parsed_base_url.netloc,
            link_params,
            '',
            '',
        ))

        if number_of_spots > 0:
            print_with_time(f"{location_name} {number_of_spots} {full_url}")
            appointmants_available = True

    if not appointmants_available:
        print_with_time("No Appointments available at this time for this location")

    # try to see if there are more pages for the same query
    pagination_spans = soup.body.find_all('span', attrs={'class': 'page'})
    for pagination in pagination_spans:
        attr_class = pagination.attrs.get('class')
        if len(attr_class) > 1:
            continue
        if attr_class[0] != 'page':
            continue
        if pagination.a.attrs.get('rel')[0] != 'next':
            continue
        # extract the next page link
        a_link = pagination.a.attrs.get('href')
        parsed_base_url = urlsplit(site_url)
        next_page_full_url = urlunsplit((
            parsed_base_url.scheme,
            parsed_base_url.netloc,
            a_link,
            '',
            '',
        ))
        time.sleep(2)
        watch_mass_immunization(site_name=site_name, site_url=next_page_full_url, page=page + 1)


def watch_locations():
    while True:
        for site_name, site_address in urls.ALL_SITES.items():
            try:
                watch_mass_immunization(site_name, site_address)
                time.sleep(2)
            except WaitMore:
                time.sleep(15)
        time.sleep(10)


if __name__ == "__main__":
    try:
        watch_locations()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
