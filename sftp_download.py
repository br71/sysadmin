# What script do => Download files from sftp server.
# with some flow, integrity chacks and rollback

import paramiko,os,datetime,sys
from pathlib import Path
import logging, stat
from imohash import hashfile,hashfileobject
import time

# Client initialization
ssh = paramiko.SSHClient()
sftp = paramiko.sftp_client.SFTPClient
f = paramiko.sftp_file.SFTPFile


# Local download folder (arguments)
localFolder = 'C:\\Temp\\dst\\'
localTmpFolder = 'C:\\Temp\\dst\\tmp\\'
localErrFolder = 'C:\\Temp\\dst\\err\\'
logFile = 'C:\\Temp\\sftplog.log'

# Remote files array
remoteFiles = []
remoteFilesExecuted = []


# Remote folders (arguments)
remoteFolder = '/C:/temp/src/'
remoteArchFolder = '/C:/temp/src/send/'


# Loging c0nfiguration (arguments)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG, filename=logFile)


# Timestamp
date = time.strftime("%Y%m%d-%H%M%S")


# Connection parameters (arguments)
IP = '127.0.0.1'
Port = 22
Username = 'sftpuser'
Password = '**************'
searchString = 'test'

# Defining flags
flag1 = False
flag2 = False
flag3 = False

# Defining temp prefix  (arguments)
ext = 'tmp_'


# Starting connection
try:
    logging.info('Starting SFTP connection')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, Port, username=Username, password=Password)
    sftp = ssh.open_sftp()
    logging.info('Sucessfully open ssh connection')
except Exception as e:
    logging.info('Unable to open ssh connection')
    logging.info(e)
    logging.info('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)


# Creating list with remote files names
try:
    logging.info('Getting list of remote files started')
    files = sftp.listdir(remoteFolder)
    for i in files:
        if ext in i:
            Path(localErrFolder + date + i + 'lockedfilefound.err').touch()
            logging.debug('Locked file found error: {}'.format(i))
            break
        elif stat.S_ISDIR(sftp.stat(remoteFolder = i).st_mode):
            logging.debug('Direcory found: {}'.format(i))
            break
        elif searchString in i:
            remoteFiles.append(i)
            logging.debug('File added to list: {}'.format(i))
    logging.info('Getting list of remote files finished')
    logging.info('Files added to list: {}'.format(remoteFiles))
except Exception as e:
    logging.info('Unable to get list of remote files')
    logging.info(e)
    logging.info('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)


# Start renaming, downloading and archiving remote files 
logging.info('Start renaming, downloading and archiving files')

for i in remoteFiles:
    k =  ext + i
    # Renaming file to tmp file
    try: 
        sftp.rename(remoteFolder + i, remoteFolder + k)
        flag1 = True
        logging.debug('Flag1 = {}, File renamed to  {}'.format(flag1,k))
    except Exception as e:
        Path(localErrFolder + date + i + 'remoterename.err').touch()
        logging.info('Unable to rename tmp file: {}. Probably already locked'.format(k))
        logging.debug(e)
        logging.debug('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))


    # Download  renamed file to tmp local folder 
    if flag1:
        logging.info(' Download {}   renamed file {} to tmp local folder '.format(searchString,k))
        try:
            sftp.get(remoteFolder + k, localTmpFolder + k)
            
            h1 = hashfileobject(sftp.file(remoteFolder + k), hexdigest=True)
            h2 = hashfile(localTmpFolder + k, hexdigest=True)
            logging.debug(' Hash created for file: {}'.format(k))

            if h1 == h2:
                flag2 = True
                logging.debug(' Hash is ok, downloaded  renamed file to tmp local folder finished {}'.format(k))
            else:
                logging.info(' Hash is not ok: {}'.format(k))
                Path(localErrFolder + date + i + 'hashisnotok.err').touch()

        except Exception as e:
            Path(localErrFolder + date + i + 'unabletodowload.err').touch()
            logging.info(' Unable to download file: {}'.format(k))
            logging.debug(e)
            logging.debug('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))

        logging.info(' Download  file {} to tmp local folder finished '.format( k))        


    # Move-rename file to from tmp folder to final destination
    if flag2:
        logging.debug(' Move file from tmp local folder to final dst  {}'.format(i))
        try:
            os.rename(localTmpFolder + k, localFolder + i)
            flag3 = True
            logging.debug(' Move file from tmp local folder to final dst finished {}'.format( i)) 
        except Exception as e:
            Path(localErrFolder + date + i + 'movefromtmp.err').touch()
            logging.info('Unable to move file to final destination: {}'.format(k))
            logging.debug(e)
            logging.debug('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    else: 
        # Dowload is unsucessfull, performing remote rename roolback
        logging.info('Performing rollback, remote rename {}'.format( i))
        try:    
            sftp.rename(remoteFolder + k, remoteFolder + i)
            logging.info('Performing rollback, remote rename finished {}'.format(i))
        except Exception as e:
            Path(localErrFolder + date + i + 'rollbackremoterename.err').touch()
            logging.info(' Unable to rollback remote renamed file: {}'.format(k))
            logging.debug(e)
            logging.debug('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))


    # Move file to to remote archive
    if flag3:
        print('{} Move remote file to archive  {}'.format(date,i))
        try:
            sftp.rename(remoteFolder + k, remoteArchFolder + i)
            logging.debug(' Move remote file to archive finished {}'.format( i))
            remoteFilesExecuted.append(i)
        except Exception as e:
            Path(localErrFolder + date + i + 'remotearchive.err').touch()
            logging.info('{} Unable to remote archive file: {}'.format(date,k))
            logging.debug(e)
            logging.debug('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
        
logging.info("Downloading and archiving finished")
logging.info('Files transfered and archived: {}'.format(remoteFilesExecuted))


#Closing connection
try:
    ssh.close()
    logging.info('{}  SSH session closed'.format(date))
except Exception as e:
    logging.info('{} Unable close ssh connection'.format(date))
    logging.info(e)
    logging.info('Error in line: {}'.format(sys.exc_info()[-1].tb_lineno))
    sys.exit(2)


