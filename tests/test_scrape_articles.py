import pytest
import sys
sys.path.append("..")
import cn_news_clustering.scrape_articles as scrape
from bs4 import BeautifulSoup
import requests


def test_get_soup_type():
    expected = type(BeautifulSoup())
    testPage = scrape.Webpage('http://google.com')
    actual = type(testPage._get_soup())
    assert expected == actual
