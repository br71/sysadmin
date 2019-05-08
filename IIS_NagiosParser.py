import re,os.path,sys,datetime

#Time
t1 = '{0:%y%m%d}'.format(datetime.datetime.now())

#Files and search string in HTTP request
tmpFile = 'C:\\log\\tmpCounter'+ t1 + '.txt'
logfile = 'C:\\inetpub\\logs\\LogFiles\\W3SVC1\\u_ex' + t1 + '_x.log'
searchString = 'some_string_in_url'


#Creating temp file to track checked lines in log file
if not os.path.exists(tmpFile):
    with open(tmpFile,'w') as t:
        t.write('0')

if not os.path.exists(logfile ):
    print('Log file does not exist'.format(logfile))
    sys.exit(1)

#Regexp for searched string: 200 0 0 218 => time of execution (218 ms, last value)
regex1 = re.compile(r'\s([0-9]+)\s([0-9]+)\s([0-9]+)\s([0-9]+)\s')

#Line counter
c = 0

#Event counters
j = 0
m = 0

#Time execution array
timeExcecute = []

#Reading line in temp file where to start counting events (point where  parsing stopped in previous check)
with open(tmpFile,'r') as t:
    intl1 = int(t.readline())

#Parsing log file
with open(logfile,'r') as logIIS:
    for line in logIIS:
        #If line count is bigger and equal than point of last check time of executions will be added to array
        if c >= intl1 :
            if searchString in line:
                r1 = regex1.search(str(line))
                timeExcecute.append(int(r1.group(4)))
        c += 1

#Longer execution time count
for k in timeExcecute:
    if k >= 30000:
        m += 1

#Shorter execution time count (in miliseconds)
for i in timeExcecute:
    if i >= 5000:
        j += 1

#Writing count of checked lines in log file, next check counting of critical events will start from this line
with open(tmpFile,'w') as t:
    t.write(str(c))

#Nagios plugin related part
if m >= 5:
    print('URL {} execution time (30000 ms) is CRITICAL'.format(searchString))
    sys.exit(2)

if m >= 3 and m < 5:
    print('URL {} execution time (30000 ms) is WARNING'.format(searchString))
    sys.exit(1)

if j >= 30:
    print('URL {} execution time (5000 ms) is CRITICAL'.format(searchString))
    sys.exit(2)

if j >= 20 and j < 30:
    print('URL {} execution time (5000 ms) is WARNING'.format(searchString))
    sys.exit(1)

else:
    print('URL {} execution time is OK'.format(searchString))
    sys.exit(0)








