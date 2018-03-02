# LinkedIn Mail Scraper
Useful python script to gather mail addresses from a specific company via LinkedIn. It basically makes regular HTTP request with a cookie containing the authentication to LinkedIn to search for people who set their current job to the company.  

# Usage
```
./linkedin-mail-scraper.py -k <keywords> -c <li_at_cookie> -d <domain>
 -k, --keywords  : Give the keywords to search for on LinkedIn
 -c, --cookie    : Set authentication cookie
    Provide the cookie value of li_at when having a valid session on LinkedIn

### Mail format ### 
 -d, --domain    : Domain after @
 -s, --separator : (optional) Give the separator (by default there is no separator)
 -f, --format    : (optional) Currently two hardcoded formats
    1: firstname<separator>lastname@... (default)
    2: lastname<separator>firstname@...

 -o, --output    : (optional) Output filename
    It outputs a csv file in the following format:
    firstname, lastname, emailaddress, Current position
 -h, --help      : This helpmenu

```

# Examples
Search for employees of Microsoft in format `firstname.lastname@microsoft.com` output to microsoft_targets.csv

```./linkedin-mail-scraper.py -k "Microsoft" -c AQEFAHA.....AXfUQ4ix -d microsoft.com -s . -o microsoft_targets.csv```

Search for employees of Microsoft in format `lastname.firstname@microsoft.com`

```./linkedin-mail-scraper.py -k "Microsoft" -c AQEFAHA.....AXfUQ4ix -d microsoft.com -s . -f 2```


# TODO
* Make filter more exact with facetCurrentCompany=["<company-ID>"]
* Deeper search to get limit the amount of pages of results by just filtering a bit more and going over all the possibilities
* Deal with special characters
* Make formatting more flexible

# Ideas
* Link it to HaveIBeenPwned for potential disclosure of credentials
