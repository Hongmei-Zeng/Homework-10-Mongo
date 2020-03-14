import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint

def scrape():
    
    URL_1 = "https://mars.nasa.gov/news/"
    html_text = requests.get(URL_1).text
    soup = BeautifulSoup(html_text, "html.parser")
    news_title = soup.find_all("div", class_="content_title")[0].text  
    
    FILE = "html-selenium.txt"
    FILE_WAIT = "html-selenium-wait.txt"
    driver = webdriver.Firefox()
    driver.get(URL_1)
    html = driver.page_source
    with open(FILE, "w+",encoding="utf-8") as f:
        f.write(html)
    driver.get(URL_1)
    driver.implicitly_wait(10)
    html = driver.page_source
    driver.close()
    with open(FILE_WAIT, "w+", encoding="utf-8") as f:
        f.write(html)
    soup = BeautifulSoup(html, "html.parser")
    news_p = soup.find_all("div", class_="article_teaser_body")[0].text

    URL_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    html_text = requests.get(URL_2).text
    soup = BeautifulSoup(html_text, "lxml")
    article = soup.find("article", class_="carousel_item")
    pic_src = article.find("a", class_="button fancybox")["data-fancybox-href"]
    pic_id = pic_src.split("/")[4]
    pic_id = pic_id.split("_")[0]
    featured_image_url = (
        f"https://www.jpl.nasa.gov/spaceimages/images/mediumsize/{pic_id}_ip.jpg"
        )

    URL_3 = "https://twitter.com/marswxreport?lang=en"
    html_text = requests.get(URL_3).text
    soup = BeautifulSoup(html_text, "lxml")
    all_tweet_p = soup.find_all(
        "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
        )
    latest_tweet_p = all_tweet_p[0]
    mars_weather = list(latest_tweet_p.children)[0]

    URL_4 = "https://space-facts.com/mars/"
    html_text = requests.get(URL_4).text
    df = pd.read_html(html_text)[0]
    df.rename(columns={0: "facts", 1: "values"}, inplace=True)
    df["facts"] = df["facts"].str.replace(":", "")
    facts_html = df.to_html()


    URL_5 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    URL_6 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    URL_7 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    URL_8 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    URL_ls = [URL_5, URL_6, URL_7, URL_8]

    hemisphere_img_ls = []
    for URL in URL_ls:
        html_text = requests.get(URL).text
        soup = BeautifulSoup(html_text, "lxml")
        article = soup.find("div", class_="container")
        title_text = article.h2.get_text()
        hemisphere_name = title_text.split(" Enhanced")[0]
        image_src = article.find("img", class_="wide-image")["src"]
        image_id = image_src.split("/")[3].split("_enhanced.tif")[0]
        img_url = f"https://astrogeology.usgs.gov/cache/images/{image_id}_enhanced.tif_full.jpg"
        hemisphere_img_ls.append({"Hemisphere": hemisphere_name, "Image": img_url})

    return {
        "News_title": news_title.replace("\n",""),
        "News_paragraph": news_p.replace('\"',""),
        "JPL_image": featured_image_url,
        "Weather": mars_weather,
        "Mars_facts": facts_html,
        "Hemispheres_and_images": hemisphere_img_ls
        }