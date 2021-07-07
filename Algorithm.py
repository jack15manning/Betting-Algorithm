import urllib.request
import sys
import re
import xlwt
from xlwt import Workbook
import os
#                                               TO DO



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
   #clean = clean.lower()
   return clean
   

#Removes matches after given year
#In -> Clean Html + End Year -------NOTE YEARS NOT CURRENTLY USED - HARDCODED TO 2014
#Out -> Clean Html ending at specified year
def filter(content):
    reduced = re.sub(r"(?s)(?<=18\d\d|19\d\d|200\d|201[0-4])(.*$)", " ", content)
    return reduced
  
#Retrieves Played Games
#In -> Clean Html, Team1, Team2
#Out -> List of Games  
def getGames(content, team1, team2):
    games = re.findall(r"("+team1+")\s(\d{1})\s\-\s(\d{1})\s("+team2+")", content)
    games += re.findall(r"("+team2+")\s(\d{1})\s\-\s(\d{1})\s("+team1+")", content)
    return games
    
#Retrieves results of Games played
#In -> List of Games, Team1, Team2
#Out -> Team1 Wins, Team2 Wins, Draws    
def getResults(games, team1, team2):
    team1Wins = 0
    team2Wins = 0
    draw = 0
    #For Each Tuple in List
    for g in games:
        #Convert Tuple to List
        game = list(g)
        #print(game)
        #print(game)
        #If team 2 is Home -> Reverse list 
        if(game[3] == team1):
            game.reverse()
        #Determine winner/draw    
        if(game[1] == game[2]):
            draw += 1
        elif(game[1] > game[2]):
            team1Wins += 1
        else:
            team2Wins +=1
    return team1Wins, team2Wins, draw

#Returns Total games played
#In -> Results
#Out -> Number games
def totalGames(results):
    return results[0] + results[1] + results[2]
#Determines Odds of Each Team Winning + Draw + 1X + 2X
#In -> Results of games played, Number of games
#Out -> odds 1, 1X, Draw, 2X, 2
def getOdds(results):
    total = results[0] + results[1] + results[2]
    if(results[0] == 0):
        oneWin = 0
    else:
        oneWin = (results[0]/total)*100
    if(results[0] == 0 and results[2] == 0):
        oneX = 0
    else:
        oneX = ((results[0]+results[2])/total)*100
    if(results[2] == 0):
        draw = 0
    else:
        draw = (results[2]/total)*100
    if(results[1] == 0 and results[2] == 0):
        twoX = 0
    else:
        twoX = ((results[1]+results[2])/total)*100
    if(results[1] == 0):
        twoWin = 0
    else:
        twoWin = (results[1]/total)*100
    return oneWin, oneX, draw, twoX, twoWin

#Determines whether to place a bet
#In -> List of odds
#Out -> Bet + Odds + Bet Tier
def getBet(odds, total):        
    if(total >= 4 and (odds[1] >= 80 or odds[3] >= 80)):                #Meets bronze
        if(total >=6 and (odds[1] >= 85 or odds[3] >= 85)):             #Meets Silver
            if(total >= 8 and (odds[1] >= 90 or odds[3] >= 90)):        #Meets Gold
                if(odds[1] >= odds[3]):
                    return "1X",odds[1],"Gold"
                else:
                    return "2X",odds[3],"Gold"
            if(odds[1] >= odds[3]):
                return "1X",odds[1],"Silver"
            else:
                return "2X",odds[3],"Silver"
        if(odds[1] >= odds[3]):
            return "1X",odds[1],"Bronze"
        else:
            return "2X",odds[3],"Bronze"
                
       
    
    else:
        if(total<4):
            return "Not enough Data", 0, ""
        else:
            return "Low Odds", 0, ""
       

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
    
#Get correct URL for match based on given teams
#In -> team1, team2
#Out -> URL
def makeUrl(team1, team2):
    team1ID = teamDict[team1]
    team2ID = teamDict[team2]
    url = "https://www.soccerbase.com/teams/head_to_head.sd?team_id=" + team1ID + "&team2_id=" + team2ID
    return url

#Gets list of Fixtures from Text File
#In -> FixtureFile
#Out -> List of Fixtures (List of List)    
def getFixtures(fixtureFile):
    file = open(fixtureFile,"r")
    fixtures = file.readlines()
    fixtureList = []
    for fixture in fixtures:
        f = []
        fixture = fixture.strip()
        f = fixture.split(",")
        fixtureList.append(f)
    file.close()
    return fixtureList    

#Generate Output file
#In -> Input File
#Out -> Output File
def getOutputFile(inFile):
    file = os.getcwd() + "\\_betList\\betlist_" + inFile + ".xls"
    return file
    
#Get Input file from correct Directory
#In -> Text file string
#Out -> Location + file string    
def getInputFile(file):
    inFile = os.getcwd() + "\\fixtures\\fixtures_" + file + ".txt"
    return inFile



#Write bets to Excel
#In -> List of bets (Team1, Team2, Bet, Odds), Outfile
#Out -> None (Writes to Excel File)
def writeBets(betList, outFile):
    wb = Workbook()
    sheet1 = wb.add_sheet('Fixtures')
    sheet1.write(0, 0, "Home")
    sheet1.write(0, 1, "Away")
    sheet1.write(0, 2, "Bet")
    sheet1.write(0, 3, "Odds")
    sheet1.write(0, 4, "Tier")
    match = 1
    for bet in betList:
        if(bet[4] == "Gold"):
            sheet1.write(match, 0, bet[0])
            sheet1.write(match, 1, bet[1])
            sheet1.write(match, 2, bet[2])
            sheet1.write(match, 3, bet[3])
            sheet1.write(match, 4, bet[4])
            match += 1
    for bet in betList:
        if(bet[4] == "Silver"):
            sheet1.write(match, 0, bet[0])
            sheet1.write(match, 1, bet[1])
            sheet1.write(match, 2, bet[2])
            sheet1.write(match, 3, bet[3])
            sheet1.write(match, 4, bet[4])
            match += 1
    for bet in betList:
        if(bet[4] == "Bronze"):
            sheet1.write(match, 0, bet[0])
            sheet1.write(match, 1, bet[1])
            sheet1.write(match, 2, bet[2])
            sheet1.write(match, 3, bet[3])
            sheet1.write(match, 4, bet[4])
            match += 1
    for bet in betList:
        if(bet[4] == ""):
            sheet1.write(match, 0, bet[0])
            sheet1.write(match, 1, bet[1])
            sheet1.write(match, 2, bet[2])
            sheet1.write(match, 3, bet[3])
            sheet1.write(match, 4, bet[4])
            match += 1
    wb.save(outFile)


#Runs Full Algorithm
#In -> Team 1, Team2
#Out -> Returns Bet list
def runAlgorithm(team1, team2):
    url = makeUrl(team1, team2)
    page_contents = get_webpage(url)
    page_reduced = filter(page_contents)
    games = getGames(page_reduced, team1, team2)
    results = getResults(games, team1, team2)
    print(results)
    total = totalGames(results)
    odds = getOdds(results)
    bet = getBet(odds, total)
    outBet = team1, team2, bet[0], bet[1], bet[2]
    return outBet

def main(startDate):
    #Set File to System Argument
    fixturesFile = getInputFile(startDate)
    #Generate Output File
    outFile = getOutputFile(startDate)
    #print(outFile)
    #Get Fixtures
    fixtures = getFixtures(fixturesFile)
    print(fixtures)
    #Initialise dictionary with All teams in teams.txt
    initTeamDict()
	#Initialise Blank List of bets
    betList = []
	#For each game in Fixture list
    for game in fixtures:
		#Add Bet to List
        betList.append(runAlgorithm(game[0], game[1])) 
	#Write bets to CSV
    writeBets(betList, outFile)
	

    
    
    
    
if __name__ == "__main__":
	main()