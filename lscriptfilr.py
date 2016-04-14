import filr
import ldap
import os
import sys
import time
from datetime import date
import datetime
import ldif
import ldap.modlist as modlist
from optparse import OptionParser	
	


def ldapcr(srv,user,passw,name,dn,attrs,naming):
        print "-"*70
        l=ldap.initialize(srv)
        try:
		l.bind_s(user, passw)
	except ldap.INVALID_CREDENTIALS:
		print "Your username or password is incorrect."
		sys.exit()
	except ldap.LDAPError, e:
		if type(e.message) == dict and e.message.has_key('desc'):
			print e.message['desc']
		else:
			print e
			sys.exit()
	try:
		print name,dn,naming
		value = l.compare_s(dn,naming,name[0])
		print value
		if value==1:
			print "Object Already Exists"
			objectpresent="yes"
	except ldap.NO_SUCH_OBJECT:
		print "Object not Found So create new object"
		print "Before Add Record ***"
		try:
			ld=modlist.addModlist(attrs)
			print ld,dn
			l.add_s(str(dn),ld)
		except:
			print "ERROR In Create"
	status=0
	return(status)

def findos(ldapsrv,base_dn,user,passw):
	print ldapsrv
	print base_dn
	l=ldap.initialize(ldapsrv)
	try:
		#l.start_tls_s()
		l.bind_s(user, passw)
	except ldap.INVALID_CREDENTIALS:
		print "Your username or password is incorrect."
		sys.exit()
	except ldap.LDAPError, e:
		print e.message['info']
		if type(e.message) == dict and e.message.has_key('desc'):
			print e.message['desc']

		else:
			sys.exit()
	except ldap.NO_SUCH_OBJECT:
		print "Object Not Found"
		sys.exit()
	attrs = ['o']
	filter='(objectclass=Organization)'
	grplist=l.search_s( base_dn,ldap.SCOPE_SUBTREE,filter,attrs)
	return(grplist)




def findusers(ldapsrv,base_dn,user,passw):
	#print ldapsrv
	l=ldap.initialize(ldapsrv)
	try:
		#l.start_tls_s()
		l.bind_s(user, passw)
	except ldap.INVALID_CREDENTIALS:
		print "Your username or password is incorrect."
		sys.exit()
	except ldap.LDAPError, e:
		print e.message['info']
		if type(e.message) == dict and e.message.has_key('desc'):
			print e.message['desc']

		else:
			sys.exit()
	except ldap.NO_SUCH_OBJECT:
		print "Object Not Found"
		sys.exit()
	#attrs = ['CN','loginTime']
	filter='(&(objectclass=inetOrgPerson)(cn=*)(ndsHomeDirectory=*))'
	#print filter
	#filter='(objectclass=inetOrgPerson)'
	attrs = ['cn','ndsHomeDirectory']
	grplist=l.search_s( base_dn,ldap.SCOPE_SUBTREE,filter,attrs)
	return(grplist)
	
def findgroups(ldapsrv,base_dn,user,passw):
     l=ldap.initialize(ldapsrv)
     try:
        #l.start_tls_s()
        l.bind_s(user, passw)
     except ldap.INVALID_CREDENTIALS:
        print "Your username or password is incorrect."
        sys.exit()
     except ldap.LDAPError, e:
        print e.message['info']
        if type(e.message) == dict and e.message.has_key('desc'):
            print e.message['desc']
        
	else:
            sys.exit()
     except ldap.NO_SUCH_OBJECT:
	print "Object Not Found"
	sys.exit()

     attrs = ['cn','objectClass','ACL']
     filter=('objectclass=groupOfNames')
     grplist=l.search_s( base_dn,ldap.SCOPE_SUBTREE,filter,attrs)
     return(grplist)	


def findous(ldapsrv,base_dn,user,passw):
	print base_dn
	print ldapsrv
	print user
	print passw
	l=ldap.initialize(ldapsrv)
	try:
		#l.start_tls_s()
		l.bind_s(user, passw)
	except ldap.INVALID_CREDENTIALS:
		print "Your username or password is incorrect."
		sys.exit()
	except ldap.LDAPError, e:
		print e.message
		print e.message['info']
		if type(e.message) == dict and e.message.has_key('desc'):
			print e.message['desc']

		else:
			sys.exit()
	except ldap.NO_SUCH_OBJECT:
		print "Object Not Found"
		sys.exit()
	attrs = ['ou','objectClass','description','loginScript']
	filter='(&(objectclass=*)(loginScript=*))'
	objlist=l.search_s( base_dn,ldap.SCOPE_SUBTREE,filter,attrs)
	return(objlist)

def dotted(dn):
	newtemp=[]
	dntemp=dn.split(",")
	print dntemp
	for line in dntemp:
		print line[0:3]
		print line[0:2]
		if line[0:3]=="ou=":
			newtemp.append(line.replace("ou=","."))
		if line[0:2]=="o=":
			newtemp.append(line.replace("o=","."))
	print newtemp
	newdn="".join(newtemp)
	newdn=newdn[1:]
	return (newdn)
	
def makeunc(path):
	print path
	if "/" in path:
		temp=path.split("/")
		srv=temp[0]
		path=temp[1].split(":")
		
		unc1="\\\\"+srv+"\\"+path[0]+"\\"+path[1]
		print unc1
	return(unc1)

def groupname(dn):
	print "dn:"+dn
	temp2=dn.split(".")
	cn=temp2[1]
	cn=cn.replace("cn=","")
	cn=cn.replace("CN=","")
	cn=cn.replace(".","")
	return(cn)
		
		
def rep(oldunc,newunc,script):
	cmd="map"
	for index,lines in enumerate(script):
		if (cmd.lower() in lines) or (cmd.upper() in lines):
			if oldunc in lines:
				new=lines.replace(oldunc,newunc)
				script[index]=new
	return(script)
			
def ldapwrite(srv,user,passw,dn,attr,value):
    l=ldap.initialize(srv)
    try:
        #l.start_tls_s()
        l.bind_s(user, passw)
    except ldap.INVALID_CREDENTIALS:
        print "Your username or password is incorrect."
        sys.exit()
    except ldap.LDAPError, e:
        print e.message['info']
        if type(e.message) == dict and e.message.has_key('desc'):
            print e.message['desc']
        else:
            print e
        sys.exit()
    mod_attrs=[( ldap.MOD_ADD, attr,value)]
    try:
    	status=l.modify_s(dn,mod_attrs)
    except ldap.TYPE_OR_VALUE_EXISTS:
        print "Value Already set against group "
    except ldap.INVALID_DN_SYNTAX:
        print "Invalid DN !!"
    l.unbind()
    # print status
    return


def mknf(filrsrv,filrusr,filrpass,lscript,hd,suffix,op):
	created=[]
	print "Netfolders and Netfolder Servers to be created for server "+filrsrv
	relpath=[]
	for temp in lscript:
		if "map" in temp or "MAP" in temp:
			#print "Map line detected"
			drive=temp[4:5]
			if drive<>"hd":
				unc=temp.split("=")
				#print unc
				if ":" in unc[1]:
					unc=unc[1].replace(":","")
					#print unc
					comp=unc.split("\\")
					l1=len(comp)
					#print comp
					if l1>2:
						relpath=comp[3:]
					host=comp[0]
					vol=comp[1]
					name=host+"."+suffix+"-"+vol.upper()
					path="\\\\"+host+"."+suffix+"\\"+vol.upper()
					nfname=vol+"-"+drive.upper()
					#print path
					#print len(relpath)
					print
					print "Creating Netfolder Server.."+name
					print "_"*80
					print
					print "Based on script line "+temp
					print "Driver Type \t"+drivertype
					print "Server Path \t"+path
					print "Proxy User \t"+proxyuser
					print "Filr Server \t"+filrsrv
					print
					print "Creating Netfolder.."
					print "Netfolder Name is "+nfname
					print 
					
					if op.lower()<>"display":
						rights=["allusers","group","ACCESS","true","false","true","false"]	
						print "Filr Netfolders and NetFolder Creation.."
						temp=filr.crnfs(name,drivertype,path,authtype,proxyuser,proxypass,filrsrv,0,"admin",s)
						created.append(name)
						if l1<=2:
							time.sleep(pause)
							temp=filr.crnf(name,nfname,'\\',filrsrv,rights,"admin",adminpass,0,s)
							print temp
							
							
						else:
							print "larger rel path"
					else:
						print "Only Display Selected so no Netfolders Created"		
					print
					
					
pause=1		
os.system("cls")
relpath=[]
parser = OptionParser()
parser.add_option("-o","--operation",help="Display or replace login script")
parser.add_option("-u","--user",help="LDAP User")
parser.add_option("-p","--password",help="LDAP Password")
parser.add_option("-d","--dn",help="BaseDN")
parser.add_option("-s","--oesserver",help="ldap://Server Name:389")
parser.add_option("-f","--filr",help="filr.xxx.com")
parser.add_option("-a","--admin",help="Admin Password")
parser.add_option("-l","--drive",help="exclude homedrive")
parser.add_option("-n","--dnssuffix",help="dns suffix")


(options, args) = parser.parse_args()

required=["operation","user","password","dn","oesserver","filr","admin","drive","dnssuffix"]
for m in required:
	if not options.__dict__[m]:
		print "mandatory option is missing\n"
		parser.print_help()
		exit(-1)



print"\n"
print"\n"

files=open("proxy.conf","r").readlines()
#print files
proxyuser=files[0][:-1]
proxypass=files[1][:-1]
proxyuser=proxyuser.replace("user=","")
proxypass=proxypass.replace("password=","")
drivertype="oes"
authtype="nmas"
oessrv=options.oesserver
filrsrv=options.filr
adminpass=options.admin
hdrive=options.drive
user=options.user
pw=options.password
basedn=options.dn
op=options.operation
dns=options.dnssuffix

s=filr.auth("admin",adminpass)

ou=findous(oessrv,basedn,user,pw)
count=0
print "Number of Source Login Scripts Found :"+str(len(ou))

if options.operation.lower()=="display":
	print "All operations will not be updated written to the Filr Server and just displayed"
if options.operation.lower()=="create":
	print "Warning all drive mappings found will be written to Filr Server "+filrsrv+" !!!"
	inp=raw_input("Are You Sure ..(Y/N)?")
	if inp.lower()=="n":
		sys.exit()
	

for temp in ou:
	out=str(count)+")Login Script = "+str(temp[0])
	print "="*len(out)
	print out
	print "="*len(out)
	print "\n"
	lscript=temp[1]["loginScript"][0]
	
	if len(lscript)<>0:
		lscriptlist=lscript.split("\r\n")
		mknf(filrsrv,"admin",adminpass,lscriptlist,hdrive,dns,op)
		count=count+1

print "Processing Complete "+str(count)+" Script(s) processed"
		
		
		
		
