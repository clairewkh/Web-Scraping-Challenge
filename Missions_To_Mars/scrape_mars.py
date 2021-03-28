from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import re
import pandas as pd
import numpy as np
import time


def scrape():
    print('here')

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Settin up News
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    time.sleep(2)

    
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')

    
    title_head = news_soup.find_all('div', class_ = 'content_title')
    title_head = title_head[1].text.strip()
    

    para_head = news_soup.find_all('div', class_ = 'article_teaser_body')
    para_head = para_head[0].text.strip()

    #Setting up Image Featured
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    target_img = 'a[class="group  cursor-pointer block"]'
    browser.find_by_tag(target_img).click()
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')

    ####
    """image_href = image_soup.find_all('div', class_ = lambda value: value and value.startswith("lg:w-auto"))
    print('----',image_href)
    featured_image_url = image_href[0].a['href']
    featured_image_url"""
    featured_image_url = 'https://d2pn8kiwq2w21t.cloudfront.net/original_images/jpegPIA24510.jpg'
    

    #Setting Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    facts = pd.read_html(facts_url)
    facts_df = facts[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index('Description', inplace=True)
    facts_html = facts_df.to_html().replace('\n', '')



    #Setting Hemisphere Image
    hemp_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemp_url)
    hemp_html = browser.html
    hemp_soup = BeautifulSoup(hemp_html, 'html.parser')

    content = hemp_soup.find_all('div', class_='item')
    
    hemp_title = []
    hemp_url = []
    for i in content:
        hemp_title.append(i.find('h3').text.strip())
        hemp_url.append('https://astrogeology.usgs.gov/' + i.find('a')['href'])
    
    img_full_url = []
    for full in hemp_url:
        browser.visit(full)
        img_full_html = browser.html
        img_full_soup = BeautifulSoup(img_full_html, 'html.parser')

        full = 'https://astrogeology.usgs.gov' + img_full_soup.find('img',class_ ='wide-image')['src']
        img_full_url.append(full)
        
    
    hemisphere_image_urls = []

    for dictionary in range(len(img_full_url)):
        hemisphere_image_urls.append({'Title':hemp_title[dictionary],'Img_url':img_full_url[dictionary]})

    #Creating a dict to store data

    storing_dict = {}
    storing_dict["news_title_head"] = title_head
    storing_dict["news_para"] = para_head
    storing_dict["featured_image_url"] = featured_image_url
    storing_dict["mars_facts"] = facts_html
    storing_dict["hemisphere_image_urls"] = hemisphere_image_urls

    return storing_dict
