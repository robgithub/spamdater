#Collate.py
#
#Rob 2019-02-14
#
#Part of the spamdater investigate.
#Reads a csv(-ish) file and outputs the date a new email address appears

import re

filename = 'data.sorted'

fh = open(filename, 'r')
lastemail = ''
for line in fh:
  #print(line)
  match = re.search('"([^"]+)", "([^"]*)"', line)
  date = match.group(2)
  email = match.group(1)
  if email != lastemail:
    print(date,email)
    lastemail = email
fh.close()
