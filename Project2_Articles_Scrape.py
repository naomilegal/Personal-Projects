#!/usr/bin/env python
# coding: utf-8

# Welcome
# in the following netbook you will find the code we used to create a news agregator, a tool that can detect polarity of articles from a website. The newspapers websites are also to be selected by section defined here :

# In[3]:


from news_extract import *
from newspaper import Article
#from news_nlp import *
#from news_scrape import *
import time
import nltk
import requests
from bs4 import BeautifulSoup as soup 


# # Summary of articles

# In[4]:


def summarize_article(url):
    article = Article(url)
    
    article.download()
    article.parse()
    article.download('punkt')
    article.nlp()
    
#     date = article.publish_date
#     print("Author of the article:"+ str(article.authors))
#     print("Date of Publication:" + str(date.strftime("%m/%d/%Y")))
#     print("Top Image Url:"+ str(article.top_image))#gets the first image of the article
#     image_string = "All Images:"
#     for image in article.images:
#         image_string += "\n\t" + image
#     print(image_string)
#     print("Article Summary:")
#     print(" ")
#     print(article.summary)
    return article
    
summarize_article('https://www.nytimes.com/2021/05/14/technology/hes-a-dogecoin-millionaire-and-hes-not-selling.html')
#loop


articles =[]
list_of_urls = ['https://www.chicagotribune.com/sports/white-sox/ct-chicago-white-sox-kansas-city-royals-takeaways-20210517-4xmlqpefkbhmtizkcaympox72i-story.html','https://www.chicagotribune.com/sports/bulls/ct-chicago-bulls-milwaukee-bucks-finale-offseason-20210517-6rn3sb7hkfeb7mbzb5yk4oslnq-story.html','https://www.chicagotribune.com/sports/cubs/ct-chicago-cubs-detroit-tigers-series-takeaways-20210517-yia72rrfy5eq5mft2ugep3s3jy-story.html']
for url in list_of_urls:
    article = summarize_article(url)
    articles.append(article)
    
articles

for article in articles:
    print(article.title)




    
#you can make a listt of urls that then you can use for getting more articles
    
    


# # Getting Topics

# ## Sciences NY-Times

# In[32]:


def article_string(url):
    page = requests.get(url)
    page_soup = soup(page.content, 'html.parser')
    # Use the below statement as a visualizer of the HTML outline.
    # print(page_soup)
    containers = page_soup.find_all("script", {"type": "application/ld+json"})

    article_list = []
    for container in containers:
        for dictionary in container:
            article_list.append(dictionary)
    article_list[0:2] = [''.join(article_list[0:2])]
    content_string = article_list[0]
    article_index = content_string.index("itemListElement")
    content_string = content_string[article_index + 18:]
    return content_string
article_string('https://www.nytimes.com/section/science/space')



  



     
    



# ## Tech NY-Times

# In[33]:


def get_content_string(url):
    page = requests.get(url)
    page_soup = soup(page.content, 'html.parser')
    # Use the below statement as a visualizer of the HTML outline.
    # print(page_soup)
    containers = page_soup.find_all("script", {"type": "application/ld+json"})

    article_list = []
    for container in containers:
        for dictionary in container:
            article_list.append(dictionary)
    article_list[0:2] = [''.join(article_list[0:2])]
    content_string = article_list[0]
    article_index = content_string.index("itemListElement")
    content_string = content_string[article_index + 18:]
    return content_string
get_content_string('https://www.nytimes.com/section/science/space')
                   
                   
                   


# In[8]:


# def get_content_string(url):
#     page = requests.get(url)
#     page_soup = soup(page.content, 'html.parser')
#     # Use the below statement as a visualizer of the HTML outline.
#     # print(page_soup)
#     containers = page_soup.find_all("script", {"type": "application/ld+json"})

#     article_list = []
#     for container in containers:
#         for dictionary in container:
#             article_list.append(dictionary)
#     article_list[0:2] = [''.join(article_list[0:2])]
#     content_string = article_list[0]
#     article_index = content_string.index("itemListElement")
#     content_string = content_string[article_index + 18:]
#     return content_string
get_content_string('https://www.nytimes.com/section/science/space')


# In[54]:


def get_content_string(url):
    page = requests.get(url)
    page_soup = soup(page.content, 'html.parser')
    # Use the below statement as a visualizer of the HTML outline.
    # print(page_soup)
    containers = page_soup.find_all("script", {"type": "application/ld+json"})

    article_list = []
    for container in containers:
        for dictionary in container:
            article_list.append(dictionary)
    article_list[0:2] = [''.join(article_list[0:2])]
    

    content_string = article_list[0]
    article_index = content_string.index("itemListElement")
    content_string = content_string[article_index + 18:]
    return content_string
get_content_string('https://www.nytimes.com/section/science/space')


# In[52]:


content_string = get_content_string('https://www.nytimes.com/section/science/space')
def find_occurences(content_string):
    start_indices = [i for i in range(len(content_string)) if
                     content_string.startswith('https://www.nytimes.com/2020', i)]
    print(start_indices)
    end_indices = [i for i in range(len(content_string)) if content_string.startswith('.html', i)]
    print(end_indices)

    end_indices = [x + 5 for x in end_indices]
    print(end_indices)

    if len(start_indices) > len(end_indices):
        difference = len(start_indices) - len(end_indices)
        start_indices = start_indices[:difference]
    if len(end_indices) > len(start_indices):
        difference = len(end_indices) - (len(end_indices) - len(start_indices))
        end_indices = end_indices[:difference]
    return start_indices, end_indices



    
        
        


# In[55]:


def get_all_urls(start_indices, end_indices, content_string):
    url_list = []
    print('start_indices = ', start_indices)
    for i in range(len(start_indices)):
        url_list.append(content_string[start_indices[i]:end_indices[i]])
    print('url listt  =', url_list)


# In[57]:


start_indices, end_indices = find_occurences(content_string)
get_all_urls(start_indices, end_indices, content_string)


# In[53]:





# In[ ]:




