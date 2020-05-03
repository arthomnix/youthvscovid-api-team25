#Team 25 YouthVSCovid API - getPopularTimes.py
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
import populartimes
import secret

def getPopularTimes(tl, br, q, day):
    return populartimes.get(secret.apiKey, [q], tl, br)
