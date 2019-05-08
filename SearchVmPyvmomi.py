#Example:
#python.exe pySearchVmPyvmomi.py -vm DB
#python.exe pySearchVmPyvmomi.py -vm DB
#Search is case insenitive

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import argparse

#Virtual machine hosts or vcenter servers
vmHost1 = 'host1.domain.com'
vmHost2 = 'host2.domain.com'
vmHost3 = 'host3.domain.com'

#Number of finded vm-s on all hosts
t = 0

#In case of domain server which have windows AD authentication username is: domain\\username
vmUser = 'myUsername'
vmPassword = 'myPassword'

parser = argparse.ArgumentParser(
    description='Search VM by name',
    epilog='Search for string in VM, search is case insensitive. '
           'Searched hosts: ' + vmHost1 + ' ' + vmHost2+ ' ' + vmHost3
    )

#Argument parser
parser.add_argument('-vm', action="store", required=True, help='Enter name (part of name) of virtual machine')
args = parser.parse_args()
seachVMstring = args.vm
seachVMstring1 = seachVMstring.lower()


#Search function
def searchHost(vmHostA, seachVMstringA):
    global t

    #Define ssl
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    #Avoid error in case of non valid certificate
    s.verify_mode = ssl.CERT_NONE

    #Define connection, content and container
    c = SmartConnect(host=vmHostA, user=vmUser, pwd=vmPassword, sslContext=s)
    content = c.RetrieveContent()
    container = content.rootFolder
    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView(container, viewType, recursive)

    #Arrays with listed virtual machines
    l1 = []
    l2 = []
    children1 = containerView.view

    print('Start to retreive data from {}.'.format(vmHostA))
    for child1 in children1:
        l1.append(child1.name)

        #Everything goes to lowercase
        l2.append(child1.name.lower())

    Disconnect(c)

    #Number of virtual machines which is found at one host
    sn = 0

    #Searh for vm pattern.
    print('Start searching for vm pattern: {}'.format(seachVMstring))
    for i in range(0, len(l2), 1):
        if seachVMstringA in l2[i]:
            sn = sn + 1
            t = t + 1
            print('vm {}: {} is located in {}:'.format(t,l1[i], vmHostA))

    if sn == 0:
        print('There is not VM pattern: {} in host: {}'.format(seachVMstring, vmHostA))

    print('\n')

def main():

    #Executing search function on each virtual machine host or vcenter servers
    searchHost(vmHost1, seachVMstring1)
    searchHost(vmHost2, seachVMstring1)
    searchHost(vmHost3, seachVMstring1)


if __name__ == '__main__':
    main()
