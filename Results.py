import xlrd
import sys
import re
import xlwt
import urllib.request
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy


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
   
#Retrieves last Played Game
#In -> Clean Html, Team1, Team2
#Out -> Single Game
def getLast(content, team1, team2):
	games = re.findall(r"("+team1+")\s(\d{1})\s\-\s(\d{1})\s("+team2+")", content)
	game = games[0]
	return game

def main():
	#Get Date from Console In
	date = sys.argv[1]
	#Get Filename
	file = "_betList/betlist_{0}.xls".format(date)
	#Initialise dictionary with All teams in teams.txt
	initTeamDict()
	
	#Create counter variables
	goldMatches = 0
	goldWins = 0
	silverMatches = 0
	silverWins = 0
	bronzeMatches = 0
	bronzeWins = 0
	#Create list of wins variable
	wins = []
	#Open Excel File
	wb = xlrd.open_workbook(file)
	#Get First Sheet
	sheet = wb.sheet_by_index(0)
	#Find number of rows
	rows = sheet.nrows
	#For each Row
	for i in range(rows):
		#If not first row (Column Names)
		if(i != 0):
			#If Game with Bet
			if(sheet.cell_value(i, 4) != ""):
				#Get Team Names
				t1 = sheet.cell_value(i, 0)
				t2 = sheet.cell_value(i, 1)
				#Make Url
				url = makeUrl(t1, t2)
				#Get Page Content
				page = get_webpage(url)
				#Find last played Game
				match = getLast(page, t1, t2)
				#Convert to List
				game = list(match)
				print(game)
				#Create result variable
				result = 0
				#Determine result
				if(game[1] > game[2]):
					result = 1
				elif(game[2] > game[1]):
					result = 2
				else:
					result = 3
				win = False
				#Get Bet
				bet = sheet.cell_value(i, 2)
				#Check if bet won
				if(result == 1):
					if(bet == "1X"):
						win = True
					else:
						win = False
				elif(result == 2):
					if(bet == "2X"):
						win = True
					else:
						win = False
				else:
					win = True
				wins.append(win)
				#Get Bet Tier
				tier = sheet.cell_value(i, 4)
				#Increase Counter variables
				if(tier == "Gold"):
					goldMatches += 1
					if(win):
						goldWins += 1
				elif(tier == "Silver"):
					silverMatches += 1
					if(win):
						silverWins += 1
				elif(tier == "Bronze"):
					bronzeMatches += 1
					if(win):
						bronzeWins += 1
			
	#Output Results
	print("Gold: {0}:{1}".format(goldMatches, goldWins))
	print("Silver: {0}:{1}".format(silverMatches, silverWins))
	print("Bronze: {0}:{1}".format(bronzeMatches, bronzeWins))
	
	#Write results
	rb = open_workbook(file)
	wb = copy(rb)
	sheet = wb.get_sheet(0)
	sheet.write(0, 5, "Result")
	counter = 1
	for result in wins:
		string = ""
		if(result):
			string = "Win"
		else:
			string = "Loss"
		sheet.write(counter, 5, string)
		counter += 1
	wb.save(file)
	
	
	print("Update Win-rates (yes/no)")
	update = input()
	if(update == "yes"):
		outFile = "Tier_Winrate.xls"
		#Update Tier winrates
		rb = xlrd.open_workbook(outFile)
		sheet = rb.sheet_by_index(0)
		#Get Current WinRates
		bPlayed = int(sheet.cell_value(1,1))
		bWins = int(sheet.cell_value(1,2))
		sPlayed = int(sheet.cell_value(2,1))
		sWins = int(sheet.cell_value(2,2))
		gPlayed = int(sheet.cell_value(3,1))
		gWins = int(sheet.cell_value(3,2))
		#Calculate New Win Rates
		newBPlayed = bPlayed + bronzeMatches
		newBWins = bWins + bronzeWins
		newSPlayed = sPlayed + silverMatches
		newSWins = sWins + silverWins
		newGPlayed = gPlayed + goldMatches
		newGWins = gWins + goldWins
		
		outFileName = "Tier_Winrate.xls"
		rb2 = open_workbook(outFile)
		wb = copy(rb2)	
		sheet = wb.get_sheet(0)
		sheet.write(1,1, newBPlayed)
		sheet.write(1,2, newBWins)
		sheet.write(2,1, newSPlayed)
		sheet.write(2,2, newSWins)
		sheet.write(3,1, newGPlayed)
		sheet.write(3,2, newGWins)
		wb.save(outFileName)
		
		
	

				
				

if __name__ == "__main__":
	main()