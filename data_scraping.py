
#%%
#dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time


#%%
# # Mars Headlines
#url and get page with requests
url = 'https://mars.nasa.gov/news/'
response = requests.get(url)


#%%
#get your soup (object)
headlines_soup = bs(response.text, 'lxml')


#%%
#scrape the latest news headline text and get rid of the white space
headline = headlines_soup.find('div', class_ = 'content_title').text.strip()


#%%
#print it to make sure it works
print(headline)


#%%
#scrape the blurb text that goes with the headline - a.k.a. the first paragraph without white space 
news = headlines_soup.find('div', class_ = 'rollover_description_inner').text.strip()


#%%
#make sure that one worked too...
print(news)


#%%
# # Get your featured image of Mars
# Import Selenium & Splinter and set the chromedriver path (I'm on windows)
from selenium import webdriver
from splinter import Browser
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


#%%
#visit the URL
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


#%%
#click the button to get to the full image
browser.click_link_by_id('full_image')


#%%
#pause 2 seconds to let it load
time.sleep(2)


#%%
#scrape browser into soup and find full resolution image of Mars
#btw, there is no "largesize" image link
#Bring up the image
html = browser.html
image_soup = bs(html, "lxml")
img_url = image_soup.find('img', class_ = 'fancybox-image')['src']


#%%
#append the url snippet to make it the full url of the image 
featured_img_url = "https://www.jpl.nasa.gov" + img_url


#%%
#verify we have the url
featured_img_url


#%%
#on to getting the latest tweet about the weather on Mars
url = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(url)


#%%
# create soup object
weather_soup = bs(response.text, 'html.parser')


#%%
#grab all the tweets in case the first one isn't the one you want
mars_weather_tweet = weather_soup.find_all('div', class_ = "js-tweet-text-container")


#%%
# find the first actual weather tweet (they start with "sol")
for tweet in mars_weather_tweet:
    if tweet.text.strip().startswith('Sol'):
        mars_weather = tweet.text.strip()


#%%
#verify you got the right info 
print(mars_weather)


#%%
# # Mars Facts
#visit the space facts site
url = 'https://space-facts.com/mars/'
browser.visit(url)


#%%
# find the html table and convert to pandas dataframe
mars_df = pd.read_html(url)
mars_df = (mars_df[0])


#%%
#set column headers 
mars_df.columns = ["Description", "Value"]
# mars_df = mars_df.set_index("Description")
# I decided not to reset the index because, to me, it looks messier to have the column headers in two mis-aligned cells
mars_df


#%%
mars_df = mars_df.to_html(classes='mars')
table_data = mars_df.replace('\n', ' ')
table_data


#%%



