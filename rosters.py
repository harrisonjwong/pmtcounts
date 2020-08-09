import mwclient
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
        roleString += players[currentIndex]
    else:
        roleString += " / "
        roleString += players[currentIndex]
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
        if rolesArr[i] == "Top Laner":
            top = processRole(top, playersArr, i)
        elif rolesArr[i] == "Jungler":
            jng = processRole(jng, playersArr, i)
        elif rolesArr[i] == "Mid Laner":
            mid = processRole(mid, playersArr, i)
        elif rolesArr[i] == "Bot Laner":
            bot = processRole(bot, playersArr, i)
        elif rolesArr[i] == "Support":
            sup = processRole(sup, playersArr, i)

    print teamName, ",", top, ",", jng, ",", mid, ",", bot, ",", sup

