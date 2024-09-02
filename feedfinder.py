#!/usr/local/bin/python3.3
from bs4 import BeautifulSoup as bs4
import requests
import feedparser
import urllib.parse

def findfeed(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw)
    feed_urls = html.findAll("link", rel="alternate")
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get("type",None)
            if t:
                if "rss" in t or "xml" in t:
                    href = f.get("href",None)
                    if href:
                        possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site)
    base = parsed_url.scheme+"://"+parsed_url.hostname
    atags = html.findAll("a")
    for a in atags:
        href = a.get("href",None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                possible_feeds.append(base+href)
    for url in list(set(possible_feeds)):
        f = feedparser.parse(url)
        if len(f.entries) > 0:
            if url not in result:
                result.append(url)
    return(result)

# extracts all the urls from the specified file
def get_urls(input_path):    
    url_file = open(input_path)
    all_urls = []
    for lines in url_file:
        words = lines.split()
        for j in words:
            all_urls.append(j.replace(" ",""))
    return all_urls

# writes all the RSS links to the specified output file
def write_to_file(rss_urls, output_file):
    rss_file = open(output_file,'a')
    for i in rss_urls:
        rss_file.write(str(i))
        rss_file.write("\n")
    rss_file.close()

#specify the input and output file paths
def take_inputs():
    input_file = input('Enter the path to source file containing the required urls:\n')
    output_file = input('Enter the path to destination file where the RSS links will be written:\n')
    main_program(input_file, output_file)

take_inputs()

