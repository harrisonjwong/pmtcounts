from datetime import datetime
import requests
import mwclient
import json
site = mwclient.Site('lol.fandom.com', path='/')

matches = site.api('cargoquery',
    limit = "max",
    tables = "MatchSchedule=M",
    fields = "M.OverviewPage, M.Team1, M.Team2, M.DateTime_UTC, M.Reddit",
    where = 'M.OverviewPage="European Masters/2021 Season/Summer Main Event"'
)

class MyMatch:
    def __init__(self, cal, team1, team2, reddit):
        self.cal = datetime.strptime(cal, '%Y-%m-%d %H:%M:%S')
        self.team1 = team1
        self.team2 = team2
        self.reddit = reddit
        self.angel = "TBD"

    def __str__(self):
        return "{cal}, {team1} vs {team2}, {reddit}, {angel}".format(
            cal = self.cal,
            team1 = self.team1,
            team2 = self.team2,
            reddit = self.reddit,
            angel = self.angel
        )

cleanMatches = []

for match in matches.get("cargoquery"):
    matchInfo = match.get("title")
    cleanMatches.append(MyMatch(matchInfo.get("DateTime UTC"), matchInfo.get("Team1"),
                                matchInfo.get("Team2"), matchInfo.get("Reddit")))

cleanMatches.sort(key=lambda r:r.cal)

def getUsernameFromRedditPost(link):
    result = requests.get(link, headers = {'User-agent': 'lulmeme'})
    if result.ok:
        myJson = json.loads(result.text)
        return myJson[0].get("data").get("children")[0].get("data").get("author")
    else:
        return "unsure"

angels = {}

for match in cleanMatches:
    if "redd.it" in match.reddit:
        # reddit.com/comments/last-6-characters/.json
        redditCode = match.reddit[-6:]
        link = "https://reddit.com/comments/{code}/.json".format(code = redditCode)
        match.angel = getUsernameFromRedditPost(link)
    elif "utm_source" in match.reddit:
        linkSplitBySlash = match.reddit.split("/")
        # 6th in split by slash is the reddit ID
        redditCode = linkSplitBySlash[6]
        link = "https://reddit.com/comments/{code}/.json".format(code=redditCode)
        match.angel = getUsernameFromRedditPost(link)
    elif "reddit.com" in match.reddit:
        link = "{link}.json".format(link = match.reddit)
        match.angel = getUsernameFromRedditPost(link)
    else:
        match.angel = "thread_missing"
    print(match)

    if match.angel in angels:
        angels[match.angel] = angels[match.angel] + 1
    else:
        angels[match.angel] = 1

# print(angels)

for angel, count in angels.items():
    print("%s, %s" % (angel, count))

