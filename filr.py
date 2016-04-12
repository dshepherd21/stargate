#!/usr/bin/python
# -*- coding: utf-8 -*-
#import _mysql as sql

import tqdm
import ast
import fnmatch
import ntpath
import mmap
import hashlib
import sys
import os
import sets
import urllib3
urllib3.disable_warnings()
import requests, json
requests.packages.urllib3.disable_warnings()
import requests_cache
requests_cache.install_cache('filr_cache',backend='sqlite',expire_after=300,allowable_methods=('GET',))
requests_cache.clear()



import time
import python_webdav.client as pywebdav_client
import xml.etree.ElementTree as ET
import paramiko
import time
import string
import datetime
import platform
import urllib2
import urllib
import urllib3
from scp import SCPClient
import _mysql as sql
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
#import simplejson
#from json2xml import json2xml
import posixpath
import sys
import copy
import datetime
import time
import platform
import getpass
import posixpath
import keyring
import pickle
from dateutil import parser
from xml.dom import minidom
from xml.dom.minidom import parseString
import dicttoxml
from tqdm import tqdm
global s
s=""
escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}


def listldap(servername,user,pw,s):
	restcmd="admin/user_sources"
	temp=filrapi(servername,restcmd,"","","",0,0,s)
	return temp

def srch(servername,user,pw,terms,recurse,s,num=100):
	fd=[]
	root="/workspaces/1"
	restcmd="workspaces/1/library_entities?recursive="+recurse+"&files=true&binders=false&folder_entries=false&folders_entries=false&replies=false&parent_binder_paths=true&first=0&count="+str(num)+"&keyword="+terms
	#print restcmd
	temp=filrapi(servername,restcmd,"","","",0,0,s)
	results=temp["items"]
	#print fd
	for line in results:
		path=line["parent_binder"]["path"]
		name=line["name"]
		fd.append(path+"/"+name)
	return (fd)
	
	
	           
def disp(output,line):
	if output=="text":
		out.write(line+"\n")
		#print line
	           
def rep(outfile,repname,srvname,user):
	global out
	out=open(outfile,"w+")
	kring="Novell.Collaboration.db:"+user+"@"+srvname
	user,pw=pw1(kring,user,None)
	#print user,pw
	if not os.path.isfile(repname):
		print "ERROR: Report Config Not found"
		return -1
	prs=cred(repname)
	try:
		output=prs.get('report','output')
	except:
		print "ERROR: Missing Output"
		return -1
	try:
		title=prs.get('report','title')
	except:
		print "ERROR: Missing Title"
		return -1
	try:
		headers=prs.get('report','headers')
	except:
		print "ERROR: Missing Headers"
		return -1
	try:
		cmd=prs.get('report','sqlcmd')
	except:
		print "ERROR: Missing Title"
		return -1
	try:
		cols=prs.get('report','cols')
	except:
		print "ERROR: Missing Title"
		return -1
		
	
	#print headers
	headers=ast.literal_eval(headers)
	cols=ast.literal_eval(cols)
	temp1=sqlcmd(srvname,user,pw,cmd)
	colist=""
	colen=[]
	for temp in temp1[0]:
		colen.append(len(temp))
	
	
	for item in cols:
		item[0]=item[0].ljust(int(item[1]))
		colist=item[0]+"\t"+colist
		
	disp(output,colist)
	disp(output,"="*80)
	print "\n"
	print "STATUS: Outputting Report Results to :"+outfile
	print "\n"
	for line in temp1:
		text=""
		li=""
		for item in cols:
			txt=str(item[0].replace(" ",""))
			text=line[int(headers[item[0].replace(" ","")])]
			if len(text)==0:
				text="No Value"
			li=text+"\t"+li
		disp(output,li)
	disp(output,"\n")
	disp(output,"="*80)
	out.close()
	
	sys.exit()
			
		
def un():
	temp="-"
	now=datetime.datetime.now()
	for attr in ['year','month','day','hour','minute','second','microsecond']:
		temp=temp+str(getattr(now,attr))+"-"
	temp=temp[:-1]
	return(temp)
	
	
def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string



def auth(user,pw):
	"""sets up session authentication for subsequent filr requests"""
	s = requests.Session()
	s.auth = (user, pw)
	s.verify = False
	return s


def filterpath(source,dest):
	"""Filter source with multiple entries in dest"""
	for name in dest:
		l1=len(source)
		temp=source.replace(name,"")
		if len(temp)<>len(source):
			break
	return(temp)
			


def userinfo(server,user,pw,s):
	"""(REST) Prints user information as unformatted blob"""
	userinfo=filrapi(server,"self","","","",0,0,s)
	return(userinfo)
	

def filt(pathname,filt1):
	l=len(pathname)

	for temp in filt1:
		newpath=pathname.replace(temp,"")
		if l<>len(newpath):
			#print pathname
			#print newpath
			break
	return(newpath)

def wspaceid(server,user,pw,s):
	"""(REST) Workspace id for user"""
	temp=filrapi(server,"self","","","",0,0,s)
	#print temp
	return temp["workspace"]["id"]

def shares(server,user,pw,s):
	"""(REST) Lists All Shares for a User"""
	id1=usertoidr(server,user,pw,s)
	resp=filrapi(server,"shares/by_user/"+str(id1),"","","",0,0,s)
	print
	print "*******************************"
	print "Items Shared By User "+user
	print "*******************************"
	print
	count=1
	error=0
	for temp in resp["items"]:
		fileid=temp["shared_entity"]["href"]
		filename=filrapi(server,fileid[1:],"","","",0,0,s)
		string="/Home Workspace/Personal Workspaces/Novell Filr ("+user+")"
		string1="/Home Workspace/Net Folders"
		try:
			item=filename["entity_type"]
		except:
			#print filename
			error=1
			
			
		
		if item=="folderEntry" and error==0:
				
	
			foldername=idfolder(server,filename["parent_binder"]["id"],"","",s)
			name=filename["title"]
			fullpath=foldername+"/"+name
			newfull=filt(fullpath,[string,string1])
			print "="*75
			print str(count)+") File Shared is "+newfull
			print "="*75
			
			rights(name,str(filename["parent_binder"]["id"]),server,user,pw,s)
			print
				
		elif item=="folder" and error==0:
			path=filename["path"]
			print "="*75
			newpath=filt(path,[string,string1])
			print str(count)+") Folder Shared is "+newpath
			print "="*75
			print
			print "Folder Granted to User "+idtoname(str(temp["recipient"]["id"]),server,"","",s)
			print "Access Granted is :"+str(temp["access"]["role"])
			print "Reshare right granted "+str(temp["access"]["sharing"]["grant_reshare"])
			print
			
			print
		error=0
		count=count+1
	print
	print "Total Number of Shares for user "+user+" is "+str(count-1)
	print	
				
		

def usertoidr(server,user,pw,s):
	"""(REST) Converts User to Filr ID Number """
	temp=filrapi(server,"self","","","",0,0,s)
	#print temp
	
	return temp["id"]
	
def homedir(server,user,pw):
	""" (REST) Routine to return the users Home Folder (if exists) and the id of the home folder"""
	path=""
	id=0
	idnum=wspaceid(server,user,pw)
	shares=filrapi(server,"workspaces/"+str(idnum)+"/library_folders","",user,pw)
	for temp in shares["items"]:
		stat=temp["home_dir"]
		#print temp
		if stat:
			#print "Home Directory found "
			path=temp["path"]
			id=temp["id"]
			#break
	
	return(id,path)
	


def netmap(server,path,user,drive):
	user,pw1=pw(server,user,None)
	cmd="net use "+drive+": https://"+server+"/"+path+" /user:"+user+" "+pw1
	print cmd
	print "Please Wait.. Filr being accessed :"
	stat=os.system(cmd)
	return stat
	

def size(name,folderid,server,user,pw,s):
	"""(REST) Size of a file from a netfolder over rest """
	status=0
	
	id=filetoidr(name,folderid,server,user,pw,s)
	data=filrapi(server,"folders/"+folderid+"/files","","","",0,0,s)
	
	filr_url=""
	for temp in data["items"]:
		if name==temp["name"]:
			length=temp["length"]
	
	#print "Time taken to run command is %5.3f seconds" %taken
	length=length/1024
	print "Size of file "+name+" is %10.3f k" %length
	return (length)



def download(name,folderid,server,path,user,pw,s,chunk=3072):
	"""Download of a file from a netfolder over rest """
	status=0
	path=raw(path)
	#print path
	if os.path.isdir(path):
		print "Destination Directory Found "
		status=1
	else:
		print "Destination Does Not Exist"
		status=1
		return(status)
	
	start_time=time.time()
	id=filetoidr(name,folderid,server,user,pw,s)
	data=filrapi(server,"folders/"+folderid+"/files","","","",0,0,s)
	#print data["items"][0]
	#print data["items"][0]["length"]
	#print data["items"][0]["permalinks"][-1]["href"]
	#print data
	filr_url=""
	for temp in data["items"]:
		if name==temp["name"]:
			filr_url=temp["permalinks"][-1]["href"]
			length=temp["length"]
	
	if filr_url=="":
		status=1
		print "Error"
		return(status)
		
	 
	local_filename = urllib2.unquote(filr_url.split('/')[-1])
	local_filename=path+"/"+local_filename
	print local_filename+" of size "+str(length)+"k"
	print "Being Downloaded ..."
	header1 = {'Content-type': 'application/json'}
	#r=requests.get(filr_url,data="",headers=header1,auth=(user,pw),stream=True,verify=False)
	r=s.get(filr_url,data="",headers=header1,stream=True,verify=False)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=chunk): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()
	print 
	taken=time.time()-start_time
	print "File Downloaded in %5.3f Seconds" %taken
	status=0
	return (status)


def idtoname(userid,srvname,user,pw,s=""):
	"""Converts User Id to User Name over Rest"""
	userinfo=filrapi(srvname,"users/"+userid,"",user,pw,0,0,s)
	return(userinfo["name"])

def rights(filename,folderid,srvname,user,pw,s=""):
	"""(REST) List Filr Shares for a file"""
	id=filetoidr(filename,folderid,srvname,user,pw,s)
	if id<>0:
		rights=filrapi(srvname,"folder_entries/"+str(id)+"/shares","","","",0,0,s)
		#recipient=rights["items"][0]["recipient"]
		#print shareing
		count = 1
		print "Access Rights for File "+filename+":"
		for temp in rights["items"]:
		
			#print temp["recipient"]
			print 
			print "File Granted to User "+idtoname(str(temp["recipient"]["id"]),srvname,user,pw,s)
			print "Access Granted is :"+str(temp["access"]["role"])
			print "Reshare right granted "+str(temp["access"]["sharing"]["grant_reshare"])
	else:
		print "ERROR file not found"
		


def dbset(srvname,user,pw):
	cred="Novell.Collaboration.DB:"+user+"@"+srvname
	keyring.set_password(cred,user,pw)
	print "Password Set for "+cred

def pwset(srvname,user,pw):
	"""Used to Set Credentials for the rest of the client"""
	cred="Novell.Collaboration.Filr:"+user+"@"+srvname
	keyring.set_password(cred, user, pw)
	print "Password Set for "+cred



def pw1(srvname,user,pw1):
	""" Uses Credential Manager to access Filr Password and User Name"""
	#srvname="Novell.Collaboration.Filr:"+user+"@"+srvname
	#print platform.system()
	if pw1==None:
		print srvname
		pw=keyring.get_password(srvname,user)
		if pw==None:
			print "Username ? :"+user
			#user=raw_input("Username ? :")
			pw=getpass.getpass("Password ? :")
			if len(user)==0 or len(pw)==0:
				print "No Values Entered"
				print "System Finished"
				sys.exit()
	else:
		pw=pw1
		
		
	return (user,pw)

	

def pw(srvname,user,pw1):
	""" Uses Credential Manager to access Filr Password and User Name"""
	srvname="Novell.Collaboration.Filr:"+user+"@"+srvname
	#print platform.system()
	if pw1==None:
		#print srvname
		pw=keyring.get_password(srvname,user)
		if pw==None:
			print "Username ? :"+user
			#user=raw_input("Username ? :")
			pw=getpass.getpass("Password ? :")
			if len(user)==0 or len(pw)==0:
				print "No Values Entered"
				print "System Finished"
				sys.exit()
	else:
		pw=pw1
		
		
	return (user,pw)


def searchdict(diction,key,value):
	for key1, value1 in diction.iteritems():
		#print value1["path"],key1
		if value1["path"] == value:
			print key1
	return(key1)


def credread():
	
	prs=cred("auth.ini")
	for section_name in prs.sections():
		#print prs.items(section_name)
		cmd=section_name+"= prs.items(section_name)"
		exec(cmd)
	return(dbserver,nfs,appliance)
		
	
	

def cred(filename):
	parser = SafeConfigParser()
	parser.read(filename)
	return parser

	

	

def filrlist(file):
	servers=open(file,"r").readlines()
	
	return(servers)
	
	


def scpget(server,user,password,sourcedir,destdir):
	#global scp
	"""scp initialisation"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(server, username=user, password=password)
	scp = SCPClient(ssh.get_transport())
	start_time=time.time()
	
	#try:
	scp.get(sourcedir,destdir,recursive=True,preserve_times=True)
	
	end_time=time.time()
	timetaken=end_time-start_time
	print "Time Taken to copy file (seconds):"+str(timetaken)[:-10]
	print
	
	return

    


def remotecmd(cmd,address,user,pw):
	#print cmd,address,user,pw
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(address, username=user,password=pw)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		#print "end"
		#output=stdout
		output=stdout.readlines()
	except:
		output="Connection Error"
	return(output)
	
	


def chkfilr(server,user,password):
	output=remotecmd("rcfilr status",server,user,password)[0][:-1]
	results=output.split()
	# print results
	return (results[3])
	

def startfilr():
	servers=filrlist("servers1.txt")
	for temp in servers:
		if temp[0]<>"#":
			conf=temp[:-1].split(",")
			stat=chkfilr(conf[0],conf[1],conf[2])
			if stat<>"running":
				print "Starting Filr on "+conf[0]
				stat=remotecmd("rcfilr start",conf[0],conf[1],conf[2])
				print "filr started on "+conf[0]
	

	

def shutfilr():
	servers=filrlist("servers1.txt")
	for temp in servers:
		if temp[0]<>"#":
			conf=temp[:-1].split(",")
			stat=chkfilr(conf[0],conf[1],conf[2])
			if stat<>"stopped":
				print "Stopping Filr on "+conf[0]
				stat=remotecmd("rcfilr stop",conf[0],conf[1],conf[2])
				#print stat
				print stat[0][:-1]+" on "+conf[0]
	
				
				
def dbback(dbserver,server,dbuser,dbpass,spass,dbdir,dbfile,destdir):
	 #mysqldump -h 192.168.10.220 -uadmin1 -pexcalibur1 --single-transaction --routines --triggers --databases filr  >backup.db.sql

	"""Backup of the MySQL Database"""
	suf=un()
	dbfile=dbfile+suf
	cmd="mysqldump -v -u "+dbuser+" -p"+dbpass+" --single-transaction --routines --triggers --databases filr | gzip -9>"+dbdir+"/"+dbfile+".gz 2>txt.tmp"
	#cmd="mysqldump -v -u "+dbuser+" -p"+dbpass+" -h "+dbserver+" --single-transaction --routines --triggers --databases filr | gzip -9>"+dbdir+"/"+dbfile+".gz 2>txt.tmp"
	#cmd="mysqldump -v -u "+dbuser+" -p"+dbpass+" -h "+dbserver+" --single-transaction --routines --triggers --databases filr >"+dbdir+"/"+dbfile+".sql 2>txt.tmp"
	print cmd
	print 
	print "Writing SQL Filr Database to "+dbdir+" on server "+server
	src="root"
	stat=remotecmd(cmd,server,"root",spass)
	cmd="rm "+dbdir+"/txt.tmp"
	stat=remotecmd(cmd,server,"root",spass)
	
	if len(stat)==0:
		print "Database Dumped to file "+dbfile
	else:
		print "Error in Dump"
		sys.exit()
	
	scpget(server,"root",spass,dbdir+"/"+dbfile+".gz",destdir)
	stat=remotecmd("rm /root/"+dbfile+".gz",server,"root",spass)
	

	
	return
	

def backup(dbserver,dbuser,dbpass,server,spass,nfs="Yes",config="servers1.txt"):
	"""Helper Routine to backup the NFS Share and call the DB Backup"""
	result="none"
	dest="c:\\dev\\backups"
	src="/vashare"
	print "This process will shutdown Filr on all of the Filr Appliances and restart when the backup is completed"
	print "Backup started on "+time.strftime("%c")
	print
	shutfilr()
	print "The Filr Service is stopped on all appliance nodes"
	print "Starting to Backup Filr NFS Share..."
	servers=filrlist(config)
	back=servers[0][:-1].split(",")
	if nfs=="Yes":
		print "Using Server "+back[0]," "+back[1]+" "+back[2]
	
		try:
			scpget(back[0],back[1],back[2],src,dest)
			result="Complete"
		except:
			print "NFS Share Backup Error"
			result="Error NFS Share Backup"
		dbback(dbserver,server,dbuser,dbpass,spass,"/root","backup.sql")
		
	
	
	
	
	
	
	startfilr()
	sys.exit()
	
	
def restoredb():
	print
	


def filrls(path1,show='false'):
	
	"""List Directory over Webdav"""
	dirs=[]
	formlist=[]
	list=auth.ls(path=path1,list_format=('F'),separator='\\t',display=0)
	count=0
	for line in list:
		#print line
		items=''.join(line).split("/")
		#print items
		if items[-1]=="":
			if count<>0:
				if show=="true":
					print "(Dir) "+urllib2.unquote(items[-2])
				dirs.append(line)
			else:
				count=count+1
		else:
			if show=="true":
				print "(File) "+urllib2.unquote(items[-1])
		
	
	return(list,dirs)

def nfname(nfpath):
	"""Strips off the filr webdav path"""
	nfname=nfpath.replace("/Home Workspace/Net Folders/","")
	return(nfname)
	
def nfunc(uncpath):
	"""Splits the UNC path into ip,path and Volume Name"""
	#print uncpath
	temp=uncpath.split("\\")
	#print temp
	ip=temp[2]
	pathtemp=temp[3].split("/")
	#print temp[3]
	#print "----"
	vol=pathtemp[0]
	path1=uncpath.split("/")[1]
	return ip,path1,vol

def authwebdav(user,pw,server):
	"""Authenticate to Filr WebDav"""
	client_object = pywebdav_client.Client(server)
	client_object.set_connection(username=user, password=pw)
	return(client_object)
	
def querynf(sqlserver,dbuser,dbpassword):
	"""Query Netfolders from MySQL"""
	out("\n")
	out("Querying Filr DB for Netfolder Details...\n")
	out("\n")
	nflist=[]
	
	cmd="select f.pathName as filrPath, concat(r.rootPath, '/', f.resourcePath) as UNC, r.name as netFolderServer from SS_Forums f inner join SS_ResourceDriver r on f.resourceDriverName=r.name where f.parentBinder=36"

	con=sql.connect(host = sqlserver,user = dbuser,passwd = dbpassword, db = 'filr')
	con.query(cmd)
	result=con.use_result();
	temp=result.fetch_row(maxrows=0)
	print "Number of NETFOLDERS Found is "+str(len(temp))
	print
	for line in temp:
		#print line[0],line[1],line[2]
		name=nfname(line[0])
		add,path2,vol=nfunc(line[1])
		print "Name :"+name
		print "IP :"+add
		print "Path :"+path2
		print "Volume :"+vol
		print
		templist=[name,add,path2,vol]
		nflist.append(templist)
		
	
	return nflist
	

	



def sqlconnect(srvname,user,password,table):
	"""sql server connection routine"""
	#print srvname,user,password,table
	try:
		con=sql.connect(host=srvname,user=user,passwd=password,db=table)
		return(con)
	except:
		print sys.exc_info()
		print "ERROR: Check port is allowed through firewall and the remote user has access from mysql"
		return ("error")
		
	
def sqlcmd(sqlsrv,sqluser,pw2,cmd):
	"""Takes SQL Query to the Filr DB"""
	#print sqlsrv,sqluser,pw2
	con=sqlconnect(sqlsrv,sqluser,pw2,'filr')
	if con=="error":
		return
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	if len(items)==0:
		print "Error Not Found!!"
		return 
	
	con.close()
	return (items)
	


def idtouser(id):
	"""Takes Filr id number and converts to a User Name"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd="select * from SS_Principals where id in ("+id+")"
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row()
	if len(items)==0:
		print "Error Not Found!!"
		return 
	user=items[0][10]
	ldapcn=items[0][11]
	fname=items[0][17]
	print "User Name is :"+user
	print "LDAP CN is   :"+ldapcn
	print "Full Name is :"+fname
	con.close()
	return (user,ldapcn,fname)
	
def usertoid(user):
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select id,name,title,foreignName from SS_Principals where type="user" and name=\"'+user+'\";'
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row()
	if len(items)==0:
		print "Error Not Found!!"
		return

	id=items[0][0]
	cn=items[0][1]
	fullname=items[0][2]
	ldap=items[0][3]
	print "ID is :"+id
	if id<>"1":
		print "LDAP CN is   :"+ldap
		print "Full Name is :"+fullname
	return (id,cn,fullname,ldap)
	
def listusers():
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	con=sqlconnect('hhefs13','root','n0v3ll!!','filr')
	cmd='select id,name,title,foreignName from SS_Principals where type=\"user\";'

	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	for line in items:
		print line[0],line[1],"("+line[2]+")",line[3]
	print
	print "Total Number of Users "+str(len(items))
	return
	
def listnf():
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd="select f.pathName as filrPath, concat(r.rootPath, '/', f.resourcePath) as UNC, r.name as netFolderServer from SS_Forums f inner join SS_ResourceDriver r on f.resourceDriverName=r.name where f.parentBinder=36;"

	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	if len(items)==0:
		print "Error Not Found!!"
		return
	for line in items:
		print line[2],"\t"+line[1].replace("/Home Workspace/Net Folders/","")
	print
	print "Total Number of NetFolders is "+str(len(items))
	
	


	return
	
def fshomepath(user):
	"""lists files from location in File-system"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select * from SS_Forums where homeDir=1 and resourcePath like "%'+user+'%";'
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	id=items[0][0]
	filrpath=items[0][10]
	uncpath=items[0][11]
	uncpath=uncpath.replace("\\","/")
	#print uncpath
	con1=filrpath.split("-")
	#print con1
	

	files=os.listdir("\\\\"+con1[0]+"\\"+con1[1]+"\\"+uncpath)
	path="\\\\"+con1[0]+"\\"+con1[1]+"\\"+uncpath
	path=path.replace("/","\\")
	print path
	#print "test1"
	#print files
	
	con.close()
	return(files,path)
	

def listallhomedir():
	""" Routine to list all the defined home folders on a Filr System"""
	hf1=[]
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select * from SS_Forums where homeDir=1;'
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	for line in items:
		#print line
		#print "="*40
		id=line[0]
		name=line[11]
		hf=line[10]
		print id,"("+name+")",hf
		hf1.append([id,name,hf])
	print
	print "Number of Homedirectories is "+str(len(items))
	print
	
	return hf1
	



def listhomedir(user):
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select * from SS_Forums where homeDir=1 and resourcePath like "%'+user+'%";'
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	id=items[0][0]
	filrpath=items[0][10]
	uncpath=items[0][11]
	print id,filrpath,uncpath
	con.close()
	return

def jitsenable(id):
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='UPDATE `filr`.`SS_Forums` SET `jitsEnabled`=1,jitsMaxAge=3600,jitsAclMaxAge=3600 WHERE `id`='+id+'; '
	con.query(cmd)
	result=con.use_result()
	con.query(cmd)
	con.close()
	return

def foldertoid(folderpath):
	"""Convert folder to folderid"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select * from SS_Forums where resourcePath=\"'+folderpath+'\";'
	
	
	print cmd
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	if len(items)==0:
		print "Error Not Found!!"
		return -1
	id=items[0][0]
	#print id
	con.close()
	return(id)
	
def idtofolder(id):
	"""Convert id to folder"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select * from SS_Forums where id=\"'+id+'\";'
	
	
	#print cmd
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	#print items
	#sys.exit()
	if len(items)==0:
		print "Error Not Found!!"
		return -1
	folder=items[0][11]
	con.close()
	return(folder)
	


def filesinfolder(folderpath):
	"""Number and names of files in a folder"""
	files=[]
	dirs=[]
	id=foldertoid(folderpath)
	if id=="-1":
		print "Error Folder Not Found in Filr DB"
		sys.exit()
	#print "folderid is "+str(id)
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd='select title from SS_FolderEntries where parentBinder=\"'+id+'\";'
	#print cmd
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	if len(items)==0:
		print "Error Not Found!!"
		return
	print "Number of Files found is "+str(len(items))
	#print "="*40
	for line in items:
		#print line[0]
		files.append(str(line[0]))
		
	
	cmd='select title from SS_Forums where parentBinder=\"'+id+'\";'
	#print cmd
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	if len(items)==0:
		print "Error Not Found!!"
		return
	#print "Number of Directories found is "+str(len(items))
	for line in items:
		#print "(DIR)"+line[0]
		dirs.append(str(line[0]))
		files.append(str(line[0]))	
	#print "="*40
	con.close()
	return(files)
	
def syncstatus(filr,fs):
	"""Comparison of network files with Filrs own database"""
	fsfiles,pth=fshomepath(filr)
	files=filesinfolder(fs)
	print "files in filesystem :"+str(len(fsfiles))
	print "files in filr       :"+str(len(files))
	print "="*30
	set1=set(fsfiles)
	set2=set(files)
	diff=set1.difference_update(set2)
	diff1=list(set1)
	return(diff1,pth)
	
def finddir(dir):
	"""Find a named directory in filr"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd="select id,resourcePath,pathName from SS_Forums where pathName like '"+dir+"';"
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row()
	#print result.fetch_row()[0][10]
	if len(items)>0:
		print items
		return items[0][0]
	else:
		print "Error Directory In Filr Database Not Found"
		con.close()
		return
	cmd="select id,resourcePath,pathName from SS_Forums where pathName like '"+dir+"';"
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row()
	#print result.fetch_row()[0][10]
	if len(items)>0:
		#print items
		return items[0][0]
	else:
		print "Error Directory In Filr Database Not Found"
		return -1


def dirinbinder(serverurl,identity,dirname,user,password,s):
	"""Returns list of filr paths within a folder"""
	dirs=[]
	start_time=time.time()
	data=""
	
	filr_url = "https://"+serverurl+"/rest/folders/"+identity+"/library_tree"
	
	header1 = {'Content-type': 'application/json'}
	count=1
	#r = requests.get(filr_url,headers=header1,auth=(user, password), verify=False)
	data=filrapi(serverurl,"folders/"+identity+"/library_tree","","","",0,0,s)
	print data
	
	
	for temp in data["children"]:
		#print temp["item"]["id"],temp["item"]["title"]
		dirs.append([temp["item"]["id"],temp["item"]["title"]])
	for temp in dirs:
		if temp[1]==dirname:
			#print "folder found"
			id=temp[0]
			return (id)
	



def filrapi(serverurl,restcmd,data1,user,pw,debug=0,up=0,s=''):
	"""General Helper function for Rest Calls"""
	#print s
	#print "---------"
	filr_url="https://"+serverurl+"/rest/"+restcmd
	
	bcache=requests_cache.core.get_cache()
	
	if str(up)=="1":
		
		if requests_cache.backends.base.BaseCache.has_url(bcache,filr_url):
			if debug==1:
				print "Filr URL removed from cache"
			requests_cache.backends.base.BaseCache.delete_url(bcache,filr_url)
	header1 = {'Content-type': 'application/json'}
	if user<>"":
		s.auth=(user,pw)
		s.verify = False
		s.timeout =(20)
		s.headers={'Content-type': 'application/json'}
		r=s.get(filr_url,data=data1)
	else:
		#print "No username/password"
		r=s.get(filr_url,data=data1)
	if debug==1:
		print "Debug Enabled"
		print r.text
	try:
		data=json.loads(r.text)
	except ValueError:
		print "Authentication Error"
		sys.exit()
	return(data)




	

def filrapi1(serverurl,restcmd,data1,user,pw,debug=0,up=0,s=""):
	"""General Helper function for Rest Calls"""
	filr_url="https://"+serverurl+"/rest/"+restcmd
	#print data1
	print "Up in Filr API is "+str(up)
	bcache=requests_cache.backends.base.BaseCache()
	print bcache
	if up==1:
		#if requests_cache.backends.base.BaseCache.has_url(bcache,filr_url):
		print "Cached URL Deleted"
		requests_cache.delete_url(filr_url)
	header1 = {'Content-type': 'application/json'}
	if user<>"":
		r=requests.get(filr_url,data=data1,headers=header1,auth=(user,pw),verify=False,timeout=20)
	else:
		print "No username/password"
		r=requests.get(filr_url,data=data1,headers=header1,verify=False,timeout=20)
	if debug==1:
		print "Debug Enabled"
		print r.text
	try:
		data=json.loads(r.text)
	except ValueError:
		print "Authentication Error"
		sys.exit()
	return(data)


def idfolder(servername,folderid,user,password,s):
	"""(REST) take folder id and convert to folder"""
	data=filrapi(servername,"folders/"+str(folderid),"","","",0,0,s)
	path=data["path"]
	
	return(path)
	
	
	
def lf(serverurl,user,password,s):
	nf=[]
	#print s
	data=filrapi(serverurl,"net_folders","","","",0,0,s)
	l=data["count"]
	
	nf = [["" for x in xrange(2)] for x in xrange(l)] 
	
	#l=data["count"]
	#print l
	#print data["items"][0]["id"]
		
	for count in range(0,l):
		if count<>l:
			nf[count][0]=data["items"][count]["id"]
			nf[count][1]=data["items"][count]["path"].replace("/Home Workspace/Net Folders","")
		else:
			print "last line detected"
	user1=userinfo(serverurl,"","",s)
	uname=user1["name"]
	fname=user1["title"]
	idnum=wspaceid(serverurl,"","",s)

	shares=filrapi(serverurl,"workspaces/"+str(idnum)+"/library_folders","","","",0,0,s)
	for temp in shares["items"]:
		stat=temp["home_dir"]
		path=temp["path"]
		id=temp["id"]
		txt="/Home Workspace/Personal Workspaces/"+fname+" ("+uname+")"
		name1=path.replace(txt,"")
		if name1<>"/My Files Storage":
			nf.append([id,name1])
	

	return nf


def flist(serverurl,identity,user,password):
	"""Returns list of filr paths within a folder"""
	start_time=time.time()
	data=""
	flist={}
	tempdict={}
	state=True
	data1=urllib.urlencode({'recursive':'true'})
	data1 = json.dumps({"""recursive""": """true"""})
	#print serverurl,identity
	data=filrapi(serverurl,"folders/"+identity+"/library_files?recursive=true",data1,user,password)
	folders=filrapi(serverurl,"folders/"+identity+"/binder_tree","",user,password)
	count=len(folders["children"])
	#print folders["children"]
	for num in range(0,count):

		path=folders["children"][num]["item"]["path"]
		path=path.replace("/Home Workspace/Net Folders","")
		id1=folders["children"][num]["item"]["id"]
		#flist.update({id1:{"path":path}})
		tempdict.update({id1:{"parent":identity,"child":[],"path":path,"content":[]}})

	tempdict.update({identity:{"parent":identity,"child":[],"path":"/","content":[]}})	
	#print tempdict
	temp=[]
	
	#print "="*80
	#print "=="
	l=len(data["items"])
	print data["items"][0]["parent_binder"]["id"]

	print "----"
	
	
	
	#print data["items"][0]["name"]
	#print data["items"][0]["parent_binder"]
	oldfolderid=0
	tempname=[]
	files=[]
	data1=copy.deepcopy(data)
	parent="root"
	for num in range(0,l):
	
		name=data["items"][num]["name"]
		folderid=data["items"][num]["parent_binder"]["id"]
		print name,folderid
		
		if oldfolderid==folderid:
			#print folderid,oldfolderid
			#print "Match found"
			folderpath=oldfolderpath
			files.append(name)
		else:
			#if oldfolderid==0:
			files.append(name)
			#print "New Directory"
			#print folderid,oldfolderid
			
			try:
				folderpath=tempdict[folderid]["path"]
				# tempdict.update({folderid:{"parent":"root","path":path,"content":[],"child":[]}})
			except:
				folderpath=idfolder(serverurl,folderid,user,password).replace("/Home Workspace/Net Folders","")
			#tempdict.update({folderid:{"parent":"root","path":folderpath,"content":[],"child":[]}})
				
			
			#print folderpath

			#tempdict={folderid:{"path":folderpath,"name":name}}
		
		#tempdict.update({folderid:{"parent":"root","content":files,"path":folderpath,"child":[]}})
		try:
			content=tempdict[folderid]["content"]
			content.append(name)
		except:
			content=[]
			content.append(name)
		tempdict.update({folderid:{"parent":"root","content":content,"path":folderpath,"child":[]}})
		#tempdict[folderid]["content"].append(name)
		#print tempdict[folderid]["content"]
		print files
		print "---"
		files=[]
			
			

		#print folderpath.replace("/Home Workspace/Net Folders","")+"/"+name
		oldfolderid=folderid
		oldfolderpath=folderpath
		
		#print type(oldfolderid)
	#print tempdict	
	print "Number of Files "+str(l)
	
	print
	print "Time taken to run command is "+str(time.time()-start_time),"seconds"
	print
	#print "="*80
	return (tempdict)
	
	
def searchdict(diction,key,value):
	for key1, value1 in diction.iteritems():
		#print value1["path"],key1
		if value1["path"] == value:
			return(key1)
	return(0)
	

def filetoidr(filename,folderid,servername,user,pw,s=""):
	data=filrapi(servername,"folders/"+folderid+"/library_files","","","",0,0,s)
	idnum=0
	for temp in data["items"]:
		#print temp
		#sys.exit()
		if temp["name"]==filename:
			idnum=temp["owning_entity"]["id"]
			#print temp
			
			# print idnum
	return(idnum)
	

	

	
def browsenf(servername,folderid,user,pw):
	filpath=flist(servername,folderid,user,pw)
	#print filpath
	filpath1=copy.deepcopy(filpath)
	#key1=searchdict(filpath,"path","/NewNetfolder/meh")

	for temp in filpath1:
		path=filpath1[temp]["path"]
		parent=posixpath.dirname(path)
		parentid=searchdict(filpath1,"path",parent)
		t1=filpath[parentid]["child"]
		#print type(t1)
		t1.append(temp)
		#sys.exit()
		filpath[parentid]["child"]=t1
		#filpath[parentid]["child"].apppend(temp)
	
		filpath[temp]["parent"]=parentid
	
		#filpath.update({temp:{"parent":parentid}})
	return(filpath)

	
def delfile(name,folderid,serverurl,user,password,s=""):
	id=filetoidr(name,folderid,serverurl,"","",s)
	status=0
	filr_url = "https://"+serverurl+"/rest/folder_entries/"+str(id)
	print "Please Wait ...."
	#r = requests.delete(filr_url,auth=(user, password),verify=False)
	r = s.delete(filr_url)
	#print r.content
	try:
		data=json.loads(r.text)
		if data["code"]=="ENTRY_NOT_FOUND":
			print "Error File Not Found in NetFolder"
			status=1
	except:
		print "File "+name+" Has Been Deleted"
		status=0
	print "status "+str(status)
	up=1
	return(status)
	


def hashfile(afile, hasher, blocksize=65536):
	#afile=open(afile1,"rb")
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()
 

def mup(iddir,files,srv,user,password,s=""):
	"""Multiple upload"""
	
	if "*" in files:
			dirname=ntpath.dirname(files)
				
			filename=ntpath.basename(files)
			#print filename,dirname
				
			if os.path.isdir(dirname):
				#print "Directory Found"
				templist=os.listdir(dirname)
				matched=[]
				size=0
				l1=0
				total=0
				for line in templist:
					if fnmatch.fnmatch(line,filename):
						size=os.path.getsize(dirname+"/"+line)
						#print u"(file)\t"+line,size
						matched.append(line)
						total=total+int(size)
						l1=l1+1
				if len(matched)==0:
					print "No Files Selected"
				else:
					print "The Following Files Have Been Selected:"
					print
					for line in matched:
						print line
					#size=total/1024
					print
					print "============================================="
					print "The Size of Files to be uploaded is \t"+str(size)
					print "The Number of Files to be uploaded is \t"+str(len(matched))
					print "=============================================="
					print
					choice=raw_input("Do You Wish To Continue ?(y/n)")
					print
					if choice.upper()=="Y":
						#for line in matched:
						for line in tqdm(matched):
							filetemp=dirname+"/"+line
							status=upload(iddir,filetemp,srv,"","",s)
							#print data,status

					else:
						return 1
					up=1		
					return 0
				
	else:
		
		data,status=upload(iddir,files,srv,"","",s)
		#print status
		print
		return 1	
 
	

def upload(iddir,name,serverurl,user,password,s=""):
	start_time=time.time()
	identity=iddir
	if os.path.isfile(name):
		f1 = open(name, 'rb')
	else:
		print "ERROR: Source File Not Found"
		data=""
		up=0
		status=1
		return(data,status)
	print name
	pth=os.path.dirname(name)
	print "Please Wait ...."
	print
	
	path1=os.getcwd()
	os.chdir(pth)
	filr_url = "https://"+serverurl+"/rest/folders/"+str(identity)+"/library_files?file_name="+ntpath.basename(name)
	size=os.path.getsize(name)
	if size==0:
		print "ERROR: Cannot Upload 0 Byte File"
		status=1
		return
	mm=mmap.mmap(f1.fileno(),0,access=mmap.ACCESS_READ)
	with requests_cache.core.disabled():
		try:
			requests.packages.urllib3.disable_warnings()
			r = s.post(filr_url, data=mm)
			#print r
			#print r.text
		except:
			print "ERROR: Connection problem"
			status=1
			return
	mm.close()
	f1.close()
	os.chdir(path1)

	data=json.loads(r.text)
	
	if "code" in data.keys():
		if data["code"]=="FILE_EXISTS":
			print "ERROR: "+str(data["message"])
			status=1
	elif "length" in data.keys():
		print str(data["name"])+" size "+str(data["length"])+ "k Uploaded Successfully...."
		taken=time.time()-start_time
		print "File Uploaded in %5.3f Seconds" %taken
		status=0
	else:
		print "ERROR: Unspecified"
		status=1
	up=1
	return(data,status)




def filetoid(filename,path):
	"""Takes File and converts to id name"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd="select * from SS_FolderEntries where title='"+filename+"' and parentBinder='"+path+"';"
	#rint cmd
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row()
	#rint items
	#rint len(items)
	if len(items)<1:
		print "No Entries Found "
	con.close()
	return items[0][0]
	

		
	
def accesslist(path,filename):
	"""Takes Filename and lists who has been shared to"""
	dirid=foldertoid(path)
	id=filetoid(filename,dirid)
	
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd="select sharerid,recipient_id FROM SS_ShareItem where sharedEntity_id='"+id+" and deletedDate is null';"
	#cmd="select * from SS_ShareItem where sharedEntity_id='"+id+"'"
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	
	if len(items)<1:
		print "No Share Entries Found "
		
		
	print "File is "+filename
	print "There are "+str(len(items))+" Assignment(s)"
	print "The following shares have been found ..."
	print
	print
	count=1
	for lines in items:
		print "Entry "+str(count)
		print "Details of Item Sharer"
		print "======================="
		sharer=idtouser(lines[0])
		print
		print  "Details of Item Recipient"
		print "==========================="
		recipient=idtouser(lines[1])
		print
		count=count+1
	con.close()
	return
	

	
def numfiles():
	"""Number of files held within filr"""
	con=sqlconnect(sqlserver,sqluser,sqlpwd,'filr')
	cmd="select count(*) from SS_FolderEntries where title<>'null' and deleted='0';"
	#cmd="select * from SS_ShareItem where sharedEntity_id='"+id+"'"
	con.query(cmd)
	result=con.use_result()
	items=result.fetch_row(maxrows=0)
	num=items[0][0]
	print "Number of files held within filr is "+str(num)
	return num
	
def syncdir(user,pw,servername,foldername,folderpath):
	global auth
	auth=authwebdav(user,pw,servername)
	#print auth
	filrls(foldername+"/"+folderpath)
	
	
	
	return


def setsql(server,user,pwd):
	"""setup of database access credentials"""
	cred="Novell.Collaboration.db:"+user+"@"+server
	keyring.set_password(cred, user, pw)
	print "Password Set for "+cred
	
def version(server,user,pw,s):
	"""Report System Version"""
	vers=filrapi(server,"release_info","","","",0,0,s)
	return(vers)
	
def lnfs(server,user,pw,s):
	vers=filrapi(server,"release_info","","","",0,0,s)
	if vers["product_version"]<"1.1.0":
		print "Error: Version of Filr does not support the API"
		sys.exit()
	nfs=filrapi(server,"admin/net_folder_servers?include_full_details=true","","","",0,0,s)
	return(nfs)

def showres(stuff):
	for key, value in stuff.iteritems() :
		print key, value

def mkdir(parent,newfolder,server,user,pw,s):
	data1 = json.dumps({'title': newfolder})
	#print data1
	header1 = {'Content-type': 'application/json'}
	
	filr_url="https://"+server+"/rest/folders/"+str(parent)+"/library_folders"
	
	
	#status = requests.post(filr_url,data=data1,headers=header1, auth=(user, pw),verify=False)
	status = s.post(filr_url,data=data1,headers=header1)
	
	#print status.text
	data=json.loads(status.text)
	#print data
	if len(data)==2:
		print "Error: Folder Already exists"
		return 1
	else:
		print "Folder Created"
		return 0

def rmdir(folderid,server,user,pw,s=""):
	
	filr_url="https://"+server+"/rest/folders/"+folderid
	#status = requests.delete(filr_url, auth=(user, pw),verify=False)
	stats=s.delete(filr_url,verify=False)
	#print status.text
	try:
		data=json.loads(status.text)
		if len(data)==2:
			print "Error "+data["code"]
			status=1
			
	except:
		print "Folder Deleted"
		status=0
	return(status)
	
	
def unshdir(rootfldrid,folder,user,srv,pwd):
	
	userid=usersearch(user,srv,user,pwd)
	userid=userid[1]["id"]
	#print userid
	data=filrapi(srv,"folders/"+rootfldrid+"/library_entities/?keyword="+folder,"",user,pwd)
	#print len(data)
	id=str(data["items"][0]["id"])
	data=filrapi(srv,"folders/"+id+"/shares","",user,"password")
	try:
		shid=data["items"][0]["id"]
	except:
		print "Folder Not Shared"
		return("Error")
	
	while True:
		tmp=raw_input("Are you sure you wish to remove all shares for folder "+folder+" ?(y/n)")
		if tmp.lower()=="y":
			r = requests.delete("https://"+srv+"/rest/shares/"+str(shid),auth=(user, pw),verify=False)
			print "Delete Succeeded"
			status="Success"
			break
		else:
			print "Delete Aborted"
			status="Error"
	return(status)
	
def fileshare(fileid,userid,server,user,pw,expire,rights,notify="false"):
	
	
	rgt={"c":"CONTRIBUTOR","v":"VIEWER","e":"EDITOR"}
	check=rights.lower()
	
	try:
		rights=rgt[check]
		
	except:
		print "Error Invalid Rights"
		rgt[0]="Error"
		return("Error")
	header1 = {'Content-type': 'application/json'}
	data1=json.dumps({'recipient':{'type':'user','id':userid},'access':{'role':rights}})
	#print data1
	
	
	status=requests.post("https://"+server+"/rest/files/"+str(fileid)+"/shares?notify="+notify,data=data1,headers=header1,auth=(user,pw),verify=False,timeout=20)
	
	try:
		stat=json.loads(status.text)
		if "[200]" in stat:
			return("success")
	except ValueError:
		print "General Error"
		return("error")
		
	return("success")



def dirshare(folderid,userid,server,user,pw,expire,rights,notify="false"):
	
	
	rgt={"c":"CONTRIBUTOR","v":"VIEWER","e":"EDITOR"}
	check=rights.lower()
	
	try:
		rights=rgt[check]
		
	except:
		print "Error Invalid Rights"
		rgt[0]="Error"
		return("Error")
	header1 = {'Content-type': 'application/json'}
	data1=json.dumps({'recipient':{'type':'user','id':userid},'access':{'role':rights}})
	#print data1
	
	
	status=requests.post("https://"+server+"/rest/folders/"+str(folderid)+"/shares?notify="+notify,data=data1,headers=header1,auth=(user,pw),verify=False,timeout=20)
	
	try:
		stat=json.loads(status.text)
		if "[200]" in stat:
			return("success")
	except ValueError:
		print "General Error"
		return("error")
		
	return("success")
	
def usersearch(suser,server,user,pw,s):
	"""Find Named User in Filr"""
	data=filrapi(server,"users/?keyword="+suser,"",user,pw,0,0,s)
	l=len(data["items"])
	if l==0:
		return("None")
	else:
		return(data["items"])

def groupsearch(grpname,server,user,pw,s):
	data=filrapi(server,"groups","","","",0,0,s)
	for temp in data["items"]:
		
			if temp["name"]==grpname:
				return temp["id"]
	return 0

def abook(server,user,pw,s):
	data=filrapi(server,"users",server,"","",0,0,s)
	address=open("abook.conf","w")
	userlist=[]
	for temp in data["items"]:
		userlist.append([temp["id"],temp["name"],temp["email_address"]])
		
	pickle.dump( userlist, open( "users.p", "wb" ) )
		
	sys.exit()	

def readabook(fname):
	userlist=pickle.load(open( fname, "rb" ) )
	return userlist
	
def syncstat(name,server,user,pw):
	print
	data1=filrapi(server,"admin/net_folders?keyword="+name,"",user,pw)
	#print data1
	folderid=data1["items"][0]["id"]
	data=filrapi(server,"admin/net_folders/"+str(folderid)+"/sync","",user,pw)
	print "Sync Status for nf "+name
	print "===================="+"="*len(name)
	syncres(data)
	
def sync(name,server,user,pw):
	"""Sync a named netfolder need (needs a slash in fron of server name"""
	print
	data1=filrapi(server,"admin/net_folders?keyword="+name,"",user,pw)
	folderid=data1["items"][0]["id"]
	r = requests.post("https://"+server+"/rest/admin/net_folders/"+str(folderid)+"/sync" ,"", auth=(user, pw),verify=False)
	data=json.loads(r.text)
	print "Sync for nf "+name
	print "===================="+"="*len(name)
	syncres(data,"sync")
	print
	

def syncres(temp1,op="syncres"):
	print "Files Found\t"+str(temp1["files_found"])
	print "Files Added\t"+str(temp1["files_added"])
	print "Files Modified\t"+str(temp1["files_modified"])
	print ""
	print "Folders Found\t"+str(temp1["folders_found"])
	print "Folders Added\t"+str(temp1["folders_added"])
	print 
	print "NF IP Address\t"+str(temp1["node_ip_address"])
	print "NF Status\t"+str(temp1["status"].upper())
	print 
	sdate=parser.parse(temp1["start_date"])
	print "Start Time\t"+sdate.strftime("%d-%m-%Y %H:%M:%S")
	if op=="sync":
		edate=parser.parse(temp1["end_date"])
		print "End Date\t"+edate.strftime("%d-%m-%Y %H:%M:%S")
		print "Time Taken\t"+str(edate-sdate)
		
def lsnf_srv(srv,user,pw):
	nflist=filrapi(srv,"admin/net_folder_servers","",user,pw)
	print nflist["count"]
	print nflist["items"]
	return nflist["items"]
	
	

def lsnf(srv,user,pw,s,display="on"):
	"""list all defined Netfolders -- Must be Admin"""
	if user<>"admin":
		print "User is not admin !"
		return
	nflist=filrapi(srv,"admin/net_folders","","","",0,0,s)
	if display=="on":
		for temp in nflist["items"]:
			print "\n"
			print "Netfolder Name : "+temp["name"]
			print "================="+"="*len(temp["name"])
			print "Relative Path\t\t:"+temp["relative_path"]
			print "Home Directory\t\t:"+str(temp["home_dir"])
			print "Allow Desktop Sync\t:"+str(temp["allow_desktop_sync"])
			print "ID Number\t\t:"+str(temp["id"])
			print "Index Content\t\t:"+str(temp["index_content"])
			server=temp["server"]["href"][1:]
			#print server
			nfsrv=filrapi(srv,server,"","","",0,0,s)
			print
			print "Parent NF Server\t:"+nfsrv["name"]
			print "Server Path\t\t:"+nfsrv["server_path"]
			print "Server Type\t\t:"+nfsrv["driver_type"]
			print "Auth Type\t\t:"+nfsrv["auth_type"]
			print "Jits Enabled\t\t:"+str(nfsrv["jits_enabled"])
			print "Jits Max Age\t\t:"+str(nfsrv["jits_max_age"])
			print "Jits Max ACL\t\t:"+str(nfsrv["jits_max_acl_age"])
			print "Proxy Account\t\t:"+nfsrv["proxy_dn"]
		print "\n"
	return(nflist)
	
def nfsid(nfsname,server,user,pw,s):
	"""Find ID of Netfolder Server"""
	test=lnfs(server,user,pw,s)
	for temp in test["items"]:
		#print temp
		#print "===="
		if nfsname in temp["name"]:
			return temp["id"]
	state="error"
	return state
	
def crnfs(name,driver_type,server_path,auth_type,proxy_dn,proxy_password,server,debug,user,s):
	"""Create Netfolder Server"""
	header1 = {'Content-type': 'application/json'}
	filr_url = "https://"+server+"/rest/admin/net_folder_servers"
	validate={"driver_type":["oes","windows_server"],"auth_type":["nmas","ntlm","kerberos_then_ntlm"]}
	if driver_type not in validate["driver_type"]:
		error=1
		print "Error: Invalid Driver Type"
		return error
	if auth_type not in validate["auth_type"]:
		error=1
		print "Error: Invalid Auth Type"
		return error
	if user<>"admin":
		error=1
		print "Error: User Not Admin"
		return error
	
	
	data1=json.dumps({'name':name,'driver_type':driver_type,'server_path':raw(server_path),"auth_type":auth_type,"proxy_dn":proxy_dn,"proxy_password":proxy_password})	

	#r = requests.post(filr_url, data1,headers=header1,auth=(user, pw),verify=False)
	r = s.post(filr_url, data1,headers=header1,verify=False)
	data=json.loads(r.text)
	#print data
	if "message" in data:
		print "ERROR: "+str(data["message"])
		return 1
	return 0
	
	
def delnf(name,server,user,pw):
	"""Delete Netfolder"""
	idnum=0
	if user<>"admin":
		print "Error: User Not Admin"
		return 1
	nf=lsnf(server,user,pw,"off")
	for temp in nf["items"]:
		print temp["name"],nf
		if temp["name"]==name:
			print "nf found"
			idnum=temp["id"]
	if idnum<>0:
		header1 = {'Content-type': 'application/json'}
		filr_url = "https://"+server+"/rest/admin/net_folders/"+str(idnum)
		r = requests.delete(filr_url,data="",headers=header1,auth=(user, pw),verify=False)
		#print r.text
		return 0
	else:
		print "Error: Netfolder not found!"
		return 1
		
	return 0
	
	
	
	
def crnf(nfs,name,relative_path,server,rights,user,pw,debug=0,s=""):
	"""Create Netfolder """
	#print nfs,name,relative_path,server,rights,user,pw
	if user<>"admin":
		print "Error: User Not Admin"
		return 1
	idnum=nfsid(nfs,server,user,pw,s)
	if idnum=="error":
		print "Error: No Netfolder Server Found"
		return 1
	#print "NFS Server id is "+str(idnum)
	header1 = {'Content-type': 'application/json'}
	filr_url = "https://"+server+"/rest/admin/net_folder_servers/"+str(idnum)+"/net_folders"
	if len(rights)==7:
		#print rights[1]
		if rights[1]=="user":
			user1=usersearch(rights[0],server,user,pw,s)
			#print user1
			id1=user1[0]["id"]
			#rights[0]==str(user["id"])
			#print "User Index is "+str(id1)
		
		
		if rights[1]=="group":
			id1=groupsearch(rights[0],server,user,pw,s)
			rights[0]==id1
			#print grpi
			#print "Group Index is "+rights[0]
			if id1==0:
				return 1
	elif len(rights)==0:
		print
	else:	
		return 1
	
	
	if len(rights)==0:
	
		data1=json.dumps({'name':name,'relative_path':relative_path})
		#print data1
	else:
		data1=json.dumps({'name':name,'relative_path':relative_path,'jits_enabled':"true",'assigned_rights':[{'principal':{'id':str(id1),'type':rights[1]},'access':{"role":rights[2],'sharing':{'internal':rights[3],'external':rights[4],'public':rights[5],'grant_reshare':rights[6]}}}]})
        #print data1
	
	#r = requests.post(filr_url, data1, headers=header1, auth=(user,pw), verify=False)
	r=s.post(filr_url,data1,headers=header1)
	data=json.loads(r.text)
	if "message" in data:
		print data["message"]
		if "Successfully" in data["message"]:
			return 0
		return 1
	return 0


def savenfs(server,filename,user,s):
	"""Saves NFS Definitions to a named XML File"""
	if user<>"admin":
		print "ERROR: user is not admin"
		return
	print "Saving NFS to file "+filename+".xml"
	nfs=filrapi(server,"admin/net_folder_servers","","","",0,0,s)
	nfs=nfs["items"]
	xml=dicttoxml.dicttoxml(nfs,attr_type=False,custom_root="NFS")
	dom = parseString(xml)
	nfs=dom.toprettyxml()
	if not os.path.isdir(os.path.dirname(filename)):
		print "ERROR: Path does not exist"
		print
		return
	
	
	with open(filename+".xml", "w") as f:
		f.write(dom.toprettyxml(indent="  "))
	
	return(nfs)
	
def savenf(server,filename,user,s):
	"""Saves NF Definitions to a named XML File"""
	if user<>"admin":
		print "ERROR: user is not admin"
		return
		
	print "Saving NF to file "+filename+".xml"
	nfs=filrapi(server,"admin/net_folders","","","",0,0,s)
	nfs=nfs["items"]
	xml=dicttoxml.dicttoxml(nfs,attr_type=False,custom_root="NF")
	dom = parseString(xml)
	if not os.path.isdir(os.path.dirname(filename)):
		print "ERROR: Path does not exist"
		print
		return
	with open(filename+".xml", "w") as f:
		f.write(dom.toprettyxml(indent="  "))
	nf=dom.toprettyxml()
	return(nf)

def restnf(server,filename,user,s):
	"""Restores NF Definitions from a File to a named Filr"""
	if user<>"admin":
		print "ERROR: user is not admin"
		return
	rights=[]
	xmldoc = minidom.parse(filename+".xml")
	temp=xmldoc.getElementsByTagName("item")
	for items in temp:
		#print items.toxml()
		name=items.getElementsByTagName('name')
		nfs=items.getElementsByTagName('id')
		relative_path=items.getElementsByTagName('relative_path')
		href=items.getElementsByTagName('href')
		#home_dir=items.getElementByTagName('home_dir')
		#home_dir=home_dir[0].firstChild.data
		
		if len(name)<>0 and name[0].firstChild.data<>"Home":
			name=name[0].firstChild.data
			nfs=nfs[0].firstChild.data
			href=href[2].firstChild.data
			relative_path=relative_path[0].firstChild.data

			
			
			#print nfs,name,relative_path,nfs,href
			nfsname=filrapi(server,href[1:],"","","",0,0,s)
			nfs=nfsname["name"]
			#print "user is "+user
			status=crnf(nfsname["name"],name,relative_path,server,rights,user,"",1,s)
			if status==1:
				print "ERROR: Netfolder "+name+" not created"
			if status==0:
				print "Error Netfolder "+name+" Created Successfully"




def restnfs(server,filename,pword,user,s):
	"""Restores NFS Definitions from a File to a named Filr"""
	xmldoc = minidom.parse(filename+".xml")
	temp=xmldoc.getElementsByTagName("item")
	for items in temp:
		#print items.toxml()
		name=items.getElementsByTagName('name')
		driver_type=items.getElementsByTagName('driver_type')
		server_path=items.getElementsByTagName('server_path')
		auth_type=items.getElementsByTagName('auth_type')
		proxy_dn=items.getElementsByTagName('proxy_dn')
		
		
		
		if len(name)<>0:
			name=name[0].firstChild.data
			#print driver_type[0]
			driver_type=driver_type[0].firstChild.data
			server_path=server_path[0].firstChild.data
			server_path1=raw(server_path)
			auth_type=auth_type[0].firstChild.data
			proxy_dn=proxy_dn[0].firstChild.data
			#print name,driver_type,server_path,auth_type,proxy_dn
			
			status=crnfs(name,driver_type,server_path1,auth_type,proxy_dn,pword,server,0,user,s)
			if status==1:
				print "ERROR: Netfolder Server "+name+" not created"
			if status==0:
				print "Error Netfolder Server "+name+" Created Successfully"
				
			
def mdel(iddir,files,srv,user,password,s=""):
	"""Multiple upload"""
	
	if "*" in files:
			dirname=ntpath.dirname(files)
				
			filename=ntpath.basename(files)
			#print filename,dirname
				
			if os.path.isdir(dirname):
				#print "Directory Found"
				templist=os.listdir(dirname)
				matched=[]
				size=0
				l1=0
				total=0
				for line in templist:
					if fnmatch.fnmatch(line,filename):
						size=os.path.getsize(dirname+"/"+line)
						#print u"(file)\t"+line,size
						matched.append(line)
						total=total+int(size)
						l1=l1+1
				if len(matched)==0:
					print "No Files Selected"
				else:
					print "The Following Files Have Been Selected:"
					print
					for line in matched:
						print line
					#size=total/1024
					print
					print "============================================="
					print "The Size of Files to be deleted is \t"+str(size)
					print "The Number of Files to be deleted is \t"+str(len(matched))
					print "=============================================="
					print
					choice=raw_input("Do You Wish To Continue ?(y/n)")
					print
					if choice.upper()=="Y":
						for line in matched:
							filetemp=dirname+"/"+line
							#status=upload(iddir,filetemp,srv,"","",s)
							status=delfile(line,iddir,srv,"","",s)
							#print data,status

					else:
						return 1
					up=1		
					return 0
				
	else:
		status=delfile(line,iddir,srv,"","",s)
		#print status
		print
		return 1	
				
			
	
	
	
	
			
		
		

sqlserver="hhefs13"
sqluser="root"
sqlpwd="n0v3ll!!"




