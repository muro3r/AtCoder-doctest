"""Generate doctest files from AtCoder"""
import argparse
import logging
import os
import sys
from urllib import parse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_body(url: str):
    """Parse task page."""

    # TODO: if content 20
    # https://abc100.contest.atcoder.jp/
    if "atcoder.jp" not in url:
        contest = url[:-2]
        url = f"https://atcoder.jp/contests/{contest}/tasks/{url}"

    r = requests.get(url)
    r.raise_for_status()

    bs = BeautifulSoup(r.text, features="html.parser")

    description = bs.find("span", class_="lang-ja") or bs.find(
        "div", id="task-statement"
    )

    body = bs.title.text + "\n" + url + "\n"
    for s in description.find_all("pre"):
        body += s.text + "\n"

    print(body)

    return url, body


def output(url: str, body: str):
    """write problem file with main statement"""
    main_statement = """def main():
    pass


if __name__ == "__main__":
    main()
"""

    _body = f'"""{body}"""\n\n' + main_statement

    contests, tasks = parse.urlparse(url).path.split("/")[2::2]

    if not os.path.isdir(contests):
        try:
            os.mkdir(contests)
        except IOError:
            sys.exit()

    filename = f"{contests}/{tasks}.py"
    if os.path.exists(filename):
        logging.error("The file was not created. File already exists.")
        sys.exit()

    with open(filename, "w", encoding="utf-8") as file:
        logging.info("%s was created.", filename)
        file.write(_body)


def main():
    parser = argparse.ArgumentParser(prog="atcoder-doctest")

    parser.add_argument("url")
    parser.add_argument("-o", "--output", action="store_true")

    args = parser.parse_args()

    url, body = get_body(args.url)

    if args.output:
        output(url, body)


if __name__ == "__main__":
    main()
