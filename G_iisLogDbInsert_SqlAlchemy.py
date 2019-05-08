#Nagios execute this cript 
import os.path,sys,datetime
from sqlalchemy import insert
import G_iisLogDbModel_SqlAlchemy


#SQL Alchemy Core
mt = G_iisLogDbModel_SqlAlchemy.metadata
lt = G_iisLogDbModel_SqlAlchemy.logtable
e = G_iisLogDbModel_SqlAlchemy.engine
connection = e.connect()

#Parser part
c = 0
t1 = '{0:%y%m%d}'.format(datetime.datetime.now())

#Temporary file. Script load logs in databases in every 5-10 minutes.
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
    print(logfile)
    print('Log file does not exist'.format(logfile))
    sys.exit(1)


#Inserting data
#Reading number of lines in last check
with open(tmpFile,'r') as t:
    intl1 = int(t.readline())
    
    #Opening log file.
    with open(logfile,'r',encoding="utf-8") as logIIS:
        for line in logIIS:
            
            #Lines in previous cycle will not be inserted
            if c >= intl1:
                
                #First lines in IIIS logs files have header which is not  needed
                if line.startswith('#'):
                    c += 1
                    continue
                else:
                    #Insert records
                    #ins = str(line.split()).strip('[]').replace('\'','\"')
                    l = line.split()
                    #print('lineIndex0: {}'.format(l[0]))
                    
                    ins = insert(lt).values(
                        ldate = '{}'.format(l[0]),
                        ltime = '{}'.format(l[1]),
                        s_ip = '{}'.format(l[2]),
                        cs_method = '{}'.format(l[3]),
                        cs_uri_stem = '{}'.format(l[4]),
                        cs_uri_query = '{}'.format(l[5]),
                        s_port = '{}'.format(l[6]),
                        cs_username = '{}'.format(l[7]),
                        c_ip = '{}'.format(l[8]),
                        cs_user_agent = '{}'.format(l[9]),
                        cs_referer = '{}'.format(l[10]),
                        sc_status = '{}'.format(l[11]),
                        sc_substatus = '{}'.format(l[12]),
                        sc_win32_status = '{}'.format(l[13]),
                        time_takens = '{}'.format(l[14]),
                        realclientips = '{}'.format(l[15])
                        )

                    #print('values: {}'.format(ins))
                    connection.execute(ins)
   
            c += 1
    
    connection.close
    
#Writing number of lines in temporary file
with open(tmpFile,'w') as t:
    t.write(str(c))


