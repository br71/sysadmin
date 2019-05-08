##USAGE:
##"path_to_wsadmin\wsadmin.bat" -user ********** -password *********** -lang jython -f C:\WebSphereAppManageWAR.py nameOfApp start
##"path_to_wsadminn\wsadmin.bat" -user ********** -password *********** -lang jython -f C:\WebSphereAppManageWAR.py nameOfApp stop
##"path_to_wsadminn\wsadmin.bat" -user ********** -password *********** -lang jython -f C:\WebSphereAppManageWAR.py nameOfApp status
##"path_to_wsadmin\wsadmin.bat" -user ********** -password *********** -lang jython -f C:\WebSphereAppManageWAR.py nameOfApp restart
##"path_to_wsadmin\wsadmin.bat" -user ********** -password *********** -lang jython -f C:\WebSphereAppManageWAR.py help
##"path_to_wsadminn\wsadmin.bat" -user ********** -password *********** -lang jython -f C:\WebSphereAppManageWAR.py statusinfo
##User and pasword, same as login in web interface.
##This script must be executed on server with instaled WebSphere. This is jython script (python 2 syntax).

def stopApp(appname):
	try:
		appManager = AdminControl.queryNames('cell=nameOfCell,node=nameOfNode,type=ApplicationManager,process=nameOfServer,*')
		AdminControl.invoke(appManager, 'stopApplication', appname)
		print appname + " stopped"
	except:
		print appname + " NOT stopped"


def startpApp(appname):
	try:
		appManager = AdminControl.queryNames('cell=nameOfCell,node=nameOfNode,type=ApplicationManager,process=nameOfServer,*')
		AdminControl.invoke(appManager, 'startApplication', appname)
		print appname
		print "started"
	except:
		print appname
		print "NOT started"


def getAppStatus(appname):
    # If objectName is blank, then the application is not running.
    objectName = AdminControl.completeObjectName('type=Application,name=' + appname + ',*')
    if objectName == "":
        #appStatus = 'Stopped'
		print "Stopped"
    else:
        #appStatus = 'Running'
		print "Running"
    #return appStatus

def getAppStatus2(appname):
    # If objectName is blank, then the application is not running.
    objectName = AdminControl.completeObjectName('type=Application,name=' + appname + ',*')
    if objectName == "":
        appStatus = 'Stopped'
    else:
        appStatus = 'Running'
    return appStatus

def appStatusInfo():
    appsString = AdminApp.list()
    appList = appsString.split("\r\n")

    print '============================'
    print ' Status |    Application   '
    print '============================'

    # Print apps and their status
    for x in appList:
        print getAppStatus2(x) + ' | ' + x

    print '============================'


def main():
	if len(sys.argv) == 0:
		print "usage: first argument is: nameOfAppp(Application),statusinfo or help. Second argument is: start,stop, restart or status (in this case first argument nameOfApp(Application) is mandatory. In first usage recomended argument is statusinfo. If argument is nameOfAppp second parameter(start, stop, status, restart) is mandatory."
	elif sys.argv[0] == 'help':
		print "usage: first argument is: nameOfAppp(Application),statusinfo or help. Second argument is: start,stop, restart or status (in this case first argument nameOfApp(Application) is mandatory. In first usage recomended argument is statusinfo. If argument is nameOfAppp second parameter(start, stop, status, restart) is mandatory."
	elif sys.argv[0] == 'statusinfo':
		appStatusInfo()
	elif sys.argv[1] == 'stop':
		print sys.argv[1]
		print "stopping app"
		stopApp(sys.argv[0])
	elif sys.argv[1] == 'start':
		print sys.argv[1]
		print "starting app"
		startpApp(sys.argv[0])
	elif sys.argv[1] == 'status':
		print sys.argv[1]
		print "Status of app"
		getAppStatus(sys.argv[0])
	elif sys.argv[1] == 'restart':
		print sys.argv[1]
		print "restarting app"
		stopApp(sys.argv[0])
		startpApp(sys.argv[0])
	else:
		print "usage: first argument is: nameOfAppp(Application),statusinfo or help. Second argument is: start,stop, restart or status (in this case first argument nameOfApp(Application) is mandatory. In first usage recomended argument is statusinfo. If argument is nameOfAppp second parameter(start, stop, status, restart) is mandatory."


if __name__ == '__main__':
	main()




