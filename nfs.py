import filr
import dicttoxml
import os
from xml.dom.minidom import parseString
import urllib3
urllib3.disable_warnings()


os.system("cls")
server="filrutp.utopia.novell.com"
user="admin"
user,pw=filr.pw(server,user,None)
s=filr.auth(user,pw)
test=filr.savenfs(server,"c:\\netfolders\\nfs",user,s)
#print test
test1=filr.savenf(server,"c:\\netfolders\\nf",user,s)
#print test1

temp=filr.restnfs(server,"c:\\netfolders\\nfs","password",user,s)
temp=filr.restnf(server,"c:\\netfolders\\nf",user,s)
