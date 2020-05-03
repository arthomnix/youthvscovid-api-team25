import populartimes
import secret

def getPopularTimes(tl, br, q, day):
    return populartimes.get(secret.apiKey, [q], tl, br)
