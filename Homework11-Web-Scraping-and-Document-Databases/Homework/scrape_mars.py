import pandas as pd
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import time
from config import (consumer_key, 
                    consumer_secret, 
                    access_token, 
                    access_token_secret)
import tweepy

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    # ## Scraping

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p

    # #### JPL Mars Space Images - Featured Image



    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)
    browser.click_link_by_partial_text("more info")
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find("article")
    extension = results.find("figure", "lede").a["href"]
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + extension
    
    mars_dict["featured_image_url"] = featured_image_url


    # #### Mars Weather


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "@MarsWxReport"

    tweet = api.user_timeline(target_user)[0]
    mars_weather = tweet["text"]
    
    mars_dict["mars_weather"] = mars_weather


    # #### Mars Facts



    url = "http://space-facts.com/mars/"
    mars_facts = pd.read_html(url)
    

    mars_facts_df = mars_facts[0]
    mars_facts_df.columns=["Facet", "Value"]

    mars_facts_df['Facet'] = mars_facts_df['Facet'].map(lambda x: x.rstrip(':').lstrip('aAbBcC'))
    
    mars_facts_table = mars_facts_df.to_html()
    mars_facts_table.replace("\n", "")
    mars_dict["mars_facts_table"] = mars_facts_table


    # #### Mars Hemispheres



    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    hemisphere_image_urls = []




    # Cerberus
    browser.visit(hemi_url)
    time.sleep(5)
    browser.click_link_by_partial_text("Cerberus Hemisphere Enhanced")

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    cerberus_link = soup.find("div", "downloads").a["href"]

    cerberus = {
        "title": "Cerberus Hemisphere",
        "img_url": cerberus_link
    }

    hemisphere_image_urls.append(cerberus)




    # Schiaparelli 
    browser.visit(hemi_url)
    time.sleep(5)
    browser.click_link_by_partial_text("Schiaparelli Hemisphere Enhanced")

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    schiaparelli_link = soup.find("div", "downloads").a["href"]

    schiaparelli = {
        "title": "Cerberus Hemisphere",
        "img_url": schiaparelli_link
    }

    hemisphere_image_urls.append(schiaparelli)





    # Syrtis Major
    browser.visit(hemi_url)
    time.sleep(5)
    browser.click_link_by_partial_text("Syrtis Major Hemisphere Enhanced")

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    syrtis_major_link = soup.find("div", "downloads").a["href"]

    syrtis_major = {
        "title": "Cerberus Hemisphere",
        "img_url": syrtis_major_link
    }

    hemisphere_image_urls.append(syrtis_major)





    # Valles Marineris
    browser.visit(hemi_url)
    time.sleep(5)
    browser.click_link_by_partial_text("Valles Marineris Hemisphere Enhanced")

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    valles_marineris_link = soup.find("div", "downloads").a["href"]

    valles_marineris = {
        "title": "Cerberus Hemisphere",
        "img_url": valles_marineris_link
    }

    hemisphere_image_urls.append(valles_marineris)
    
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_dict

