import sys

def getAppStatus(appname):
    objectName = AdminControl.completeObjectName('type=Application,name=' + appname + ',*')
    if objectName == "":
        appStatus = 'Stopped'
    else:
        appStatus = 'Running'
    return appStatus


def main():
    print('Status of service: ' + sys.argv[0] + ' is: ' + getAppStatus(sys.argv[0]))
    if getAppStatus(sys.argv[0]) == 'Stopped':
        sys.exit(2)
    elif getAppStatus(sys.argv[0]) == 'Running':
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()

####################################################################
#was = IBM WebSphere application server (tested on ver. 8.5)
#Below is nagios part:
####################################################################
#
#Line in nsclient.ini(client machine - windows):
#
#checkWas[something]="[path to wsadmin.bat]\wsadmin.bat" -user *** -password *** -lang jython -f "[path to script]\wasStatusAppNagios.py" [name of websphere app]
#
####################################################################
#
#Line in commands.cfg (nagios host):
#
#define command{
#        command_name checkWas[something]
#        command_line /usr/lib64/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c checkWas[something]
#        }
#
####################################################################
#
#Service desctripionin nagios services:
#
#define service (nagios host){
#       use                     generic-service
#       host_name               [hostname]
#       service_description     checkWas[something]
#       check_command           checkWas[something]
#       }
#
####################################################################

