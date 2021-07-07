import sys
import urllib.request
import re
import os
dirname = os.path.dirname(__file__)

#Generate Output file
#In -> League, matchweek
#Out -> Output File
def getOutputFile(startDate):
    temp = os.getcwd() + "\\fixtures\\fixtures_" + startDate + ".txt"
    print(temp)
    return temp
    
#Get correct URL for match based on league and week
#In -> league, week
#Out -> URL
def makeUrls(dates):
    urlList = []
    for date in dates:
        d = "https://www.bbc.co.uk/sport/football/scores-fixtures/" + date
        urlList.append(d)
    return urlList
#Retrieves base text of Url
#In -> URL
#Out -> Clean HTML
def get_webpage(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()   
        if (isinstance(html, bytes)): # convert bytes to string if necessary
            html = html.decode('utf-8','ignore') # was decode('utf-8')
            #Remove JS + CSS
            clean = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
            #Remove Comments
            clean = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", clean)
            #Remove Tags
            clean = re.sub(r"(?s)<.*?>", " ", clean)
            #Remove Punctuation
            clean = re.sub(r"[!()-[]{};:'""\,<>./?@#$%^&*_~]+", " ", clean)
            #Remove Whitespace
            clean = re.sub(r"&\w+;", " ", clean)
            clean = re.sub(r"\s+", " ", clean)
            clean = clean.strip()       
            return clean
            
#Method to remove some unneeded Content from webpage
#In -> Web Content
#Out -> reduced Content focused on Fixtures
def filter(content):
    reduced = re.split(r"(?s)Content (.*)", content)
    r = reduced[1]
    reduced = re.split(r"(?s) All time(.*)", r)
    clean = reduced[0]
    #Remove Foreign Characters
    clean = clean.replace("é", "e")
    clean = clean.replace("ö", "o")
    clean = clean.replace("î", "i")
    clean = clean.replace("ü", "u")
    clean = clean.replace("É", "E")
    clean = clean.replace("á", "a")
    return clean
    
#Service Method to standardise Team Name Formats
#In -> Team
#Out -> Clean Team name    
def filterGame(team1):
        if("Ham" in team1):
            team1 = "West Ham"
        if("United" in team1):
            team1 = team1.replace("United", "Utd")
        if("Sheffield" in team1):
            team1 = team1.replace("Sheffield", "Sheff")
        if("Wolverhampton Wanderers" in team1 or "Wolves" in team1):
            team1 = "Wolves"
        if("Manchester" in team1):
            team1 = team1.replace("Manchester", "Man")
        if("Leicester City" in team1):
            team1 = "Leicester"
        if("Tottenham" in team1):
            team1 = "Tottenham"
        if("Paderborn" in team1):
            team1 = "SC Paderborn"
        if("Koln" in team1):
            team1 = "Cologne"
        if("AFC" in team1):
            team1 = "Bournemouth"
        if("Hove Albion" in team1 or "Brighton" in team1):
            team1 = "Brighton"
        if("Newcastle" in team1):
            team1 = "Newcastle"
        if("Norwich" in team1):
            team1 = "Norwich"
        if("Atletico" in team1):
            team1 = team1.replace("Atletico", "Atl")
        if("Sociedad" in team1):
            team1 = "Sociedad"
        if("Leverkusen" in team1):
            team1 = "B Leverkusen"
        if("Frankfurt" in team1):
            team1 = "E Frankfurt"
        if("Schalke" in team1):
            team1 = "Schalke"
        if("Hoffenheim" in team1):
            team1 = "Hoffenheim"
        if("Werder" in team1):
            team1 = team1.replace("Werder", "W")
        if("Freiburg" in team1):
            team1 = "Freiburg"
        if("VfL" in team1):
            team1 = team1.replace("VfL ", "")
            team1 = team1.replace(" VfL", "")
        if("Monchengladbach" in team1 or "Mgladbach" in team1):
            team1 = "Mgladbach"
        if("Paris" in team1 or "Germain" in team1):
            team1 = "Paris St-G."
        if("Brest" == team1):
            team1 = "Stade Brest"
        if("Borussia" in team1):
            team1 = team1.replace("Borussia", "B")
        if("Valladolid" in team1):
            team1 = "Valladolid"
        if("Athletic" in team1):
            team1 = team1.replace("Athletic", "Ath")
        if("Bayern" in team1):
            team1 = team1.replace("Bayern", "B")
        if("FC" in team1):
            team1 = team1.replace(" FC", "")
            team1 = team1.replace("FC ", "")
        if("05" in team1):
            team1 = team1.replace(" 05", "")
        if("Fortuna" in team1):
            team1 = "F Dusseldorf"
        if("SPAL" == team1):
            team1 = "Spal"
        if("AC" in team1):
            team1 = team1.replace("AC ", "")
        if("Inter" in team1):
            team1 = "Inter"
        if("saint" in team1):
            team1 = team1.replace("Saint", "St")
        if("Etienne" in team1):
            team1 = "St-Etienne"
        if("Hellas Verona" == team1):
            team1 = "Verona"
        if("Bromwich Albion" == team1):
            team1 = "West Brom"
        if("Leeds" in team1):
            team1 = "Leeds"
        if("DSC" in team1):
            team1 = "Arminia"
        if("VfB" in team1):
            team1 = "Stuttgart"
        if("Arminia" in team1):
            team1 = "Arminia"
        return team1
    
    
#Uses Regex to get games from webpage
#In -> WebContent, Dictionary
#Out -> List of Games    
def getGames(content, dictionary):
    #Find Games using Regex
    #matches two Words/Numbers followed by HH:MM for time followed by two Words/Numbers
    games = re.findall(r"(?s)([A-Z|a-z|\d|\-]+)\s(\d.|[A-Z|a-z|\-]+)?\s\d\d:\d\d\s([A-Z|a-z|\-]+)\s(\d.|[A-Z|a-z|\-]+)?", content)
    #print(games)
    gamelist = []
    #For each Game
    for game in games:
        #Format related Stuff
        if(game[0] == game[1]):
            team1 = game[1]
        else:
            team1 = game[0] + " " + game[1]
        if(game[2] == game[3]):
            team2 = game[2]
        else:
            team2 = game[2] + " " + game[3]
            
        #Strip Team names
        team1 = filterGame(team1)
        team2 = filterGame(team2)
        #Make List
        g = [team1, team2]
        #print(g)
        #if team is tracked in Betlist
        if(team1 in dictionary and team2 in dictionary):
            #Add to gamelist
            gamelist.append(g)
    return gamelist
    
#Get Fixtures from Url
#In -> Url
#Out -> Fixture List    
def getFixtures(url):
    #Initialise team Dictionary
    initTeamDict()
    #Get Webpage
    page = get_webpage(url)
    #Strip Webpage
    reducedPage = filter(page)
    print(reducedPage)
    #print(reducedPage)
    #Get Games
    games = getGames(reducedPage, teamDict)
    return games
    
#Create Dictionary TeamName:ID
#In -> nothing
#Out -> nothing (Sets Global Dict variable)
teamDict = {}
def initTeamDict():
    file = open("teams.txt","r")
    if file.mode == "r":
        contents = file.readlines()
        for line in contents:
            line = line.strip()
            x = line.split(",")
            teamDict[x[0]] = x[1]
       
#Write Fixtures to file
#In -> File, Fixtures
#Out -> Write Fixtures to given File
def writeFixtures(File, Fixtures):
        f = open(File, "w")
        for game in Fixtures:
            output = game[0] + "," + game[1] + "\n"
            f.write(output)
       
       
#Main Function
#In -> System Arguments for Dates
#Out -> Fixture File       
def main(gameDates):
    #Get Dates from Sys Argv
    dates = gameDates
    startDate = dates[0]
    #Generate output File
    out = getOutputFile(startDate)
    #Generate Urls
    urls = makeUrls(dates)
    #Create fixture list
    fixtures = []
    #For each Url made
    for url in urls:
        #Get Fixtures
        fix = getFixtures(url)
        #For each fixture
        for f in fix:
            #Add fixture to list
            print(f)
            fixtures.append(f)
    #Write to File
    writeFixtures(out, fixtures)
    
    
if __name__ == "__main__":
	main()