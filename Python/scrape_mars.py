import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pprint
import requests as req
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url_nasa_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    url_jpl_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_twitter_weather = 'https://twitter.com/marswxreport?lang=en'
    url_sf_facts = 'https://space-facts.com/mars/'
    url_USGS_hemispheres = 'http://www.labellelube.com/mars.html'


    browser.visit(url_nasa_news)
    time.sleep(1)
    html = browser.html
    soup_news = BeautifulSoup(html, "html.parser")
    time.sleep(1)

    news_title = soup_news.find("div",class_="content_title").text
    news_paragraph = soup_news.find("div", class_="article_teaser_body").text

    # Mars Hemispheres |  USGS Astrogeology site
    browser.visit(url_USGS_hemispheres)

    html = browser.html
    soup_USGS = BeautifulSoup(html, "html.parser")
    items = soup_USGS.find_all('div', class_='item')
    USGS_images = []
    url_root='http://www.labellelube.com/'

    for i in items: 
        title = i.find('h2').text
        image = i.find('img')['src']
        USGS_images.append({"title" : title,"link" : url_root+image})

    browser.quit()


    
# JPL Mars Space Images - Featured Image
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    browser.visit(url_jpl_images)
    time.sleep(1)

    browser.click_link_by_id('full_image')
    time.sleep(2)

    browser.click_link_by_partial_text('more info')
 
    html = browser.html
    soup_jpl = BeautifulSoup(html, "html.parser")
    time.sleep(1)
    jpl_image = soup_jpl.find('figure', class_='lede').a['href']
    url_root = "https://www.jpl.nasa.gov/"
    time.sleep(1)
    jpl_image_absolute = url_root+jpl_image
    print(jpl_image_absolute)

    browser.quit()
    time.sleep(1)



# Mars Facts | Space Facts
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    browser.visit(url_sf_facts)
    time.sleep(1)
    html = browser.html
    soup_sf = BeautifulSoup(html, "html.parser")
    time.sleep(1)

    ### # Mars Facts | Space Facts
    # https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.read_html.html
    # https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.to_html.html

    df_mars_facts = pd.read_html(url_sf_facts)
    #df_mars_facts has earth comparison.

    
    df_mars_space_facts = df_mars_facts[1]

    df_mars_space_facts.columns = ['Description','Value']
    df_mars_space_facts.set_index('Description', inplace=True)
    df_mars_space_facts.to_html()
    df_mars_space_facts
    df_mars_space_facts_output = df_mars_space_facts.to_html()

    browser.quit()


## https://github.com/taspinar/twitterscraper
    ## DIDN"T WORK
    # http://localhost:8888/notebooks/003-99-EXTRA_Stu_Scrape_Mars/Stu_Scrape_Mars.ipynb
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    browser.visit(url_twitter_weather)
 
    html = browser.html
    soup_jpl = BeautifulSoup(html, "html.parser")

    # Find all tweets
    tweets = soup_jpl.find_all('div', class_='js-tweet-text-container')

    time.sleep(1)
    for tweet in tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
           print(weather_tweet)
           break
        else: 
            pass

        browser.quit()
        time.sleep(1)



    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "USGS_images": USGS_images,
        "jpl_image_absolute":jpl_image_absolute,
        "df_mars_space_facts_output":df_mars_space_facts_output,
        "weather_tweet":weather_tweet
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
