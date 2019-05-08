# Resp1
This respository contains useful python/jython scripts. 

Descriptions:

WebSphereAppManageWAR.py:  
Puprose of script is to manage web sphere appliactions using wasagent juthon console. Usage is located on top of the script. 

pyListLocalWinGroups2excel.py:  
This script list all local windows groups from list of computers and export results directly to microsoft excel.

pySearchVmPyvmomi.py:  
Script search through vcenter servers for VM. Input parameter is name of VM or part of name. Search is case insesitive.
Search speed depends on search criteria. Couple hunderd of VM-s provides satisfactory search speed.  

wasStatusAppNagios.py:  
This is nagios check for webSphere applications. Jython script and nagios configurations (comented part)

pyIIS_NagiosParser.py:
Simple IIS log file parser. It is nagios plugin. 
Purpose is to find response time (by regex in log line) for some url (by search string in log line) and do nagios part.


IISlogsToPostgreSQL.py:
This script insert IIS log files lines to potgresql db, table.


G_iisLogDbModel_SqlAlchemy.py, G_iisLogDbInsert_SqlAlchemy.py:
These scripts read IIS log files and insert log lines in database. 
Incremental parsing (cron job ...) of log file is implemented. 
In case of batch insert execute script just once (before that delete temporary file (if exist) which count parsed lines)
SqlAlchemy is used for persistence to the database. Postgresql, Mysql and MSSQ databases are tested.



