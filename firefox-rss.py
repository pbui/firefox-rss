#!/usr/bin/env python3

import datetime
import email
import re

import requests

# Constants

RELEASES_URL    = 'https://ftp.mozilla.org/pub/firefox/releases/'
RELEASES_RX     = r'a href="/pub/firefox/releases/([0-9\.]+)/' # Excludes beta, esr
RELEASES_LIMIT  = 12

# Functions

def fetch_all_releases(url=RELEASES_URL):
    return re.findall(RELEASES_RX, requests.get(url).text)

def print_rss_header():
    print('''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>Firefox Releases</title>
<link>https://ftp.mozilla.org/pub/firefox/releases/</link>
<description>Firefox Releases</description>
<atom:link href="https://yld.me/raw/firefox-rss" rel="self" type="application/rss+xml" />
''')

def print_rss_item(release):
    response = requests.get(f'https://www.mozilla.org/en-US/firefox/{release}/releasenotes/')
    if response.status_code != 200:
        return

    pub_date = datetime.datetime.strptime(
        re.findall(r'<p class="c-release-date">([^<]+)</p>', response.text)[0],
        '%B %d, %Y'
    )

    print('''<item>
<title>Firefox {release}</title>
<author>firefox@mozilla.org (Firefox)</author>
<link>https://www.mozilla.org/en-US/firefox/{release}/releasenotes/</link>
<pubDate>{pub_date}</pubDate>
<guid isPermaLink="false">{release}</guid>
</item>'''.format(release=release, pub_date=email.utils.format_datetime(pub_date)))

def print_rss_footer():
    print('''</channel>
</rss>''')

# Main Execution

def main():
    print_rss_header()

    releases = fetch_all_releases()
    for release in sorted(releases, key=lambda r: [int(n) for n in r.split('.')])[-10:]:
        print_rss_item(release)
    
    print_rss_footer()

if __name__ == '__main__':
    main()
