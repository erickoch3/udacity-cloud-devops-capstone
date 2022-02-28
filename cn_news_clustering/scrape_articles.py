#!/usr/local/bin/python

""" This module helps us scrape articles from a given websites """
from lexical_analysis import is_chinese_char
from clustering import cluster_pages
from globals import Globals as glob
from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path
from collections import OrderedDict
import logging
import urllib3
# TODO: Convert our print statements to logging.

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.ERROR)

class WebsiteDatabase:

    def __init__(self, sites):
        """ Initialize with a list of string website hostnames """
        self.pages_data = OrderedDict()
        self.invalid_sites = dict()
        self._load_db_from_json()
        self.sites = list()
        self._scrape_sites(sites)

    def _load_db_from_json(self):
        """ Loads data from a json if found. """
        # Grab a corpus if one exists
        try:
            if Path(glob.db_path).exists():
                with open(glob.db_path, 'r') as openfile:
                    logging.info(f"{glob.floppy} Loading saved data...")
                    self.pages_data = OrderedDict(json.load(openfile))
            else:
                logging.info(f"{glob.floppy} No data to load.")
                
            if Path(glob.invalid_sites_path).exists():
                with open(glob.invalid_sites_path, 'r') as openfile:
                    logging.info(f"{glob.floppy} Loading saved data...")
                    self.invalid_sites = json.load(openfile)
                    for key in self.invalid_sites:
                        self.invalid_sites[key] = set(self.invalid_sites[key])
            else:
                logging.info(f"{glob.floppy} No data to load.")
        except json.decoder.JSONDecodeError:
            logging.error(f"{glob.floppy} Failed to decode saved file at {glob.db_path}")

    def _scrape_sites(self, sites):
        """ For the given sites, scrape their data. """
        for site in sites:
            # TODO Filter out the bad apples if a website has no words
            logging.info(f"{glob.web} Inspecting {site}...")
            website = Website(site, self)
            # We scrape a globally set number of pages per website
            website.scrape(website.url)
            self.sites.append(website)
        
    def _save_to_json(self):
        """ Saves the database to a json file. """
        with open(glob.db_path, "w") as outfile:
            outfile.write(json.dumps(self.pages_data))
        with open(glob.invalid_sites_path, "w") as outfile:
            for key in self.invalid_sites:
                self.invalid_sites[key] = list(self.invalid_sites[key])
            outfile.write(json.dumps(self.invalid_sites))

    def compute(self):
        """ Build our corpus of Chinese web pages and cluster them """
        self._save_to_json()
        return cluster_pages(self.pages_data.values())


class Website:

    def __init__(self, name, db):
        self.name = name
        self.url = self.clean_url(self.name)
        self.urls = set([
            url for url in db.pages_data if url.startswith(self.url)
        ])
        logging.info(f"{glob.cat_smile} We already have {len(self.urls)} urls for {self.url}.")
        self.pages = set()
        self.db = db
        if self.url not in self.db.invalid_sites:
            self.db.invalid_sites[self.url] = set()

    def scrape(self, url):
        # getting the request from url
        logging.info(f"\t{glob.search} Scraping url: {url}")
        page = Webpage(url)
        if page.url.endswith('htm') or page.url.endswith('html'):
            logging.info(f"\t{glob.fire} HIT: Saving data for page.")
            self.db.pages_data[page.url] = page.text if page.text else ''

        # If the soup fails, save that so we don't try it again.
        if not page.soup:
            logging.info(f"\t\t{glob.skull} {page.url} doesn't have soup!")
            return  

        # Stop once we've hit our max pages.
        if len(self.urls) >= glob.max_pages_per_site:
            logging.info(f"\t{glob.check} Reached max pages for {self.url}!")
            return

        if self.url not in self.db.pages_data:
            self.pages.add(page)

        # Recursively scrape web pages
        for i in page.soup.find_all("a"):
            if len(self.urls) >= glob.max_pages_per_site:
                break
            # Get all of the links
            try:
                href = self.clean_url(i.attrs['href'], root_url=self.url)
                logging.info(f"\t\t{glob.raw} Found: {href}")
            except KeyError:
                continue
            # Scrape all of those links that are part of the site
            if href in self.db.invalid_sites[self.url]:
                return
            
            if href is not None and href.startswith(self.url):

                if href not in self.urls:
                    self.urls.add(href)
                    # calling it self
                    self.scrape(href)
                else:
                    logging.info(f"\t\t{glob.neutral} Already scraped: {href}")
            else:
                valid = False
                for root in glob.sites:
                    if href.startswith(root):
                        self.scrape(href)
                        valid = True
                if not valid:
                    logging.info(f"\t\t{glob.skull}  Invalid: {href}")
                    self.db.invalid_sites[self.url].add(href)

    def clean_url(self, url, root_url=None):
        # If it doesn't start with http it needs to
        if not url.startswith('http://') and not url.startswith('https://'):
            # Check whether it's a relative path
            if root_url and not url.startswith(root_url[7:]):
                url = f'{root_url}/{url}'
            else:
                url = f'http://{url}'
        if url.endswith('/'):
            url = url[:-1]
        return url

class Webpage:

    def __init__(self, url):
        self.url = url
        self.soup = self._get_soup()
        self.tf_dict = dict()
        self.text = self._get_page_text()

    def _get_soup(self):
        """ Acquire the site's BeautifulSoup """
        try:
            page = requests.get(self.url)
            return BeautifulSoup(page.content, 'lxml')
        except requests.exceptions.ConnectionError or requests.exceptions.MaxRetryError:
            logging.info(f'\t\t{glob.cry} Failed to connect to {self.url}')

    def _get_page_text(self):
        """
        Takes paragraphs from the BeautifulSoup to get raw text of the page.
        """
        if not self.soup:
            logging.info(f"\t\t\t{self.url} didn't have soup.")
            return
        pgraphs = self.soup.find_all('p')
        raw_text = ''.join(p.getText() for p in pgraphs)
        # Acquire all individual Chinese characters
        return ''.join(c for c in raw_text if is_chinese_char(c))
