from fpdf import FPDF
import xlrd
import sys
class PDF(FPDF):
    def header(self):
        # Logo
        #self.image('Logo.JPG', 10, 8, 200)
        # Arial bold 15
        self.set_font('Arial', 'B', 20)
        self.set_fill_color(255, 0, 0)
        self.set_text_color(255, 255, 255)
        # Title
        self.cell(190, 10, 'Jack\'s Bet Club', 1, 0, 'C', True)
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def main(startDate):
	#Get System Argument
	print(startDate)
	#Predefined Bet File
	betDoc = "_betlist/betlist_{0}.xls".format(startDate)
	#Get Gold matches
	gold = []
	silver = []
	bronze = []
	wb = xlrd.open_workbook(betDoc)
	sheet = wb.sheet_by_index(0)
	rows = sheet.nrows
	#For each Row
	for i in range(rows):
		#If not first row (Column Names)
		if(i != 0):
			#Check Tier
			if(sheet.cell_value(i, 4) == "Gold"):
				#Add to Gold List
				bet = []
				bet.append(sheet.cell_value(i, 0))
				bet.append(sheet.cell_value(i, 1))
				bet.append(sheet.cell_value(i, 2))
				gold.append(bet)
			elif(sheet.cell_value(i, 4) == "Silver"):
				#Add to Silver
				bet = []
				bet.append(sheet.cell_value(i, 0))
				bet.append(sheet.cell_value(i, 1))
				bet.append(sheet.cell_value(i, 2))
				silver.append(bet)
			elif(sheet.cell_value(i, 4) == "Bronze"):
				#Add to Bronze
				bet = []
				bet.append(sheet.cell_value(i, 0))
				bet.append(sheet.cell_value(i, 1))
				bet.append(sheet.cell_value(i, 2))
				bronze.append(bet)



	#Get Win rates
	file = ("Tier_Winrate.xlsx")
	wb = xlrd.open_workbook(file)
	sheet = wb.sheet_by_index(0)
	bronzeWin = str(round(sheet.cell_value(1,3), 2))
	silverWin = str(round(sheet.cell_value(2,3), 2))
	goldWin = str(round(sheet.cell_value(3,3), 2))
	bronzeString = 'Bronze: {0}%'.format(bronzeWin)
	silverString = 'Silver: {0}%'.format(silverWin)
	goldString = 'Gold: {0}%'.format(goldWin)

	# Instantiation of inherited class
	pdf = PDF()
	pdf.alias_nb_pages()
	pdf.add_page()
	
	pdf.add_font('sysfont', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)
	
	pdf.set_font('Times','B', 15)
	pdf.cell(190, 10, 'Algorithm', 0, 1, 'C')
	pdf.set_font('Times', '', 12)
	pdf.cell(190, 5, 'My algorithm analyses past head-to-head results to determine which team is more likely to win the fixture and', 0, 1)
	pdf.cell(190, 5, 'how likely this predicted result is to occur. If the probability of a result is high enough a bet will be calculated', 0, 1)
	pdf.cell(190, 5, 'as either 1X or 2X where 1X indicates Team 1 to Win or Draw and 2X indicates Team 2 to Win or Draw.', 0, 1)
	pdf.set_font('Times', 'B', 15)
	pdf.cell(190, 10, 'Current Success Rates:', 0, 1, 'C') 
	pdf.set_font('Times', '', 12)
	pdf.cell(190, 5, bronzeString, 0, 1, 'C')
	pdf.cell(190, 5, silverString, 0, 1, 'C')
	pdf.cell(190, 5, goldString, 0, 1, 'C')
	pdf.set_font('Times', 'B', 15)
	pdf.cell(190, 10, 'Gold Bets:', 0, 1, 'C')
	pdf.set_font('Times', '', 12)
	for bet in gold:
		teams = '{0} vs {1}'.format(bet[0], bet[1])
		pdf.cell(95, 5, teams, 0, 0, 'R')
		pdf.cell(20, 5, bet[2], 0, 1, 'R')
	pdf.set_font('Times', 'B', 15)
	pdf.cell(190, 10, 'Silver Bets:', 0, 1, 'C')
	pdf.set_font('Times', '', 12)
	for bet in silver:
		teams = '{0} vs {1}'.format(bet[0], bet[1])
		pdf.cell(95, 5, teams, 0, 0, 'R')
		pdf.cell(20, 5, bet[2], 0, 1, 'R')
	pdf.set_font('Times', 'B', 15)
	pdf.cell(190, 10, 'Bronze Bets:', 0, 1, 'C')
	pdf.set_font('Times', '', 12)
	for bet in bronze:
		teams = '{0} vs {1}'.format(bet[0], bet[1])
		pdf.cell(95, 5, teams, 0, 0, 'R')
		pdf.cell(20, 5, bet[2], 0, 1, 'R')
		
	pdf.output('_betlist/BetList_{0}.pdf'.format(startDate), 'F')

if __name__ == "__main__":
	main()