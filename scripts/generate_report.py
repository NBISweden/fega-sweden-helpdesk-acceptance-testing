 #!/usr/bin/env python

import configparser
import sys
import datetime

import pandas as pd

from github import Github


ALL_ISSUE_TYPES = ["Bug", "Enhancement"]
ALL_STATUSES = ["To report", "Reported"]

config_filepath = sys.argv[1]  # path to config file with GitHub access token
product = sys.argv[2]  # name of the product

config = configparser.ConfigParser()
config.read(config_filepath)

g = Github(config["github"]["token"])

repo = g.get_repo("NBISweden/fega-sweden-helpdesk-acceptance-testing")

open_issues = repo.get_issues(state="open")


def parse_issue_labels(issue):
    labels = issue.get_labels()
    labels_dict = {}
    for label in labels:
        k, v = label.name.split(": ")
        if k in labels_dict:
            raise ValueError(f"Duplicated label category: '{k}'")
        labels_dict[k] = v
    return(labels_dict)


def normalize_text(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


def issue_to_series(issue):
    labels_dict = parse_issue_labels(issue)
    ser = pd.Series(
        [
            issue.number,
            issue.title,
            normalize_text(issue.body),
            labels_dict.get("Type"),
            labels_dict.get("Product"),
            labels_dict.get("Status")],
        index=[
            "number",
            "title",
            "body",
            "issue_type",
            "product",
            "status"])
    return ser

def issue_to_text(series):
    title = "### " + "[" + str(series.number) + "] " + series.title + "\n\n"
    text = title + series.body + "\n\n"
    return text
    

# Create issue dataframe
ser_gen = (issue_to_series(issue) for issue in open_issues)
frame = pd.DataFrame.from_records(ser_gen)

# Sort issue by type, product and status
frame.sort_values(by=["product", "issue_type", "status"], inplace=True)
frame["body"] = frame.body.str.rstrip("\n")
frame["body"] = frame.body.replace(r"\n\*\*(.+)\*\*\n+", r"\n#### \1\n\n", regex=True)

today_str = datetime.date.today().strftime("%Y-%m-%d")

front_matter = f"""---
title: "Feedback regarding '{product}'"
author: FEGA Sweden Helpdesk Team
date: {today_str}
date-format: "MMM D, YYYY"
lang: en-GB
editor: 
  markdown: 
    wrap: sentence
format:
  pdf:
    documentclass: scrreprt
    papersize: a4
    toc: true
    toc-depth: 3
    number-sections: false
    colorlinks: true
---

"""

no_enhancements_text = """# Enhancements

Anything that we think can be improved.

No enhancement requests included in this report.
"""

product_frame = frame[
    (frame["product"] == product) & (frame["status"] != "Draft")].copy()
issue_types = [t for t in ALL_ISSUE_TYPES if (t in product_frame.issue_type.values)]
print(front_matter)

for issue_type in issue_types:
    issue_type_frame = product_frame[product_frame.issue_type == issue_type]
    if issue_type == "Bug":
        print(f"# Bugs\n\nAny unexpected behaviour is considered by us to be a bug.\n")
    elif issue_type == "Enhancement":
        print(f"# Enhancements\n\nAnything that we think can be improved.\n")
    else:
        print(f"# {issue_type}\n")
    for status in [s for s in ALL_STATUSES if s in issue_type_frame.status.values]:
        status_frame = issue_type_frame[issue_type_frame.status == status]
        if status == "To report":
            print(f"## New\n")
        elif status == "Reported":
            print("## Previously reported but unresolved")
        else:
            pass

        for index, row in status_frame.iterrows():
            print(issue_to_text(row))

if "Enhancements" not in issue_types:
    print(no_enhancements_text)
