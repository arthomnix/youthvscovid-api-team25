#Team 25 YouthVSCovid API - api.py
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
import falcon, json
from getNews import getNonCoronaNews, getCoronaNews
import newsapi
from getPopularTimes import getPopularTimes
from awsSentiment import detectSentiment
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
            news = {'error': error, 'attribution': 'Powered by NewsAPI.org', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'news': getNonCoronaNews(page)}
        except newsapi.newsapi_exception.NewsAPIException:
            resp.status = falcon.HTTP_500
            news = {'error': 'NewsAPIException', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'There was a News API error, most likely out of requests.'}
        except ValueError:
            resp.status = falcon.HTTP_400
            news = {'error': 'ValueError', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'A ValueError was raised, almost certainly due to the fact that there are only 10 pages of news. Please only use page numbers of 10 or less'}
        except:
            resp.status = falcon.HTTP_500
            news = {'error': 'GeneralError', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'Something went wrong, please contact arthomnix for details.'}
        resp.body = json.dumps(news)

class CovidNewsResource(object):
    def on_get(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            news = {'error': 'None', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'attribution': 'Powered by NewsAPI.org', 'news': getCoronaNews()}
        except newsapi.newsapi_exception.NewsAPIException:
            resp.status = falcon.HTTP_500
            news = {'error': 'NewsAPIException', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'There was a News API error, most likely out of requests.'}
        except:
            resp.status = falcon.HTTP_500
            news = {'error': 'GeneralError', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'Something went wrong, please contact arthomnix for details.'}
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
                resp.body = {'error': 'None', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'popularTimes': getPopularTimes(tl, br, q, day)}
            else:
                resp.status = falcon.HTTP_400
                resp.body = {'error': 'RequestError', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'Invalid request format.'}
            resp.body = json.dumps(resp.body)
        except:
                resp.status = falcon.HTTP_500
                resp.body = json.dumps({'error': 'GeneralError', 'source': 'https://github.com/arthomnix/youthvscovid-api-team25', 'description': 'Something went wrong, please contact arthomnix for details.'})

class LicenseInfoResource(object):
    def on_get(self, req, resp):
        resp.body=json.dumps({"License": "GNU AGPLv3", "information": "You can access the source code and detailed license info for this project at https://github.com/arthomnix/youthvscovid-api-team25"})

class SentimentAnalysisResource(object):
    def on_post(self, req, resp):
        error = "None"
        try:
            data = json.load(req.bounded_stream)
            if 'text' in data and 'lang' in data:
                text = data['text']
                lang = data['lang']
                langUsed = True
            elif 'text' in data:
                text = data['text']
                langUsed = False
            else:
                error = "RequestError"
                errorDescription = "Invalid request format."
                errorCode = falcon.HTTP_400
        except:
            error = "RequestLoadError"
            errorDescription = "The server failed to load your request data."
            errorCode = falcon.HTTP_400
        if error != "None":
            resp.status = errorCode
            resp.body = json.dumps({"error": error, "description": errorDescription})
        try:
            if langUsed:
                sentiment = detectSentiment(text, lang)
            else:
                sentiment = detectSentiment(text)
            overallSentiment = sentiment['Sentiment']
            pos = sentiment['SentimentScore']['Positive']
            neu = sentiment['SentimentScore']['Neutral']
            neg = sentiment['SentimentScore']['Negative']
            mix = sentiment['SentimentScore']['Mixed']
        except:
            error = "SentimentAnalysisError"
            errorDescription = "There was an error performing sentiment analysis, was your language code valid?"
            errorCode = falcon.HTTP_500
        if error != "None":
            resp.status = errorCode
            resp.body = json.dumps({"error": error, "description": errorDescription})
        else:
            response = {'error': error, 'overall-sentiment': overallSentiment, 'pos': pos, 'neg': neg, 'neu': neu, 'mix': mix}
            resp.body = json.dumps(response)

api = falcon.API()
noncovidnews_endpoint = NonCovidNewsResource()
covidnews_endpoint = CovidNewsResource()
populartimes_endpoint = PopularTimesResource()
license_endpoint = LicenseInfoResource()
sentiment_endpoint = SentimentAnalysisResource()

api.add_route('/news/nonCovid', noncovidnews_endpoint)
api.add_route('/news/Covid', covidnews_endpoint)
api.add_route('/popularTimes', populartimes_endpoint)
api.add_route('/license', license_endpoint)
api.add_route('/sentiment', sentiment_endpoint)
