# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    #Setup Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    # -----------------
    # NASA Mars News
    # -----------------
    # Set up url request
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve the latest title
    news_title = soup.find('div', class_='content_title').get_text()

    # Retrieve the latest article teaser
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    # -----------------
    # JPL Mars
    # -----------------
    # Visit spaceimages-mars.com
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # create full featued image url
    featured_image_url = soup.find('img', class_='headerimage')['src']
    full_featured_image_url = url + "/" + featured_image_url

    # -----------------
    # Mars Facts
    # -----------------
    # Visit page
    url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url)

    # Convert to dataframe
    df = table[0]
    df = df.rename(columns={0:'Description', 1:'Mars', 2:'Earth'})
    df = df.set_index('Description')
    # Export to html table
    html_table = df.to_html(classes="table table-striped table-bordered")
    html_table = html_table.replace('\n', '')

    # -----------------
    # Mars Hemispheres
    # -----------------
    # Visit spaceimages-mars.com
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Open second browser for clicking link to image url
    browser_img = Browser('chrome', **executable_path, headless=False)

    # Set up blank list for dictionaries
    hemisphere_image_urls = []

    # find parent container with the list of hemispheres
    container = soup.find('div', class_='results')

    # create a list of the hemisphere titles
    items = container.find_all('div', class_='item')

    for item in items:
        # Get hemisphere title name
        title = item.find('h3').get_text()
        
        # Get full image url
        hemisphere_page = item.find('a', class_='product-item')['href']
        hemisphere_page_url = url + hemisphere_page

        # Open second browswer to new page
        browser_img.visit(hemisphere_page_url)

        #Scrape new page into Soup
        html_img = browser_img.html
        soup_img = bs(html_img, "html.parser")

        # create img_url
        img_url = url + soup_img.find('a', text='Original')['href']

        # Create dictionary
        hemisphere_dict = {"title": title, "img_url": img_url}

        # Append dict to list
        hemisphere_image_urls.append(hemisphere_dict)

    # Exit browser
    browser_img.quit()
    browser.quit()

    scrape_mars = {'Latest_News': [news_title, news_p], 
                   'Featured_Image': full_featured_image_url,
                   'Mars_Facts': html_table,
                   "Mars_Hemispheres": hemisphere_image_urls}

    return scrape_mars

