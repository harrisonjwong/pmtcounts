from datetime import datetime
import mwclient
import pytz

league = 'LPL'
season = '2022 Season'
split = 'Spring Season'
week = 'Week 2'

site = mwclient.Site('lol.fandom.com', path='/')

matches = site.api('cargoquery',
                   limit="max",
                   tables="MatchSchedule=M",
                   fields="M.OverviewPage, M.Team1, M.Team2, M.DateTime_UTC, M.Reddit, M.Tab",
                   where='M.OverviewPage="%s/%s/%s" and M.Tab="%s"' % (league, season, split, week)
                   # where='M.OverviewPage="%s/%s/%s"' % (league, season, split)
                   )

# print(pytz.all_timezones_set)


utc = pytz.timezone('UTC')
eastern_us = pytz.timezone('America/New_York')
pacific_us = pytz.timezone('America/Los_Angeles')
central_eu = pytz.timezone('Europe/Berlin')


def clean_team_name(name: str):
    if name == 'Rogue (European Team)':
        return 'Rogue'
    elif name == 'Evil Geniuses.NA':
        return 'Evil Geniuses'
    else:
        return name


class MyMatch:
    def __init__(self, cal, team1, team2, tab):
        self.cal = datetime.strptime(cal, '%Y-%m-%d %H:%M:%S')
        self.utc_time = utc.localize(self.cal)
        self.eastern = self.utc_time.astimezone(eastern_us)
        self.pacific = self.utc_time.astimezone(pacific_us)
        self.european = self.utc_time.astimezone(central_eu)
        self.team1 = team1
        self.team2 = team2
        self.tab = tab

    def __str__(self):
        return "{eastern_date}\t{eastern}\t{pacific}\t{european}\t{team1}\tvs.\t{team2}".format(
            eastern_date=self.eastern.strftime('%a %Y-%m-%d'),
            eastern=self.eastern.strftime('%H:%M'),
            pacific=self.pacific.strftime('%H:%M'),
            european=self.european.strftime('%H:%M'),
            team1=clean_team_name(self.team1),
            team2=clean_team_name(self.team2),
            tab=self.tab,
        )


cleanMatches = []

for match in matches.get("cargoquery"):
    matchInfo = match.get("title")
    cleanMatches.append(MyMatch(matchInfo.get("DateTime UTC"), matchInfo.get("Team1"),
                                matchInfo.get("Team2"), matchInfo.get("Tab")))

cleanMatches.sort(key=lambda r: r.cal)

for match in cleanMatches:
    print(match)
