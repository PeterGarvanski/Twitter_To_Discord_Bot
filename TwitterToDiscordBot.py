import snscrape.modules.twitter as scraper
import json
import datetime
import re
import configparser
import requests

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    url = config["discord"]["api_url"]
    auth = {"Authorization": config["discord"]["authentication"]}

    msg = {
        "content": "This was sent using a python script!"
    }

    with open("twitter.json") as file:
        jsonData = json.load(file)

    time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    currentDate = re.search(r"(\d{2}):(\d{2}):(\d{2})", str(time))
    
    hours = int(currentDate.group(1))
    minutes = int(currentDate.group(2))
    seconds = int(currentDate.group(3))
    
    customTime = (hours * 3600) + (minutes * 60) + (seconds)

    tweets = []
    running = True
    
    while running:
        for user in jsonData["userTag"]:
            print(user)
            for query in jsonData["query"]:
                q = f"({query} (from:{user}) since:{datetime.date.today()})"
                for tweet in scraper.TwitterSearchScraper(q).get_items():
                    tweetDate = re.search(r"(\d{2}):(\d{2}):(\d{2})", str(tweet.date))
                    h = int(tweetDate.group(1))
                    m = int(tweetDate.group(2))
                    s = int(tweetDate.group(3))
                    tweetTime = (h * 3600) + (m * 60) + s
                    if tweetTime > customTime:
                        print(tweet.url)
                        requests.post(url, headers=auth, data=msg)

        if len(tweets) > 0:
            running = False

if __name__ == "__main__":
    main()
