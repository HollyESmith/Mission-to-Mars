# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = bs(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p

    # ### Featured Images

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = bs(html, 'html.parser')

    # Find the relative image url. -->.get('src') pulls the link to the image
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url_rel

    # Use the base URL to create an absolute URL. We're using an f-string for this print statement because
    # it's a cleaner way to create print statements; they're also evaluated at run-time. This means that it, 
    # and the variable it holds, doesn't exist until the code is executed and the values are not constant. 

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url

    # Creating a new dataframe from the HTML table. [read_html()] specifically searches for and returns
    # a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only 
    # the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['description', 'Mars', 'Earth'] # assign columns to the new DataFrame for additional clarity

    # .set_index() function turns the Description column into the DataFrame's index.
    # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame 
    # to a new variable.
    df.set_index('description', inplace=True)
    df

    # Pandas converts DataFrame back into HTML-ready code using [.to_html()]
    df.to_html()

    # Deliverable 1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # Hemispheres

    # Use BeautifulSoup and Splinter to scrape full-resolution images of Mars’s hemispheres 
    # and the titles of those images

    #1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #3. Write a code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_list = bs(html, 'html.parser')

    items = hemisphere_list.find_all('div', class_='item')

    base_url = 'https://marshemispheres.com/'

    for item in items:
        url = item.find("a")['href']
        browser.visit(base_url + url)
        
        hemisphere_item_html = browser.html
        hemisphere_soup = bs(hemisphere_item_html, 'html.parser')
        
        title = hemisphere_soup.find('h2', class_ = 'title').text
        
        downloads = hemisphere_soup.find('div', class_ = 'downloads')
        image_url = downloads.find('a')['href']
        
        hemisphere_image_urls.append({"title": title, "url": base_url + image_url})

    #4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": img_url,
        "facts": df.to_html(classes="table table-striped"),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }    

    return data

if __name__ == "__main__":
    print(scrape_all())

