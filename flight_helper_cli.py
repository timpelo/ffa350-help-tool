#===================================================================#
# Copyright Jani Timonen 2017										#
#																	#
# star_to_fms is small program used to convert NavData				#
# into valid FMS files used by X-Plane flight simulator.			#
# NavData is commercial data provided by Navigraph. NavData			#
# has updated infromation for all aviational waypoints, airports	#
# airport runways etc. This data is updated every month				#
#===================================================================# 

# Imports.
import sys
import os
import re
from prettytable import PrettyTable

# Global variables.
__OUTPUT_FILE__='../Games/X-Plane 11/Output/FMS plans/'
__AIRPORT_FILE__ = '../Games/X-Plane 11/Custom Data/GNS430/navdata/Airports.txt'
__ICAO_FOLDER__ = '../Games/X-Plane 11/Custom Data/GNS430/navdata/Proc/'
__ICAO__ = "EFHK"
__RWY__ = "04L"
__STAR__ = "DIVA1B"
__START_OF_STAR__ = False
__START_OF_FINAL__ = False
__NRO_OF_STAR_WP__ = 0
__CORRECT_AIRPORT__ = False


# Builds dictionary depending given waypoint type. Dictionary
# contains key and index of key in give data line from file.
def getMap(type):
	dict = {}
	if type=='TF':
		dict = {
		'type' : '3',
		'alt' : 11,
		'name' : 1,
		'lat' : 2,
		'lon' : 3,
		}
	if type=='IF':
		dict = {
		'type' : '3',
		'alt' : 8,
		'name' : 1,
		'lat' : 2,
		'lon' : 3,
		}
	
	if type=='CF':
		dict = {
		'type' : '2',
		'alt' : 11,
		'name' : 1,
		'lat' : 2,
		'lon' : 3,
		}
	
	if type=='A':
		dict = {
		'type' : '1',
		'alt' : 5,
		'name' : 1,
		'lat' : 3,
		'lon' : 4,
		}
	
	if type=='STAR':
		dict = {
		'name' : 1,
		'rwy' : 2,
		}
		
	if type=='FINAL':
		dict = {
		'rwy' : 1,
		}
	if type=='ILS':
		dict = {
		'frequency' : 6,
		'course' : 7
		}
	return dict

# Clears output file. Also adds mandatory version info
# at the start of file.
def clearOutputFile():
	if not os.path.exists("../Games/X-Plane 11/Output/FMS plans/"+__ICAO__):
		os.makedirs("../Games/X-Plane 11/Output/FMS plans/"+__ICAO__)
		
	print __OUTPUT_FILE__
	with open(__OUTPUT_FILE__, 'w+') as file:
		file.write('I\n\n3 version\n\n1\n\n6\n\n')
	
# Writes given waypoint to file.
def writeToFile(waypoint):
	with open(__OUTPUT_FILE__, 'a') as file:
		file.write(waypoint+'\n\n')

# Confirms that given STAR waypoint is correct. It should have correct
# name and it should lead to correct runway.
def confirmCorrectStar(array):
	map = getMap('STAR')

	correctStar = False
	correctRwy = False
	
	name = array[map['name']]
	rwy = array[map['rwy']]

	if name == __STAR__:
		correctStar = True
	if rwy == __RWY__  or rwy == "ALL":
		correctRwy = True
		
	if correctRwy and correctStar:
		global __NRO_OF_STAR_WP__
		__NRO_OF_STAR_WP__ += 1
		return True
	else:
		return False

# Confirms that given FINAL waypoint is correct. It should
# lead to correct runway.
def confirmCorrectFinal(array):
	map = getMap('FINAL')

	correctFinal = False
	rwy = array[map['rwy']]

	if rwy == 'L'+__RWY__:
		correctFinal = True
		
	if correctFinal:
		return True

# Confirms that given argument is not malformed with given code type.
def confirmArgument(argument, type):
	result = False
	
	if type == "ICAO":
		pattern = re.compile("[A-Z]{4}$") #Four capital letters.
		result = pattern.match(argument)
	elif type == "RWY":
		pattern = re.compile("((^0[1-9])((L|R|C|)$)|(^1[1-9])((L|R|C|)$)|(^2[0-9])((L|R|C|)$)|(^3[0-6])((L|R|C|)$))") #Number between 01 and 36 (leading zeroes must) and end with L,R,C or nothing.
		result = pattern.match(argument)
	elif type == "STAR":
		pattern = re.compile("^[A-Z]{3,4}[0-9][A-Z]$") #Four or three capital letters, number from 0-9 and one capital letter.
		result = pattern.match(argument)
	return result
	
# Creates STAR waypoint using generated dictionary. Picks correct values
# from data line using indexes found from generated dictionary.	
def createStarWp(array, type):
	map = getMap(type)
	if map:
		wpType= map['type']
		name = array[map['name']]
		lat = array[map['lat']]
		lon = array[map['lon']]
		alt = array[map['alt']]
		
		waypoint = wpType + ' '
		waypoint += name + ' '
		waypoint += alt + ' '
		waypoint += lat + ' '
		waypoint += lon + ' '
		
		writeToFile(waypoint)
		print "Wrote STAR waypoint: ", waypoint
	
# Creates FINAL waypoint using generated dictionary. Picks correct values
# from data line using indexes found from generated dictionary.
def createFinalWp(array, type):
	map = getMap(type)
	if map:
		wpType= map['type']
		name = array[map['name']]
		lat = array[map['lat']]
		lon = array[map['lon']]
		alt = array[map['alt']]

		waypoint = wpType + ' '
		waypoint += name + ' '
		waypoint += alt + ' '
		waypoint += lat + ' '
		waypoint += lon + ' '
		
		writeToFile(waypoint)
		print "Wrote FINAL waypoint: ", waypoint
	
# Creates AIRPORT waypoint using generated dictionary. Picks correct values
# from data line using indexes found from generated dictionary.
def createDestWp(array, type):
	map = getMap(type)
	if map:
		wpType= map['type']
		name = array[map['name']]
		lat = array[map['lat']]
		lon = array[map['lon']]
		alt = array[map['alt']]

		if name==__ICAO__:
			waypoint = wpType + ' '
			waypoint += name + ' '
			waypoint += alt + ' '
			waypoint += lat + ' '
			waypoint += lon + ' '
			
			writeToFile(waypoint)
			print "Wrote AIRPORT waypoint: ", waypoint
	
# Processes given line. Checks that it is valid by using information given
# by user. Then generates waypoint and writes it into the file.
def processLine(line):
	count = line.count(',')
	array = line.split(',', count)
	type=array[0];
	
	global __START_OF_STAR__
	global __START_OF_FINAL__
	
	#Reset if newline.
	if type=='\n':
		__START_OF_STAR__ = False
		__START_OF_FINAL__ = False
			
	#Create waypoint if line is correct.
	if __START_OF_STAR__:
		createStarWp(array, type)
	
	if __START_OF_FINAL__:
		if __NRO_OF_STAR_WP__ > 0:
			createFinalWp(array, type)
		else:
			print "No STAR waypoints before FINAL. STAR is missing."
			print "NO STAR file created. Exiting program!"
			sys.exit(1)
	
	#Check type.
	if type=='A':
		createDestWp(array, type)
	elif type=='STAR':
		correct = confirmCorrectStar(array)
		if correct:
			__START_OF_STAR__= True
	elif type=='FINAL':
		correct = confirmCorrectFinal(array)
		if correct:
			__START_OF_FINAL__=True

def readAirportLine(line):
	global __CORRECT_AIRPORT__
	count = line.count(',')
	
	if count==0:
		return
		
	array = line.split(',', count)
	airportOrRwy = array[1]
	
	if __CORRECT_AIRPORT__:
		if airportOrRwy==__RWY__:
			map = getMap('ILS')
			freq = array[map['frequency']]
			course = array[map['course']]
			
			clearConsole()
			print "Info for " + __ICAO__ + " runway " + __RWY__ + " ILS:"
			print "Frequency: " + freq
			print "Course:    " + course
			__CORRECT_AIRPORT__ = False
			
	
	
	if airportOrRwy==__ICAO__:
		__CORRECT_AIRPORT__ = True
	

def printInfo(f, typeToList, runwayToList):
	table = PrettyTable(['TYPE', 'NAME', 'RUNWAY'])
	for line in f:
		lineArray = line.split(',')
		arrayCount = line.count(',')
		
		#STAR to table
		
		if typeToList=="STAR" or typeToList=="ALL":
			if lineArray[0]=="STAR":
				runways = ""
				for i in range(2, arrayCount):
					runways += lineArray[i] + " "
					
				if runwayToList == "ALL" or runwayToList.strip()==runways.strip() or runways.strip()=="ALL":
					table.add_row(['STAR', lineArray[1], runways])
		#SID to table
		if typeToList=="SID" or typeToList=="ALL":
			if lineArray[0]=="SID":
				runways = ""
				for i in range(2, arrayCount):
					runways += lineArray[i] + " "
				if runwayToList == "ALL" or runwayToList.strip()==runways.strip() or runways.strip()=="ALL":
					table.add_row(['SID', lineArray[1], runways])
			
	clearConsole()
	print table

	
##------- EXECUTE FUNCTIONS ---------##
def executeList():
	print "Give ICAO:"
	rawInput = raw_input()
	__ICAO__ = rawInput
	
	typeToList = 'ALL'
	runwayToList = 'ALL'
	
	print "SID or STAR (Hit enter for both):"
	rawInput = raw_input()
	if len(rawInput)>0:
		typeToList=rawInput
		
	print "Runway (Hit enter for both):"
	rawInput = raw_input()
	if len(rawInput)>0:
		runwayToList=rawInput
	
		
	
	correctArgs = False
	if not confirmArgument(__ICAO__, "ICAO"):
		print "Malformed ICAO! Correct format is 4 digit airport ICAO code (i.e EGLL for London Heathrow)\n"
	else:
		correctArgs = True
	
	#Repeat for correct ICAO
	while not correctArgs:
		rawInput = raw_input()
		__ICAO__ = rawInput
		if not confirmArgument(__ICAO__, "ICAO"):
			print "Malformed ICAO! Correct format is 4 digit airport ICAO code (i.e EGLL for London Heathrow)\n"
		else:
			correctArgs = True
			
	#Read file for listing
	with open(__ICAO_FOLDER__+__ICAO__+'.txt', 'rU') as f:
		printInfo(f, typeToList, runwayToList)
		
	print("\n\n")
	showMenu()
	
def executeSid():
	print "TODO"
	
def executeILS():
	global __ICAO__
	global __RWY__
	
	print "Give ICAO and runway:"
	rawInput = raw_input()
	inputArray = rawInput.split()
	
	#Check amount of given arguments.
	if len(inputArray) < 2:
		print "Please use ICAO RUNWAY (using 4 letter name)\n"
		print "EFHK 04L\n"
		sys.exit(1)
	
	#Set arguments to globals.
	else:
		__ICAO__ = inputArray[0].upper()
		__RWY__ = inputArray[1].upper()
		
	correctArgs = True
	if not confirmArgument(__ICAO__, "ICAO"):
		print "Malformed ICAO! Correct format is 4 digit airport ICAO code (i.e EGLL for London Heathrow)\n"
		correctArgs = False
	
	if not confirmArgument(__RWY__, "RWY"):
		print "Malformed runway! Correct format is 2 digits and optional L, R or C (i.e 04L)\n"
		correctArgs = False
	
	if not correctArgs:
		executeILS()

	#AIRPORT waypoint.	
	with open(__AIRPORT_FILE__, 'rU') as f:
		for line in f:
			readAirportLine(line)
	
	print("\n\n")
	showMenu()
	
def executeStar():
	global __OUTPUT_FILE__
	global __ICAO__
	global __RWY__
	global __STAR__
	
	print "Give STAR (ICAO, Runway, STAR):"
	rawInput = raw_input()
	inputArray = rawInput.split()
	
	#Check amount of given arguments.
	if len(inputArray) < 3:
		print "Please use ICAO RUNWAY STAR (using 4 letter name)\n"
		print "EFHK 04L DIVA1B\n"
		sys.exit(1)
	
	#Set arguments to globals.
	else:
		__ICAO__ = inputArray[0].upper()
		__RWY__ = inputArray[1].upper()
		__STAR__ = inputArray[2].upper()
		__OUTPUT_FILE__ += __ICAO__+'/STAR_'+__ICAO__+__RWY__+'_'+__STAR__+'.fms' 
		
	correctArgs = True
	if not confirmArgument(__ICAO__, "ICAO"):
		print "Malformed ICAO! Correct format is 4 digit airport ICAO code (i.e EGLL for London Heathrow)\n"
		correctArgs = False
	
	if not confirmArgument(__RWY__, "RWY"):
		print "Malformed runway! Correct format is 2 digits and optional L, R or C (i.e 04L)\n"
		correctArgs = False
		
	if not confirmArgument(__STAR__, "STAR"):
		print "Malformed STAR! Correct format is 3 or 4 digits as name and number + letter for code (i.e DIVA1B for DIVAM 1B approach)\n"
		correctArgs = False
		
	if not correctArgs:
		executeStar()

	#Clear outpit file.
	clearOutputFile()

	#STAR and FINAL waypoints.
	with open(__ICAO_FOLDER__+__ICAO__+'.txt', 'rU') as f:
		for line in f:
			processLine(line)
			
	#AIRPORT waypoint.	
	with open(__AIRPORT_FILE__, 'rU') as f:
		for line in f:
			processLine(line)
	
	print("\n\n")
	showMenu()

def clearConsole():
	_=os.system('cls')
	
# Main.
def showMenu():
	print "1. List SID/STAR"
	print "2. Generate SID"
	print "3. Generate STAR"
	print "4. ILS Info"
	print "5. Exit"
	
	command = input()
	
	if command==1:
		clearConsole()
		executeList()
	if command==2:
		clearConsole()
		executeSid()
	if command==3:
		clearConsole()
		executeStar()
	if command==4:
		clearConsole()
		executeILS()
	if command==5:
		print "Bye! Have a safe flight!"
		sys.exit(1);
if __name__ == "__main__":
	clearConsole()
	showMenu()
	
	
	
#END OF FILE
