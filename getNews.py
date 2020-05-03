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
