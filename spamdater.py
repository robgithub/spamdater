# SpamDater
#
# parse out the email addresses (mine) and the dates email received
# Rob 2019-01-14
#
# Code smells due to lack of error checking, but is trying to work on highly structured data

import re

print("SpamDater")

#sub for single file parsing
#Returns a dictionary of emails with date
def parsefile(filename):
  print("parsing", filename)
  resultshash = {}
  fh = open(filename,"r")
  emailset = set()
  datehash = {}
  for line in fh:
    regex = '[-\w_.+]+@jumpstation\.co\.uk'
    matches = re.findall(regex,line, re.IGNORECASE)
    for match in matches:
      #print(line,match)
      # add to set as unique string
      emailset.add(match)
    regex = 'Date:\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)?,?\s?(\d{1,2})\s(\w{3})\s(\d{4})'
    match = re.search(regex,line)
    if match:
      day = paddate(str(match.group(2)))
      month3l = match.group(3)
      year = match.group(4)
      month = paddate(str(getmonth(month3l)))
      datestr = str(year) + '-' + str(month) + '-' + str(day)
      #print(datestr)
      datehash[datestr]='Best'
    else:
      regex = '(Mon|Tue|Wed|Thu|Fri|Sat|Sun)?,?\s?(\d{1,2})\s(\w{3})\s(\d{4})'
      match = re.search(regex,line)
      if match:
        day = paddate(str(match.group(2)))
        month3l = match.group(3)
        year = match.group(4)
        month = paddate(str(getmonth(month3l)))
        datestr = str(year) + '-' + str(month) + '-' + str(day)
        #print("-",year,month,day)
        if not datehash.has_key(datestr):
          datehash[datestr]='OK'
  fh.close()
  #print(datehash)
  for email in emailset:
    resultshash[email] = datestr
  return resultshash

#convert three letter months to number
def getmonth(name):
  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return(1+months.index(name))

#pad single digits to double, must be a built in way
def paddate(numstr):
  if len(numstr) == 1:
    return '0' + str(numstr)
  else:
    return numstr

#sub for list of files
def getfilenames(pattern):
  fn = 'test.dat'
  logresults(parsefile("/home/rednuht/Mail/Black list/spamassassin/23458"), fn)
  logresults(parsefile("/home/rednuht/Mail/Black list/spamassassin/29152"), fn)

#log results of parsing
def logresults(results, filename):
  fh = open(filename, 'a')
  for result in results:
    fh.write('"' + result + '", "' + results[result] + '"\n')
  fh.close()


getfilenames("")
