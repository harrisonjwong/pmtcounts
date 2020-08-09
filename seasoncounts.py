from datetime import datetime
import requests
import mwclient
import json
site = mwclient.Site('lol.gamepedia.com', path='/')

matches = site.api('cargoquery',
    limit = "max",
    tables = "MatchSchedule=M",
    fields = "M.OverviewPage, M.Team1, M.Team2, M.DateTime_UTC, M.Reddit",
    where = 'M.OverviewPage="LEC/2020 Season/Summer Season"'
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

for match in cleanMatches:
    if "redd.it" in match.reddit:
        # reddit.com/comments/last-6-characters/.json
        redditCode = match.reddit[-6:]
        link = "https://reddit.com/comments/{code}/.json".format(code = redditCode)
        match.angel = getUsernameFromRedditPost(link)
    elif "reddit.com" in match.reddit:
        link = "{link}.json".format(link = match.reddit)
        match.angel = getUsernameFromRedditPost(link)
    else:
        match.angel = "thread_missing"
    print(match)