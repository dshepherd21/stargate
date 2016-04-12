import filr
import os
from tqdm import tqdm

os.system("cls")
srv="filrutp.utopia.novell.com"
user="admin"

user,pw=filr.pw(srv,user,None)
print user
s=filr.auth(user,pw)
folderid="61"
fname=raw_input("Enter Your File Name ?")
name=filr.raw(fname)
print "Path is "+name

status=filr.mup(folderid,name,srv,"","",s)

