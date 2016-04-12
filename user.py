import filr
import os


os.system("cls")
pw=None
srv="filrutp.utopia.novell.com"

user="admin"
user,pw=filr.pw(srv,user,pw)
s=filr.auth(user,pw)
userinfo=filr.filrapi(srv,"self","","","",0,0,s)
os.system("cls")

print userinfo["title"]
