#What script do => Download files from sftp server.
#Connection to sftp server is key(with paraphrase) based authentication
#Files which which will be downloaded is determined by search string.
#Script compare list of names on remote and local locationd and download only different files from remote location

import paramiko,os,datetime,sys

#Client initialization
ssh = paramiko.SSHClient()
sftp = paramiko.sftp_client.SFTPClient

#Local download folder
localFolder = 'C:\\test\\'

#Local files array
localFiles =[]

#Remote files array
remoteFiles = []

#Remote folder
remoteFolder = '/test/'

#Timestamp
d1 = str(datetime.date.today())
t1 = str(datetime.datetime.now().time())
date = d1 + ' ' + t1

#Connection parameters
IP = 'sftpServerAddress'
Port = 22
Username = 'myUsername'

#Key password (paraphrase)
Password = 'myPassword'
#Key is in OpenSSH compatible format
#http://stackoverflow.com/questions/2224066/how-to-convert-ssh-keypairs-generated-using-puttygenwindows-into-key-pairs-use
Key = 'C:\\test.pem'

#Search string for files which will be downloaded
searchString = 'mySearchString'


#Starting connection
try:
    print('{} Starting ftp connection'.format(date))
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, Port, username=Username, password=Password, key_filename=Key)
    sftp = ssh.open_sftp()
    print('{} Sucessfully open ssh connection'.format(date))
except Exception as e:
    print('{} Unable to open ssh connection'.format(date))
    print(e)
    print('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)

#Creating list with remote files names
try:
    print('{} Getting list of remote files started.'.format(date))
    files = sftp.listdir(remoteFolder)
    for i in files:
        if searchString in i:
            remoteFiles.append(i)
    print('{} Getting list of remote files finished.'.format(date))
except Exception as e:
    print('{}  Unable to get list of remote files'.format(date))
    print(e)
    print('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)

#Creating list with local files names
try:
    print('{} Getting list of LOCAL files started.'.format(date))
    localFiles = os.listdir(localFolder)
    print('{}  Getting list of LOCAL files finished.'.format(date))
except Exception as e:
    print('{} Unable get list of LOCAL files'.format(date))
    print(e)
    print('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)


#Determining difference between loal and remote files.
#Different names wil be downloaded
p = set(remoteFiles).difference(localFiles)
print('{} files to download: {}'.format(date,p))

#Start downloading remote files(sync)
try:
    print('{} Start downloading files'.format(date))
    for k in p:
        sftp.get(remoteFolder + k, localFolder + k)
    print('{} Downloading finished'.format(date))

except Exception as e:
    print('{} Unable download admst...csv files'.format(date))
    print(e)
    print('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)


#Closing connection
try:
    ssh.close()
    print('{}  SSH session closed'.format(date))
except Exception as e:
    print('{} Unable download close ssh connection'.format(date))
    print(e)
    print('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)

