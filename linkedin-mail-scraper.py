#! /usr/bin/python
# Written by Vinnie Vanhoecke
import json,httplib
import time
import re
import sys, getopt
from urllib2 import Request, urlopen
import urllib

## Global variables:
# Request parameters
search = ''
authcookie = ''
# Boolean to see end of the pages
endReached = False
# Hold persons found with no special character on LinkedIn
loot = []
# Holds persons with special character names on LinkedIn
needManual = []
# Mail formating
domain = ""
separator = ""
format = "1"
# Output filename
output = "output.csv" 

def help():
	print "##########################################"
	print "./linkedin-mail-scraper.py -k <keywords> -c <li_at_cookie> -d <domain>"
	print " -k, --keywords  : Give the keywords to search for on LinkedIn"
	print " -c, --cookie    : Set authentication cookie"
	print "    Provide the cookie value of li_at when having a valid session on LinkedIn"
	print "\n### Mail format ###"
	print " -d, --domain    : Domain after @"
	print " -s, --separator : (optional) Give the separator (by default there is no separator)"
	print " -f, --format    : (optional) Currently two hardcoded formats"
	print "    1: firstname<separator>lastname@... (default)"
	print "    2: lastname<separator>firstname@..."
	print "\n -o, --output    : (optional) Output filename"
	print " -h, --help      : This helpmenu"
	print "\n### Example ###"
	print "# Search for employees of Microsoft in format firstname.lastname@microsoft.com output to microsoft_targets.csv"
	print " ./linkedin-mail-scraper.py -k \"Microsoft\" -c AQEFAHA.....AXfUQ4ix -d microsoft.com -s . -o microsoft_targets.csv"
	print "# Search for employees of Microsoft in format lastname.firstname@microsoft.com"
	print " ./linkedin-mail-scraper.py -k \"Microsoft\" -c AQEFAHA.....AXfUQ4ix -d microsoft.com -s . -f 2"
	print "##########################################"

def searchNames(data):
	# Global variables
	global count,needManual,search,domain,separator,format,output,loot,endReached
	# Local variables	
	searchData = ""
	
	# Only get the line with the actual searchdata
	for line in data.readlines():
		if ":&quot;GLOBAL_SEARCH_HEADER&quot;," in line:
			searchData = line
	# Fix quotings
	searchData = searchData.replace("&quot;",'\"')

	# Convert to json data
	try:
		json_data = json.loads(searchData)
	except:
		print "Error occured when parsing the response from linkedin"
		return 
	# To check for end reached
	if len(json_data["included"]) == 0:
		endReached = True
	for data_line in json_data["included"]:
		# Filter out profile data and 
		if "firstName" in data_line:
			profile_data = json.dumps(data_line)
			profile_data = json.loads(profile_data)
			# Filter again on the search keyword because its gives false positives
			if not search in profile_data["occupation"].lower():
				continue 
			# Remove spaces from names
			profile_data["firstName"] = re.sub("[\ ]","",profile_data["firstName"]).lower()
			profile_data["lastName"] = re.sub("[\ ]","",profile_data["lastName"]).lower()
			# Check if there are no other special characters
			if not re.search("^[a-zA-Z\ -]+$", profile_data["lastName"] + profile_data["firstName"] + profile_data["occupation"]):
				needManual.append(profile_data["firstName"] + " " + profile_data["lastName"]) 
				continue
			# Get more false positives out of it
			if profile_data["firstName"] == "" or profile_data["lastName"] == "": 
				continue
			# Save the information
			if format == "1":
 				loot.append(str(profile_data["firstName"]) + "," + str(profile_data["lastName"])  + "," + str(profile_data["firstName"]) + separator + str(profile_data["lastName"]) + "@" + domain + "," + str(profile_data["occupation"]))
 			elif format == "2":
 				loot.append(str(profile_data["firstName"]) + "," + str(profile_data["lastName"])  + "," +str(profile_data["lastName"]) + separator + str(profile_data["firstName"]) + "@" + domain + "," + str(profile_data["occupation"]))


# Get the parameters
def main(argv):
	global search,authcookie,domain,separator,format,output
	if len(argv) == 0:
		help()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,"hk:c:d:s:f:o:h",["keywords=","cookie=","domain=","separator=","format=","output=","help"])
	except getopt.GetoptError:
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-k", "--keywords"):
			search = arg.lower()
		elif opt in ("-c", "--cookie"):
			authcookie = arg 
		elif opt in ("-d", "--domain"):
			domain = arg
		elif opt in ("-s", "--separator"):
			separator = arg
		elif opt in ("-f", "--format"):
			format = arg
		elif opt in ("-o", "--output"):
			output = arg
		elif opt in ("-h", "--help"):
			help()
			sys.exit()
	print search


if __name__ == "__main__":
    main(sys.argv[1:])


# Main loop to iterate over all the pages (max is apperently 100 so this makes max 1000 mail addresses)
for i in range(1,100):
	url = "https://www.linkedin.com/search/results/index/?" + urllib.urlencode({"keywords":search,"origin":"GLOBAL_SEARCH_HEADER","page":i}) 
	reqGetEmployees = Request(url)
	reqGetEmployees.add_header('Cookie', 'li_at="' + authcookie + '";')
	print "[PAGE " + str(i) + "] " + url
	response = urlopen(reqGetEmployees)
	searchNames(response)
	if endReached:
		print "[END reached]"
		break


# Results
print "\n##############################################################\n" 
print "\nFound " + str(len(loot)) + " accounts"
print str(len(needManual)) + " account need manual verification:"
for x in needManual:
    print x
output_file = open(output,"w+")
for x in loot:
	output_file.write(x + "\n")
output_file.close()
