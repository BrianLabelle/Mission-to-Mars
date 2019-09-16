#!/usr/bin/env python
# coding: utf-8

# In[114]:


# Dependencies
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


# In[115]:


# URL of pages to be scraped

# NASA Mars News |  NASA Mars News Site
url_nasa_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# JPL Mars Space Images - Featured Image
url_jpl_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# Mars Weather | Twitter ( return entry with InSight sol )
url_twitter_weather = 'https://twitter.com/marswxreport?lang=en'

# Mars Facts | Space Facts
url_sf_facts = 'https://space-facts.com/mars/'

# Mars Hemispheres |  USGS Astrogeology site
# url_USGS_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
# Error 404 We couldn’t find the page. If you think you are seeing this in error please contact us. You can also try searching for the missing page.

# Temp
url_USGS_hemispheres = 'http://www.labellelube.com/mars.html'


# In[116]:


executable_path = {"executable_path":"chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)
browser.visit(url_nasa_news)
time.sleep(2)
html = browser.html
soup_news = BeautifulSoup(html, "html.parser")
time.sleep(2)


# In[117]:


# Examine results determine div that contains info
news_title = soup_news.find("div",class_="content_title").text
news_paragraph = soup_news.find("div", class_="article_teaser_body").text

# Display scrapped data 
print(news_title)
print(news_paragraph)


# In[118]:


browser.quit()
time.sleep(1)


# In[ ]:





# In[119]:


# JPL Mars Space Images - Featured Image
# http://localhost:8888/notebooks/003-99-EXTRA_Stu_Scrape_Mars/Stu_Scrape_Mars.ipynb
executable_path = {"executable_path":"chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)
browser.visit(url_jpl_images)
time.sleep(1)


# In[120]:


# https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
# https://stackoverflow.com/questions/29773368/splinter-how-to-click-a-link-button-implemented-as-a-div-or-span-element
browser.click_link_by_id('full_image')
time.sleep(1)


# In[121]:


# https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
# browser.click_link_by_text('more info')
browser.click_link_by_partial_text('more info')
time.sleep(1)


# In[122]:



#jpl_image = soup_jpl.select_one("article figure.lede a img").get("src")
html = browser.html
soup_jpl = BeautifulSoup(html, "html.parser")
time.sleep(1)
jpl_image = soup_jpl.find('figure', class_='lede').a['href']
url_root = "https://www.jpl.nasa.gov/"
time.sleep(1)
jpl_image_absolute = url_root+jpl_image
print(jpl_image_absolute)


# In[123]:


browser.quit()
time.sleep(1)


# In[124]:


## https://github.com/taspinar/twitterscraper
## DIDN"T WORK
# http://localhost:8888/notebooks/003-99-EXTRA_Stu_Scrape_Mars/Stu_Scrape_Mars.ipynb
executable_path = {"executable_path":"chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)
browser.visit(url_twitter_weather)
time.sleep(1)
html = browser.html
soup_jpl = BeautifulSoup(html, "html.parser")
time.sleep(1)


# In[ ]:





# In[125]:


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


# In[126]:


browser.quit()
time.sleep(1)


# In[127]:


# Mars Facts | Space Facts
executable_path = {"executable_path":"chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)
browser.visit(url_sf_facts)
time.sleep(1)
html = browser.html
soup_sf = BeautifulSoup(html, "html.parser")
time.sleep(1)


# In[147]:


### # Mars Facts | Space Facts
# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.read_html.html
# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.to_html.html

df_mars_facts = pd.read_html(url_sf_facts)
#df_mars_facts has earth comparison.

df_mars_comparison = df_mars_facts[0]
df_mars_space_facts = df_mars_facts[1]

df_mars_space_facts.columns = ['Description','Value']
df_mars_space_facts.set_index('Description', inplace=True)
df_mars_space_facts.to_html()
df_mars_space_facts
print(df_mars_space_facts.to_html())


# In[145]:


browser.quit()


# In[58]:


# Mars Hemispheres |  USGS Astrogeology site

executable_path = {"executable_path":"chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)
browser.visit(url_USGS_hemispheres)
time.sleep(2)


# In[62]:


html = browser.html
soup_USGS = BeautifulSoup(html, "html.parser")
items = soup_USGS.find_all('div', class_='item')
USGS_images = []
url_USGS_hemispheres = 'http://www.labellelube.com/mars.html'
url_root='http://www.labellelube.com/'

for i in items: 
    title = i.find('h2').text
    image = i.find('img')['src']
    USGS_images.append({"title" : title,"link" : url_root+image})
    
USGS_images


# In[63]:


print(USGS_images)
time.sleep(5)


# In[43]:


browser.quit()


# In[ ]:




