import pandas as pd
import extruct as ex
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import config



###url to scrape#######
URL=config.URLS[0]
#URL='https://fr.trustpilot.com/review/cdisount.fr'



####get chrome driver##########
def get_driver_chrome():
    ###chrome option#####
    options = Options()
    ####add argument#####
    options.add_argument('--headless')
    ####dynamic install
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    return driver

###############################get source page###########################################
def get_source_page(driver, url):
    driver.get(url)
    return driver.page_source

##############################get json page###############################################
def get_json(source):
    return ex.extract(source, syntaxes=['json-ld'])

##############################jump to next page##############################
def get_next_page(driver, source):
    ###localize###
    elements = driver.find_elements_by_xpath('//link[@rel="next"]')
    if elements:
        return driver.find_element_by_xpath('//link[@rel="next"]').get_attribute('href')
    else:
        return ''

############################save reviews########################################
def save_reviews(data, df):
    for item in data['json-ld']:
        if "review" in item:
            for review in item['review']:

                row = {
                    'author': review.get('author', {}).get('name'),
                    'headline': review.get('headline'),
                    'body': review.get('reviewBody'),
                    'rating': review.get('reviewRating', {}).get('ratingValue'),
                    'item_reviewed': review.get('itemReviewed', {}).get('name'),
                    'publisher': review.get('publisher', {}).get('name'),
                    'date_published': review.get('datePublished')
                }

                df = df.append(row, ignore_index=True)

    return df 


if __name__ == "__main__":
    df = pd.DataFrame(columns = ['author', 'headline', 'body', 'rating', 
                             'item_reviewed', 'publisher', 'date_published'])
    driver = get_driver_chrome()
    source = get_source_page(driver, URL)
    json = get_json(source)
    df = save_reviews(json, df)
    next_page = get_next_page(driver, source)
    paginated_urls = []
    paginated_urls.append(next_page)
    if paginated_urls:
        for url in paginated_urls:
            if url:
                print(next_page)
                driver = get_driver_chrome()
                source = get_source_page(driver, url)
                json = get_json(source)
                df = save_reviews(json, df)
                next_page = get_next_page(driver, source)
                paginated_urls.append(next_page)
    df.to_csv('discount_reviews_data.csv')
