#!/usr/bin/env python3
"""[summary]
ABC 問題から入出力のみ出力する
"""

from bs4 import BeautifulSoup
import requests

import argparse


def main(url):
    contest = url[:-2]

    url = "https://atcoder.jp/contests/{}/tasks/{}".format(contest, url)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, features="html.parser")

    description = bs.find("span", class_="lang-ja") or bs.find(
        "div", id="task-statement"
    )

    print(bs.title.text, url, sep="\n")
    for s in description.find_all("pre"):
        print(s.text, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    main(args.url)
