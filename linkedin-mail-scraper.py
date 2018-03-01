#!/usr/bin/python

import json,httplib
import time
import re
import sys
from urllib2 import Request, urlopen  # Python 2
## Global variables:
# Counter for found users
count = 0
# Counter for names that need a manual check
count2 = 0 
# Holds persons with special character names on linkedin
needManual = []


def searchNames(data):
	global count
	global count2
	global needManual	
	searchData = ""
	for line in data.readlines():
		if "firstName" in line:
			searchData = line

	searchData = searchData.replace("&quot;",'\"')

        try:
            b = json.loads(searchData)
        except:
            return
        needManual = []
	for c in b["included"]:
		if "firstName" in c:
			d = json.dumps(c)
			d = json.loads(d)
			if "Belfius" in d["occupation"]: 
				# Remove spaces from names
				d["firstName"] = re.sub("[\ ]","",d["firstName"])
				d["lastName"] = re.sub("[\ ]","",d["lastName"])
				# Check if there are no other special characters
				if re.search("^[a-zA-Z\ -]+$", d["lastName"]):
					if re.search("^[a-zA-Z\ -]+$", d["firstName"]):
					    # Print the email adres
                                            try:
					        print str(d["firstName"]).lower() + "." + str(d["lastName"]).lower() + "@belfius.be," + str(d["occupation"]) 
                                            except:
					        print str(d["firstName"]).lower() + "." + str(d["lastName"]).lower() + "@belfius.be,Belfius"  

					else:
					    count2 = count2 + 1
					    needManual.append(d["firstName"] + " " + d["lastName"])
				else:
					count2 = count2 + 1
					needManual.append(d["firstName"] + " " + d["lastName"])
				count = count + 1


# Main loop to iterate over all the pages (max is apperently 100 so this makes max 1000 mail addresses)
for i in range(1,100):
	q = Request("https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%222515234%22%5D&facetGeoRegion=%5B%22be%3A4920%22%5D&origin=GLOBAL_SEARCH_HEADER&page=" + str(i))
	q.add_header('Cookie', 'bcookie="v=2&ab6aace1-af0b-49d0-8836-93a567f6dd7e"; bscookie="v=1&20180102134727b91b116a-47e7-4803-83a4-6676f3f2c070AQFbO6vPTMn3E8cRsYBqe1F--PDNkHr9"; JSESSIONID="ajax:4169467469122887069"; visit="v=1&M"; sl="v=1&hSLBB"; li_at=AQEDAQQ9z4UEiRygAAABYMaF00oAAAFg6pJXSk4Aze3CQTS3fQ_8nkwT-pBjWacv-CBYV1WGqLL3SUXno655pxccqX5XyixMux1x6JOw1ugMja_7JsFXyS9qZY07Ck9jIs_9TkRLhYuKJmGpg1aP-1sz; liap=true; _lipt=CwEAAAFg5STQU3p_7s5DoyHVgFbric_O9BEevGjsJKtRQh7ksNoAECejsVEB1mx4qkiLraAoi3q2c5W4OeMsgoJ5W6C_B8qbf_A-YYHOCwttvrwfru6PgcDlMqmauJW31xJbevzxcYXjgpb1pBOH9z-uHuo2IIYOhCunJiU0fj1wJQQFgMUS4AXwOL8O7ROvMbLNBN2u1nqnbEgyregS_-WNBVm5987AgtY5ghDQRNOYUt03ZFnb91A1w9LsZvXvmw2AjcSliIKYkKtST9hmGMF7wwyd1IedKrNekcEglUkrGl4pg3KdrctSpvfHwjdZoVw6EkrfOP4Ov5EFnOg; _ga=GA1.2.582980139.1515159151; lidc="b=TB85:g=914:u=95:i=1515672910:t=1515758854:s=AQGjd-2OuCQQfBjDWZd4Ezux1MQmFfT9"; lang="v=2&lang=en-us"')
	a = urlopen(q)
	searchNames(a)



print "\nFound " + str(count) + " accounts"
print "\n##############################################################\n" 
print str(count2) + " account need manual verification:"
for x in needManual:
    print x