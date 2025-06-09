
import re
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import  webdriver
from selenium.webdriver.common.by import By
import time

FORM_URl='https://forms.gle/CiXkup9JwjPHMwPF7'
URL='https://appbrewery.github.io/Zillow-Clone/'






response = requests.get(url=URL, verify=True)
zillow_data = response.text

soup = BeautifulSoup(zillow_data, 'html.parser')
address_title = soup.find_all('address', {'data-test': 'property-card-addr'})
# adress=address_title.get_text().strip()
list_of_address = [address.get_text().strip() for address in address_title]
property_links = soup.find_all('a', {'data-test': 'property-card-link'})
list_of_property_links = [link['href'] for link in property_links]
list_of_prices=[]
property_prices = soup.find_all('span', {'data-test': 'property-card-price'})
for price in property_prices:
    text = price.get_text()
    price_text = re.split(r'[\+\/]', text)
    list_of_prices.append(price_text[0])



options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get(FORM_URl)
time.sleep(3)
for i in range(len(list_of_address)):
    time.sleep(2)
    input_tags = driver.find_elements(By.CSS_SELECTOR, '.whsOnd')
    input_tags[0].send_keys(list_of_address[i])
    input_tags[1].send_keys(list_of_prices[i])
    input_tags[2].send_keys(list_of_property_links[i])
    time.sleep(2)
    submit_button=driver.find_element(By.CLASS_NAME,'uArJ5e')
    submit_button.click()
    time.sleep(2)

    next_response=driver.find_element(By.LINK_TEXT,'Submit another response')
    next_response.click()