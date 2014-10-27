#!/usr/bin/env python
# Copyright (c) 2013, Hal Blackburn <hal@caret.cam.ac.uk>,
#                     CARET <http://www.caret.cam.ac.uk/>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Romeo Scrape.

Scrapes a list of Journals from SHERPA RoMEO (www.sherpa.ac.uk/romeo/),
printing them to stdout.

Usage:
    romeo_scrape.py
    romeo_scrape.py [--raw-html | --ugly-json]
    romeo_scrape.py (-h | --help)
    romeo_scrape.py --version

Options:
  --raw-html   Output the HTML response from SHERPA RoMEO instead of JSON.
  --ugly-json  Don't pretty print the JSON output.
  -h --help    Show this screen.
  --version    Print the version and exit.
"""

from collections import OrderedDict
import json
import re
import sys

from docopt import docopt
from lxml import etree
import requests


VERSION = "Romeo Scrape 0.0.1"
ROMEO_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 2.5"
ROMEO_URL = "http://www.sherpa.ac.uk/romeo/"
# Thanks to a handy bug, fetching a pageno beyond the last seems to return
# all journals.
# FIXME: pageno
ALL_JOURNALS_URL = (
    "http://www.sherpa.ac.uk/romeo/journalbrowse.php?pageno=9999&letter=Z")
SSN_PATTERN = re.compile(r"[0-9]{4}-[0-9]{3}[0-9X]")
EMPTY_PATTERN = re.compile(r"^\s*-\s*$")


class RomeoException(Exception):
    pass


def fetch_all_journal_html():
    resp = requests.get(ALL_JOURNALS_URL)
    if not resp.ok:
        raise RomeoException(
            "Request failed. Status: {}".format(resp.status_code)
        )

    # The content returned is UTF-8 but has at least one invalid char, so we
    # need to replace errors with the unicode replacement char.
    return resp.content.decode("utf-8", errors="replace")


def parse_journals(html):
    root = etree.fromstring(html, parser=etree.HTMLParser())
    return [
        journal_from_table_row(tr)
        for tr in root.xpath("//table[@class='journaltable']/tr[position()>1]")
    ]


def journal_from_table_row(tr):
    return OrderedDict([
        ("title", empty_values(tr.xpath("normalize-space(td[1])"))),
        ("issn", split_ssns(tr.xpath("normalize-space(td[2])"))),
        ("essn", split_ssns(tr.xpath("normalize-space(td[3])"))),
        ("colour", empty_values(tr.xpath("normalize-space(td[4])").lower())),
        ("publisher", empty_values(tr.xpath("normalize-space(td[5])"))),
        ("notes", empty_values(tr.xpath("normalize-space(td[6])")))
    ])


def empty_values(string):
    return None if EMPTY_PATTERN.match(string) else string


def split_ssns(ssn_str):
    return SSN_PATTERN.findall(ssn_str)


def main():
    arguments = docopt(__doc__, version=VERSION, help=True)

    html = fetch_all_journal_html()

    if arguments["--raw-html"]:
        sys.stdout.write(html.encode("utf-8"))
        sys.exit(0)

    journal_data = OrderedDict([
        ("source", ROMEO_URL),
        ("license", ROMEO_LICENSE),
        ("journals", parse_journals(html))
    ])

    indent = None if arguments["--ugly-json"] else 2
    json.dump(journal_data, sys.stdout, indent=indent)


if __name__ == "__main__":
    status = 0
    try:
        main()
    except requests.RequestException as e:
        print >> sys.stderr, "Error executing HTTP request for journals:", e
        status = 2
    except RomeoException as e:
        print >> sys.stderr, e
        status = 3
    sys.exit(status)
