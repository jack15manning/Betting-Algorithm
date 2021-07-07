# Betting Algorithm

Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Example PDF](#example)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [Authors and history](#authors-and-history)


Introduction
------------

This is a simple betting algorithm that I created in my free time, and can be used to identify likely "Double-chance" bets which one could place on a betting site. It utilises the Information Retrieval techniques that I acquired during my University Second year module "Information Retrieval" and demonstrates my fluency with Python development. Executing this file locally will do the following:
* Identify any fixtures occuring in the following X days which feature two teams that this algorithm can predict - this is done using web crawling
* Use previous head-to-head data to determine the odds of each possible result occuring (Home Win, Draw, Away Win)
* Identify any fixtures which have a high likelihood of returning a winning Double Chance bet (1X - Home team to win or draw / 2X - Away team to win or draw)
* Generate a PDF which lists "Gold, Silver, and Bronze" fixtures which are suitable for a winning Double Chance bet


Installation
------------

Several libraries are required to use this betting algorithm and can be installed using the following commands in the command line:
* FPDF
```bash
pip install fpdf
```
* UrlLib
```bash
pip install urllib
```
* XLRD
```bash
pip install xlrd
```
* XLWT
```bash
pip install xlwt
```
* XLUtils
```bash
pip install xlutils
```

Usage
-----

To use this betting algorithm the following steps can be taken:
1. Clone this directory to your machine
2. Open a Powershell window in the downloaded folder
3. Enter the following line of code, where X is the number of days you would like to identify fixtures up to (5 = from today -> 5 days ahead)
```bash
python .\Generate.py X
```

Following the above steps will result in a PDF being generated in the betList folder under the name "BetList_DATE"

Only fixtures containing opposing teams in the "teams.txt" file will be predicted, more teams can be added by entering the name of the team followed by that teams ID on www.soccerbase.com

Example PDF
----------------------------

![Example PDF](/images/2020-11-16_BetList.PNG)

Known issues and limitations
----------------------------

**Limitations**
* The ability to automatically tweet the generated Bet List to Twitter has been disabled
* When selecting the number of days ahead to predict matches, large numbers can cause server errors. Try to keep this number below 10.


**Known Issues**
* N/A


Getting help
------------

If you have any issues with using the service, please send me an email at jack15manning@gmail.com

Contributing
------------

If you would like to make any changes to my system, clone the repository and make any additions you would like. 

Authors and history
---------------------------

This project was created by myself (Jack Manning).
