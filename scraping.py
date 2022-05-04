# Import Splinter and BeautifulSoup
from dataclasses import dataclass
from http.server import executable
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiates headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #Set news title and paragraph variables (will return 2 values)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls=hemisphere(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls(),
        "last_modified": dt.datetime.now()
    }
    return data

# add 'browser' to function, telling Python that we'll be using the browser variable we defined outside the function
def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    # By adding try: just before scraping, we're telling Python to look for these elements. 
    # If there's an error, Python will continue to run the remainder of the code. 
    # If it runs into an AttributeError, instead of returning the title and paragraph, Python will return nothing instead.
    try:
        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image

def featured_image(browser):   
    # Visit URL
    url = 'https://spaceimages-mars.com'
    print(url)
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url.   .get('src') pulls the link to the image
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL. We're using an f-string for this print statement because
    # it's a cleaner way to create print statements; they're also evaluated at run-time. This means that it, 
    # and the variable it holds, doesn't exist until the code is executed and the values are not constant. 
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

    #Stop webdriver and return data
    browser.quit()
    return data

# ## Scrape Hemisphere Data
def hemisphere(browser):
    url='https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    img_links=browser.find_by_css("a.product-item h3")

    for x in range(len(img_links)):
        hemisphere={}

        # find elements
        browser.find_by_css("a.product-item h3")[x].click()

        # find sample image link
        sample_img= browser.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']

        # get hemisphere title
        hemisphere['title']=browser.find_by_css("h2.title").text

        # add objects to hemisphere_image_urls list
        hemisphere_image_urls.append(hemisphere)

        browser.back()
    return hemisphere_image_urls    

# Tell Flask that script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all()) 



