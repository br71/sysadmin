import os.path,sys,psycopg2,datetime

#Connect to database
conn = psycopg2.connect("dbname=***** user=***** host=***** password=****")
cur = conn.cursor()
c = 0

t1 = '{0:%y%m%d}'.format(datetime.datetime.now())

#Temporary file. Script load logs (scheduled task, cron job ...) in databases in every 5-10 minutes.
#At every next check only new log lines will be inserted in database.
tmpFile = 'C:\\log\\tmp'+ t1 + '.txt'

#Log file location, change location if necessary
logfile = 'C:\\inetpub\\logs\\LogFiles\\W3SVC1\\u_ex' + t1 + '_x.log'

#If temporary file do not exist it will be created
if not os.path.exists(tmpFile):
    with open(tmpFile,'w') as t:
        t.write('0')

#if log file does not exist script will exit
if not os.path.exists(logfile):
    print('Log file does not exist'.format(logfile))
    sys.exit(1)

#Reading number of lines in last check
with open(tmpFile,'r') as t:
    intl1 = int(t.readline())
    
    #Opening log file.
    with open(logfile,'r') as logIIS:
        for line in logIIS:
            
            #Lines in previous cycle will not be inserted
            if c >= intl1:
                
                #First lines in IIIS logs files have header which is not  needed
                if line.startswith('#'):
                    c += 1
                    continue
                else:
                    #Insert records
                    cur.execute('INSERT INTO table1 VALUES({})'.format(str(line.split()).strip('[]')))
            c += 1
    conn.commit()
    conn.close()

#Writing number of lines in temporary file
with open(tmpFile,'w') as t:
    t.write(str(c))
    

#Table creation DDL
#
# CREATE TABLE public.table1 (
#     ldate date NOT NULL,
#     ltime time NOT NULL,
#     s_ip cidr NOT NULL,
#     cs_method varchar(1000) NOT NULL,
#     cs_uri_stem varchar(2000) NOT NULL,
#     cs_uri_query varchar(2000) NOT NULL,
#     s_port int4 NULL,
#     cs_username varchar(1000) NOT NULL,
#     c_ip cidr NOT NULL,
#     cs_user_agent varchar(2000) NOT NULL,
#     cs_referer varchar(1000) NOT NULL,
#     sc_status int4 NULL,
#     sc_substatus int4 NULL,
#     sc_win32_status int4 NULL,
#     time_taken int4 NULL,
#     realclientip varchar(1000) NOT NULL
# )
# WITH (
#     OIDS=FALSE
# );

