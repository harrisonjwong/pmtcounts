import mwclient
import re
site = mwclient.Site('lol.gamepedia.com', path='/')

teams = site.api('cargoquery',
    limit = "max",
    tables = "Teams=T,TournamentRosters=TR",
    fields = "T.Name, TR.RosterLinks, TR.Roles",
    join_on = "T.Name=TR.Team",
    where = 'TR.Tournament="LCS 2020 Summer"'
)


def processRole(roleString, players, currentIndex):
    if roleString == "":
        roleString += re.sub(r" ?\([^)]+\)", "", players[currentIndex])
    else:
        roleString += " / "
        roleString += re.sub(r" ?\([^)]+\)", "", players[currentIndex])
    return roleString


for team in teams.get("cargoquery"):
    teamName = team.get("title").get("Name")
    roles = team.get("title").get("Roles")
    players = team.get("title").get("RosterLinks")

    rolesArr = roles.split(";;")
    playersArr = players.split(";;")

    top = ""
    jng = ""
    mid = ""
    bot = ""
    sup = ""

    for i in range(len(rolesArr)):
        if rolesArr[i] == "Top":
            top = processRole(top, playersArr, i)
        elif rolesArr[i] == "Jungle":
            jng = processRole(jng, playersArr, i)
        elif rolesArr[i] == "Mid":
            mid = processRole(mid, playersArr, i)
        elif rolesArr[i] == "Bot":
            bot = processRole(bot, playersArr, i)
        elif rolesArr[i] == "Support":
            sup = processRole(sup, playersArr, i)

    print("{teamName}, {top}, {jng}, {mid}, {bot}, {sup}".format(
        teamName = teamName,
        top = top,
        jng = jng,
        mid = mid,
        bot = bot,
        sup = sup))

