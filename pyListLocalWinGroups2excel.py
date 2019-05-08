#Script list members in all local groups on windows machine.
#Windows machines is member of domain. Domain admin permission is necessary.

import win32net
import xlwt

#List of workstations
hostname = open(r'c:\\workstations.txt','r')

#Start insterting data from row 1, row 0 is header
row2 = 1

#Font style
style0 = xlwt.easyxf('font: name Arial, color-index black, bold on')

#Cretating workbook, sheet, and header
wb = xlwt.Workbook()
ws = wb.add_sheet('CecurityGroups')
ws.write(0, 0, 'Computer name',style0)
ws.write(0, 1, 'Group name',style0)
ws.write(0, 2, 'Group members',style0)

#Parsing hostname file and looping to create excel file
for h in hostname:
    print(h, end = '')

    #Detect empty line in computer list
    if h == '\n':
        continue

    else:
        h1 = h.strip()

        try:
            #Get local groups on sigle host, this is enum not list of groups
            l = win32net.NetLocalGroupEnum(h1, 0, 0)
        except:
            #In case that host is offline script will not stop. It will write that host is offline
            ws.write(row2, 0, h1)
            ws.write(row2, 1, 'Offline')
            row2 = row2 + 1
            continue

        #Initializing list with usernames in group
        group = []

        #Looping through key valye list l[] and creating list of groups
        for i in l[0]:
            group.append(i['name'])

        #Looping through list group[] 
        for g in group:
            #Get list of group members
            a = win32net.NetLocalGroupGetMembers(h1, g, 3)
            ws.write(row2, 0, h1)
            ws.write(row2, 1, g)

            #List with users
            s=[]

            #Lopping through key value list a[] an extacting only users
            for i in a[0]:
                s.append(i['domainandname'])

            #Print in file and removing character for pretty printing
            ws.write(row2, 2, str(s).strip('[]').replace('\'', '').replace('\\\\','\\'))

            row2 = row2 + 1

#Saving workbook
wb.save(r'c:\\test.xls')







