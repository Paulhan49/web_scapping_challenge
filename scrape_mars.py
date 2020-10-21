#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs

#Site Navigation
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# # NASA Mars News

def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

# # JPL Mars Space Images - Featured Image
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image_path = soup.find_all('img', class_="thumb")[1]["src"]
    current_img = "https://www.jpl.nasa.gov" + image_path
    return current_img


# # Mars Facts
def marsFacts():
    import pandas as pd
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    #facts_html = browser.html
    #soup = bs(facts_html, "html.parser")
    #facts = soup.find(id_="tablepress-p-mars-no-2", class_="tablepress tablepress-p-mars")
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ["Description", "Value"]
    mars_data = df.set_index("Description")
    mars_data
    return mars_data


# # Mars Hemispheres
def marsHem():
    import time 
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    
    articles = soup.find('div', class_='description')
    #hemis = articles.find('div', class_='item')
    

    for hemi in articles:
        title = hemi.a.find("h3").text
        link = hemi.find('a')
        href = link['href']
        img_url = "https://astrogeology.usgs.gov" + href
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    return hemisphere_image_urls