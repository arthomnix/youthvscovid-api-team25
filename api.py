import falcon, json
from getNews import getNonCoronaNews, getCoronaNews
import newsapi
from getPopularTimes import getPopularTimes
from datetime import datetime

class NonCovidNewsResource(object):
    def on_post(self, req, resp):
        error = "None"
        try:
            data = json.load(req.bounded_stream)
        except:
            page = 1
            error = "InvalidJSONWarning"
        if 'data' in locals():
            if 'page' not in data:
                page = 1
            else:
                page = data['page']
        try:
            resp.status = falcon.HTTP_200
            news = {'error': error, 'attribution': 'Powered by NewsAPI.org', 'news': getNonCoronaNews(page)}
        except newsapi.newsapi_exception.NewsAPIException:
            resp.status = falcon.HTTP_500
            news = {'error': 'NewsAPIException', 'description': 'There was a News API error, most likely out of requests.'}
        except ValueError:
            resp.status = falcon.HTTP_400
            news = {'error': 'ValueError', 'description': 'A ValueError was raised, almost certainly due to the fact that there are only 10 pages of news. Please only use page numbers of 10 or less'}
        except:
            resp.status = falcon.HTTP_500
            news = {'error': 'GeneralError', 'description': 'Something went wrong, please contact arthomnix for details.'}
        resp.body = json.dumps(news)

class CovidNewsResource(object):
    def on_get(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            news = {'error': 'None', 'attribution': 'Powered by NewsAPI.org', 'news': getCoronaNews()}
        except newsapi.newsapi_exception.NewsAPIException:
            resp.status = falcon.HTTP_500
            news = {'error': 'NewsAPIException', 'description': 'There was a News API error, most likely out of requests.'}
        except:
            resp.status = falcon.HTTP_500
            news = {'error': 'GeneralError', 'description': 'Something went wrong, please contact arthomnix for details.'}
        resp.body = json.dumps(news)

class PopularTimesResource(object):
    def on_post(self, req, resp):
        resp.body = json.dumps({"You should not": "be seeing this"})
        try:
            data = json.load(req.bounded_stream)
            if 'tl' in data and 'br' in data and 'q' in data:
                tl = data['tl']
                br = data['br']
                q = data['q']
                day = int(datetime.now().strftime('%u'))-1
                resp.body = {'error': 'None', 'popularTimes': getPopularTimes(tl, br, q, day)}
            else:
                resp.status = falcon.HTTP_400
                resp.body = {'error': 'RequestError', 'description': 'Invalid request format.'}
            resp.body = json.dumps(resp.body)
        except:
                resp.status = falcon.HTTP_500
                resp.body = json.dumps({'error': 'GeneralError', 'description': 'Something went wrong, please contact arthomnix for details.'})

api = falcon.API()
noncovidnews_endpoint = NonCovidNewsResource()
covidnews_endpoint = CovidNewsResource()
populartimes_endpoint = PopularTimesResource()

api.add_route('/news/nonCovid', noncovidnews_endpoint)
api.add_route('/news/Covid', covidnews_endpoint)
api.add_route('/popularTimes', populartimes_endpoint)
