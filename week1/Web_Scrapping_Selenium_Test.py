'''
import requests
page = requests.get("https://www.google.com")
contents = page.content
print(contents)

from bs4 import BeautifulSoup
soup = BeautifulSoup(contents, 'lxml')
print(soup.find('a'))

from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.google.com/')
element = browser.find_element_by_name("q")
element.send_keys("hello world")
element.submit()
browser.close()
'''
from re import findall,sub
from lxml import html
from time import sleep
from selenium import webdriver
from pprint import pprint

def parse(url):
    searchKey = "Las Vegas" # Change this to your city 
    checkInDate = '27/08/2019' #Format %d/%m/%Y
    checkOutDate = '29/08/2019' #Format %d/%m/%Y
    response = webdriver.Chrome()
    response.get(url)
    searchKeyElement = response.find_elements_by_xpath('//input[contains(@id,"q-destination")]')
    checkInElement = response.find_elements_by_xpath('//input[contains(@id,"q-localised-check-in")]')
    checkOutElement = response.find_elements_by_xpath('//input[contains(@id,"q-localised-check-out")]')
    submitButton = response.find_elements_by_xpath('//button[@type="submit"]')
    if searchKeyElement and checkInElement and checkOutElement:
        searchKeyElement[0].send_keys(searchKey)
        checkInElement[0].clear()
        checkInElement[0].send_keys(checkInDate)
        checkOutElement[0].clear()
        checkOutElement[0].send_keys(checkOutDate)
        randomClick = response.find_elements_by_xpath('//h1')
        if randomClick:
            randomClick[0].click()
        submitButton[0].click()
        sleep(15)
        dropDownButton = response.find_elements_by_xpath('//a[@data-menu="sort-submenu-price"]')
        if dropDownButton:
            dropDownButton[0].click()
            priceLowtoHigh = response.find_elements_by_xpath('//a[@data-option-id="opt_PRICE"]')
            if priceLowtoHigh:
                priceLowtoHigh[0].click()
                sleep(10)

    parser = html.fromstring(response.page_source,response.current_url)
    hotels = parser.xpath('//li[@class="hotel"]')
    for hotel in hotels[:5]: #Replace 5 with 1 to just get the cheapest hotel
        hotelName = hotel.xpath('.//h3/a')
        hotelName = hotelName[0].text_content() if hotelName else None
        price = hotel.xpath('.//div[@class="price"]/a//ins')
        price = price[0].text_content().replace(",","").strip() if price else None
        if price==None:
            price = hotel.xpath('.//div[@class="price"]/a')
            price = price[0].text_content().replace(",","").strip() if price else None
        price = findall('([\d\.]+)',price) if price else None
        price = price[0] if price else None
        star = hotel.xpath('.//span[contains(@class,"star-rating-text")]')
        star = star[0].text_content() if star else None
        address = hotel.xpath('.//span[@dir="ltr"]')
        address = "".join([x.text_content() for x in address]) if address else None
        rating = hotel.xpath('.//strong[contains(@class, "guest-reviews-badge")]')
        rating = rating[0].text_content() if rating else None

        item = {
                    "hotelName":hotelName,
                    "price":price,
                    "rating":rating,
                    "address":address,
                    "star":star
        }
        pprint(item)

    response.close()

url = "https://www.hotels.com"
parse(url)