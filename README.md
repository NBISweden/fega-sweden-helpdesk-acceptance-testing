# FEGA Sweden Helpdesk Acceptance Testing

The purpose of this repository is to keep track of issues resulting from acceptance testing carried out by the by FEGA Sweden's Helpdesk team.

[See open issues](https://github.com/NBISweden/fega-sweden-helpdesk-acceptance-testing/issues)

We are currently testing the following products:

* **File upload** -- software for uploading files the FEGA Sweden
* **Submitter Portal** -- FEGA Sweden's instance of the FEGA Submitter Portal, which is currently hosted by central EGA.
* **Helpdesk Portal** -- FEGA Sweden's instance of the FEGA Submitter Portal, which is currently hosted by central EGA.

## Generating reports

A script can be used for compiling reports to be sent to developers. Prerequisites and use is described below.

### Prerequisites

You need to have Python 3 installed on your computer, as well as the following Python packages:

* [pandas](https://pandas.pydata.org)
* [PyGithub](https://pygithub.readthedocs.io/en/latest/index.html)

1. Use the Python script `generate_report.py` to export non-draft issues to [Quarto](https://quarto.org) markdown.

Usage:

```
./generate_report.py [CONFIG-FILE] [PRODUCT-NAME]
```

For example, to generate a report file, type something like this in the terminal:

```
./generate_report.py ~/my-config.ini "Submitter Portal" > ~/report.qmd
```

The config file should contain a valid GitHub access token and be formatted like this:

```
[github]
token={your access token}
```

2. Open and edit the resulting markdown file in [RStudio](https://posit.co/products/open-source/rstudio/).

3. From within RStudio, render a pdf of the report (you will need to have LaTeX installed on your computer in order to do this).
