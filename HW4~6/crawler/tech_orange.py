#%% [markdown]
# # 爬蟲
# 在科技報橘TechOrange網站爬五個產業的新聞各80篇，包含電商、區塊鍊、金融、行銷和旅遊，最後分別將爬蟲結果存成五個檔案
# [爬蟲結果](/crawler/data)

#%%
import sys
import pickle
import requests
from datetime import datetime
from bs4 import BeautifulSoup

#%%
# Main function. In oreder to iterate through all pages on the website.
def get_data_from_news_pages(from_page, to_page, search_word):
    url_1 = "https://buzzorange.com/techorange/page/"
    url_2 = "/?s="
    print("page_number from {} to {}" .format(from_page, to_page))
    data = []
    for page_number in range(from_page, to_page + 1):
        print("page_number: {}" .format(page_number))
        data = data + get_news_from_each_page(url_1 + str(page_number) + url_2 + search_word)
    
    print("done")
    return(data)

# Get all news of one page
def get_news_from_each_page(url):
    r = requests.get(url)
    r.encoding = "UTF-8"
    soup = BeautifulSoup(r.text, "html.parser")
    news_blocks = soup.find_all("article")
    
    news = []
    for each_news in news_blocks:
        try:
            news_info = get_news_info(each_news)
            # print(get_title(each_news))
        except:
            pass
        else:
            news.append(news_info)
    return(news)

# Get all information, including date, title, share times, link and content, of a news of one page. Then, combine the information as a dictionary object.
def get_news_info(each_news):
    date  = get_date(each_news)
    title = get_title(each_news)
    share = get_share(each_news)
    link  = get_link(each_news)
    content = get_content(link)
    info = {
        "date" : date,
        "title" : title,
        "share" : share,
        "link" : link,
        "content" : content
        }
    return(info)

# Get the published date of a news
def get_date(news_block_node):
    date_string = news_block_node.find("time", class_="entry-date").text
    return(datetime.strptime(date_string, "%Y/%m/%d").strftime("%Y-%m-%d"))

# Get the title of a news
def get_title(news_block_node):
    return news_block_node.find("h4", class_="entry-title").a.text

# Get the share times of a news
def get_share(news_block_node):
    return news_block_node.find("span", class_="shareCount").text

# Get the link of a news
def get_link(news_block_node):
    return news_block_node.find("h4", class_="entry-title").a.get("href")

# Get the contnent of a news
def get_content(link):
    r = requests.get(link)
    r.encoding = "UTF-8"
    article = ""
    soup = BeautifulSoup(r.text, "html.parser")
    article_block = soup.find("div", class_="entry-content")
    for article_node in article_block.find_all("p"):
        if article_node.find("a"):
            continue
        article += article_node.text
    # print(article)
    return article.replace("\n", "")

#%%
# Scrap through indicated industries
for industry_to_search in ["電商", "區塊鍊", "金融", "行銷", "旅遊"]:
    data = get_data_from_news_pages(from_page=1, to_page=10, search_word=industry_to_search)
    sys.setrecursionlimit(100000)
    with open("./crawler/data/tech_orange_" + industry_to_search + ".pkl", "wb") as handle:
        pickle.dump(data, handle)
