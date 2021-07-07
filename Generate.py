import sys
import Fixtures
import Algorithm
import PDF
from datetime import datetime, timedelta
def main():
	#Work out days to get Fixtures
	days = int(sys.argv[1])
	dates = []
	for i in range(days):
		dates.append((datetime.today() + timedelta(i)).strftime('%Y-%m-%d'))
	startDate = dates[0]
	#Find fixtures
	Fixtures.main(dates)
	#Get bets
	Algorithm.main(startDate)
	#Create PDF
	PDF.main(startDate)

	#Check if tweet needed
	#print("Post to Twitter? (yes/no)")
	#twit = input()
	#if(twit == "yes"):
	#	Tweet.main(startDate)
	
if __name__ == "__main__":
	main()