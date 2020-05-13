#Team 25 YouthVSCovid API - awsSentiment.py
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
import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='eu-west-2')

def detectSentiment(text, langCode='en'):
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode=langCode)
    return sentiment

if __name__ == "__main__":
    print(detectSentiment("lockdown is so boring, nothing to do, i'm feeling so depressed"))
