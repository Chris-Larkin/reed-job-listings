## Import packages
import requests
import re
import os
import lxml.html
import pandas as pd
pd.set_option('max_colwidth',120)
pd.set_option('display.max_row', 100)
import numpy as np
from itertools import chain
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request as ur
from html.parser import HTMLParser

## Setting base URLs and target URLs
base = "http://www.reed.co.uk"
url = "http://www.reed.co.uk/jobs?datecreatedoffset=Today"

## Defining function all_urls() for grabbing links for all pages on reed's website for the day
def all_urls():
    r = requests.get(url).content
    soup = BeautifulSoup(r, "html.parser")
    # get the urls from the first page
    yield  [urljoin(base, a["href"]) for a in soup.select("div.details h3.title a[href^=/jobs]")]
    nxt = soup.find("a", title="Go to next page")
    # title="Go to next page" is missing when there are no more pages
    while nxt:
        # wash/repeat until no more pages
        r = requests.get(urljoin(base, nxt["href"])).content
        soup = BeautifulSoup(r, "html.parser")
        yield  [urljoin(base, a["href"]) for a in soup.select("div.details h3.title a[href^=/jobs]")]
        nxt = soup.find("a", title="Go to next page")

## Calling function and extracting links to each vacancy
dflink = pd.DataFrame(columns=["links"], data=list(chain.from_iterable(all_urls())))

## Define function strip_html()
def strip_html(x):
    return lxml.html.fromstring(x).text_content() if x else ' '

## Initializing empty dataframe
emptydata = pd.DataFrame({"job_description":[], "salary_disp":[], "salary_min":[], "salary_max":[], "salary_time":[], "job_country":[], "job_region":[], "job_locality":[], "job_postcode":[], "job_type":[], "job_type_disp":[], "applications_ten":[], "link":[]})

## Filling out dataframe with a description + other columns for each vacancy
for index, row in dflink.iloc[0:dflink.size].iterrows():
    url = row['links']
    s = ur.urlopen(url).read()
    soup = BeautifulSoup(s, "html.parser")
    description = strip_html(str(soup.find_all("span", itemprop="description")))
    try:
        get_a_new_job = pd.DataFrame({
                "job_description":[description],
                "salary_disp":[soup.select_one('.salary span').text.strip()],
                "salary_min":[soup.select_one('.salary meta[itemprop="minValue"]')["content"]],               
                "salary_max":[soup.select_one('.salary meta[itemprop="maxValue"]')["content"]],
                "salary_time":[soup.select_one('.salary meta[itemprop="unitText"]')["content"]],               
                "job_country":[soup.select_one('.location span[id="jobCountry"]')["value"]], 
                "job_region":[soup.select_one('.location meta[itemprop="addressRegion"]')["content"]],
                "job_locality":[soup.select_one('.location span[itemprop="addressLocality"]').text],
                "job_postcode":[soup.select_one('.location meta[itemprop="postalCode"]')["content"]],
                "job_type":[soup.select_one('.time span[itemprop="employmentType"]')["content"]],
                "job_type_disp":[soup.select_one('.time span[itemprop="employmentType"]').text],
                "applications_ten":[soup.select_one('.applications').text.strip()],
                "link": [row]             
        })
        emptydata = emptydata.append(get_a_new_job)
    except:
        pass

## Rename dataframe
reed_data = emptydata

## How many listings have we scraped?
reed_data.size

## Inspect listings as pd frame
reed_data
