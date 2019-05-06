
#%%
#Import needed libraries and functions
import sys
import pickle
import requests
from datetime import datetime
from bs4 import BeautifulSoup

#%%
#Get htaml elements and parse values
def get_date(news_block_node):
    #Parse the html by specific attributes and get text values
    date_string = news_block_node.find(class_="news_date").string.split('|')[0][2:-1]

    #Format the time and dates
    return(datetime.strptime(date_string, '%Y.%m.%d').strftime('%Y-%m-%d'))
    
def get_title(news_block_node):
    #Get innertext of tag "a"
    return news_block_node.find(class_="news_title").a.string

def get_link(news_block_node):
    #Get href attribute of tag "a"
    return news_block_node.find(class_="news_title").a.get('href')

def get_content(link):
    r = requests.get(link)

    #Set encoding method
    r.encoding = "UTF-8"
    soup = BeautifulSoup(r.text, 'html.parser')

    #Find element by the attribute
    article_node = soup.find(itemprop='articleBody')

    #Get innertext
    article = article_node.get_text()
    
    #Delete unnecessary new lines
    return article.replace("\n", "")


#%%
#eaach_news is a bs element
def get_news_info(each_news):
    #Call the fuctions and assign the return values to the variables
    date  = get_date(each_news)
    title = get_title(each_news)
    link  = get_link(each_news)
    content = get_content(link)
    
    #Create a dictionary variale to store the above values
    info = {'date' : date,
            'title': title,
            'link' : link,
            'content': content}
    
    #Return type: dictionary
    return(info)

#Using get request and beautifulsoup to get html document
def get_page_news(page_url):
    r = requests.get(page_url)
    r.encoding = "UTF-8"

    soup = BeautifulSoup(r.text, 'html.parser')
    news_blocks = soup.find_all(class_="news-list-item clearfix ")
    
    news = []

    #Loop through each html element whose class = news-list-item clearfix
    for each_news in news_blocks:
        #Only append the list when success
        try:
            news_info = get_news_info(each_news)
#             print(get_title(each_news))
        except:
#             print('-------{}-------'.format())
            pass

        #Append the list
        news.append(news_info)

    #Return type: list
    return(news)


def get_new_talk_news(from_page=1, end_page=270, url="https://newtalk.tw/news/subcategory/2/政治/"):
    print("page_number from {} to {}".format(from_page, end_page -1))
    data = []
    
    #Loop through every page of news website with the scraping process
    for page_number in range(from_page, end_page):
        print("page_number: {}".format(page_number))
        data = data + get_page_news( url+str(page_number) )
    
    print('done')
    return(data)


#%%
data = get_new_talk_news(from_page=1, end_page=270)


#%%
#Show part of the data
data.head()


#%%
#Save all data as a pkl file
sys.setrecursionlimit(100000)
with open('data/new_talk.pkl', 'wb') as handle:
    pickle.dump(data, handle)