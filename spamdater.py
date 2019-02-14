# SpamDater
#
# parse out the email addresses (mine) and the dates email received
# Rob 2019-01-14
#
# Code smells due to lack of error checking, but is trying to work on highly structured data

import re, sys, getopt
import glob

print("SpamDater")

#sub for single file parsing
#Returns a dictionary of emails with date
def parsefile(filename, verbose):
  print("parsing", filename)
  resultshash = {}
  fh = open(filename,"r")
  emailset = set()
  gooddate = ''
  okdate = ''
  for line in fh:
    regex = '[-\w_.+]+@jumpstation\.co\.uk'
    matches = re.findall(regex,line, re.IGNORECASE)
    for match in matches:
      if verbose: 
        print(line,match)
      # add to set as unique string
      emailset.add(match)
    baseregex = '(Mon|Tue|Wed|Thu|Fri|Sat|Sun)?,?\s?[^0-9](\d{1,2})(-|\s)([A-Za-z]{3})(-|\s)(\d{4})[^0-9]'
    regex = 'Date:\s+' + baseregex
    match = re.search(regex,line)
    if match:
      day = paddate(str(match.group(2)))
      month3l = match.group(4)
      year = match.group(6)
      month = paddate(str(getmonth(month3l)))
      datestr = str(year) + '-' + str(month) + '-' + str(day)
      if verbose: 
        print('+', datestr)
      if not len(gooddate):
        gooddate = datestr
    else:
      match = re.search(baseregex,line)
      if match:
        day = paddate(str(match.group(2)))
        month3l = match.group(4)
        year = match.group(6)
        month = paddate(str(getmonth(month3l)))
        datestr = str(year) + '-' + str(month) + '-' + str(day)
        if verbose: 
          print("-",year,month,day)
        okdate = datestr
  fh.close()
  #print(datehash)
  for email in emailset:
    resultshash[email] = getbestdate(gooddate, okdate) 
  return resultshash

#get best date
def getbestdate(good, ok):
  if len(good):
    return good
  else:
    return ok

#convert three letter months to number
def getmonth(name):
  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  if name.title() in months:
    return(1+months.index(name.title())) # title() makes 'Feb','feb','FEB' all 'Feb'
  else:
    return('XX')

#pad single digits to double, must be a built in way
def paddate(numstr):
  if len(numstr) == 1:
    return '0' + str(numstr)
  else:
    return numstr

#sub for list of files
def parsefiles(pattern, log, verbose):
  for filename in glob.glob(pattern):
    logresults(parsefile(filename, verbose), log)

#log results of parsing
def logresults(results, filename):
  fh = sys.stdout
  if len(filename):
    fh = open(filename, 'a')
  for result in results:
    fh.write('"' + result + '", "' + results[result] + '"\n')
  if len(filename):
    fh.close()

#getfilenames("")
def usage():
  print('Usage: --file="file in" --log="file to log to"')
  print('Usage: --directory="path/glob*" --log="file to log to"')

try:
  opts, args = getopt.getopt(sys.argv[1:], 'f:l:d:hv', ['directory=', 'file=', 'log=', 'help', 'verbose'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
verbose=False
log=''
filename=''
globpattern=''
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-f', '--file'):
    filename = arg
  elif opt in ('-l', '--log'):
    log = arg
  elif opt in ('-d', '--directory'):
    globpattern = arg
  elif opt in ('-v', '--verbose'):
    verbose=True
  else:
    usage()
    sys.exit(2)

if verbose:
  print('Filename', filename)
  print('Glob pattern', globpattern)
  print('Log file', log)

if len(filename):
  logresults(parsefile(filename, verbose), log)
elif len(globpattern):
  parsefiles(globpattern, log, verbose)  
