#Team 25 YouthVSCovid API - getNews.py
#Copyright (C) 2020 arthomnix
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published
#by the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from newsapi import NewsApiClient
from ml.model import predictCoronaArticle
from secret import newsApiKey

newsWebsites = 'bbc-news'
newsapi = NewsApiClient(api_key=newsApiKey)

#print("A Young Coders Meetup project for Teens In AI YouthVSCovid Hackathon")
#print("Powered by News API https://newsapi.org/")



def getNonCoronaNews(page=1):
    if page > 10:
        raise ValueError("A free API key only supports 100 requests (10 pages).")
    news = newsapi.get_everything(sources=newsWebsites, language='en', page_size=10, page=page, sort_by='relevancy')
    articles = news['articles']
    nonCoronaArticles = []
    coronaArticles = []
    coronaCounter = 0
    output = []
    for article in articles:
        title = article['title']
        description = article['description']
        content = title + ' ' + description
        corona = False
        if predictCoronaArticle(content) == 1:
            corona = True
        if not corona:
            nonCoronaArticles.append(article)
        else:
            coronaArticles.append(article)
            coronaCounter += 1
    for article in nonCoronaArticles:
        output.append({'source': 'bbc-news', 'title': article['title'], 'description': article['description'], 'url': article['url']})
    return output

def getCoronaNews():
    news = newsapi.get_everything(q='coronavirus', sources=newsWebsites, language='en', page_size=100)
    articles = news['articles']
    output = []
    for article in articles:
        output.append({'source': 'bbc-news', 'title': article['title'], 'description': article['description'], 'url': article['url']})
    return output
#print(f"Filtered out {coronaCounter} coronavirus-related articles")
#for article in nonCoronaArticles:
#    print(f"Title: {article['title']}")
#    print(f"Link: {article['url']}")
#
#
#print("Filtered articles:")
#for article in coronaArticles:
#    print(f"{article['title']}")
