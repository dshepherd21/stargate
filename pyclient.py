#!/usr/bin/env python
import urllib3
urllib3.disable_warnings()
import filr

import os
import sys
import json
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import posixpath
import shlex
from optparse import OptionParser
import platform
import getpass
import readline
import codecs
import locale
import fnmatch
import ping
import argparse
from dateutil import parser

CMD=["folderid","lsnf","syncstat","sync","unshdir","shdir","share","rmdir","mkdir","dir","up","cd","size","view","rights","shares","about","who","ldir","script","userid","savenf","loadnf"]

def chgpath(path):
	#print path[0]
	if "/" not in path:
		return(path)
	if path[0]=="/":
		return(path)
	if path[2]=="/":
		return(path)
	option1="*"+path
	option2=option1[0:2]
	option=option1.replace(option2,"/"+option1[1])
	return(option)
	

def complete(text, state,):
	"""Auto Complete Commands"""
	for cmd in COMMANDS:
		if cmd.startswith(text):
			if not state:
				return cmd
			else:
				state -= 1
                
def out(text):
	print text
	if scripton==1:
		log.write(text+"\n")
	return

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
        
        
        							
    
def shared(server,userid,user,pword,s="",parent=1):
	print s
	"""(REST) Routine to look at shared with Me Folder"""
	start_time=time.time()
	global nf
	data=filr.filrapi(server,"shares/with_user/"+str(userid),"","","",0,0,s)
	path="/Shared With Me"
	if parent==1:
		nf.update({int(userid):{"parent":parent,"child":[],"path":path,"content":[]}})
	
	for temp in data["items"]:
		type=temp["shared_entity"]["type"]
		url=temp["shared_entity"]["href"][1:]
		#print url
		data1=filr.filrapi(server,url,"",user,pword)
		#print data1
		if type=="folderEntry":
			#print data1["title"]
			if data1["title"] not in nf[int(userid)]["content"]:
				nf[int(userid)]["content"].append(data1["title"])
		if type=="folder":
			try:
				path=data1["path"]
				path=data["path"].replace("/Home Workspace/Personal Workspaces/"+fname+" ("+user+")","")
				#print path
				nf.update({data1["id"]:{"parent":int(userid),"child":[],"path":path,"content":[]}})
				if data1["id"] not in nf[int(userid)]["child"]:
					nf[int(userid)]["child"].append(data1["id"])
			except:
				error=1
	taken=time.time()-start_time
	print
	print "Time taken to run command is %5.3f seconds" %taken
	print
	
	return(nf)
	

def browse(server,folderid,user,pword,parent=1,up=0,s=""):
	start_time=time.time()
	global nf
	data=filr.filrapi(server,"folders/"+folderid,"","","",0,up,s)
	path=data["path"].replace("/Home Workspace/Net Folders","")
	path=data["path"].replace("/Home Workspace/Personal Workspaces/"+fname+" ("+user+")","")
	
	data=filr.filrapi(server,"folders/"+folderid+"/folders","","","",0,up,s)
	if parent==1:
		nf.update({int(folderid):{"parent":parent,"child":[],"path":path,"content":[]}})
	
	
	for temp in data["items"]:
		tempath=temp["path"].replace("/Home/Workspace/Net Folders","")
		tempath=tempath.replace("/Home Workspace/Personal Workspaces/"+fname+" ("+user+")","")
		nf.update({temp["id"]:{"parent":int(folderid),"child":[],"path":tempath,"content":[]}})
		if temp["id"] not in nf[int(folderid)]["child"]:
			nf[int(folderid)]["child"].append(temp["id"])
	
	if up==1:
		#print "Prior Change Detected"		
		data=filr.filrapi(server,"folders/"+folderid+"/files","","","",0,1,s)
		up=0
	else:
		data=filr.filrapi(server,"folders/"+folderid+"/files","","","",0,0,s)
		
	for temp in data["items"]:
		#print temp["name"]
		if temp["name"] not in nf[int(folderid)]["content"]:
			nf[int(folderid)]["content"].append(temp["name"])
			
			
	taken=time.time()-start_time
	print
	print "Time taken to run command is %5.3f seconds" %taken
	print
		
	return(nf)	




def title():
	cls()
	print 
	print "Welcome to PyFilr "+version
	print 
	print "========================================="
	print "Folders Available for user "+user
	print "========================================="
	print
	print


def cls():
	comp=platform.system()
	if comp=="Linux":
		os.system("clear")
	elif comp=="Windows":
		os.system("cls")	

version="0.98"
up=0
# Codec changes to support Unicode




readline.parse_and_bind(u"tab: complete")
readline.set_completer(complete)
#wrapped_stdout=codecs.getwriter('UTF-8')(sys.stdout)
#sys.stdout=wrapped_stdout

#parser = OptionParser()
#parser.add_option("-s","--server",help="Set Filr Server Name")
#parser.add_option("-u","--user",action="store",help="Filr User Name")
#parser.add_option("-r","--run",help="Set Script file to Run")
#parser.add_option("-c","--uni",help="Sets UTF8")
#parser.add_option("-p","--pw",help="Filr User Password"
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Set Filr Server Name")
parser.add_argument("-u", "--user", help="User Name")
parser.add_argument("-r", "--run", help="Set Filr Server script name")
parser.add_argument("-c", "--uni", help="Sets UTF 8")
parser.add_argument("-p", "--pw", help="Filr User Password")
                 
                    
options = parser.parse_args()



scripton=0
#options, args = parser.parse_args()
#print options,args
#sys.exit()
if options.run<>None:
	scripton=1
	scriptname=options.run
	print "Running Script is "+scriptname

if options.uni=="on":
	wrapped_stdout=codecs.getwriter('UTF-8')(sys.stdout)
	sys.stdout=wrapped_stdout


if options.user==None:
	user=os.getenv("USERNAME")
	print "Default User Selected"
else:
	user=options.user


if options.server==None:
	ftest=os.path.isfile(os.getcwd()+"/server.conf")
	if ftest==True:
		#print "selected"
		srv=open(os.getcwd()+"/server.conf","r").readline()
		srv=srv.replace("https://","")
		srv=srv.replace("/rest","")
	else:
		
		print "Error: server.conf file is not in the program directory File needs to contain the name of default server"
		sys.exit()
		
	print "Default Server Selected"
	print "Default Server is :"+srv
else:
	srv=options.server
	srv=srv.replace("https://","")
	srv=srv.replace("/rest","")
#print "Server URL is "+srv

stat="1"


if stat=="-1":
	print
	print "Error Server Not Found..."
	print
	sys.exit()

cls()

comp=platform.system()
print "Platform is "+comp
user,pw=filr.pw(srv,user,options.pw)
#print user,pw
s=filr.auth(user,pw)
#print s

resp=filr.lf(srv,user,pw,s)
resp.append([int(filr.usertoidr(srv,user,pw,s)),"/Shared With Me"])
usr=filr.userinfo(srv,user,pw,s)
fname=usr["title"]

if options.run==None:
	title()

	for temp in resp:
		print temp[1]

nf={}
tp=1
print
print
top=1
rootlist=[]
nonrootlist=[]
path1="Command : "
#scripton=0
#scriptname="temp.scr"
first="yes"
command=""

while tp==1:
	if top==1:
		for items in resp:
			rootlist.append(items[1])
		#print rootlist
		COMMANDS=CMD+rootlist
	if top<>1:
		#print current
		for item in nf[current]["content"]:
			#print item
			nonrootlist.append(item)
		for item in nf[current]["child"]:
			#print item
			path=nf[item]["path"]
			if posixpath.basename(path) not in nonrootlist:
				nonrootlist.append(posixpath.basename(path))
		#print nonrootlist
		COMMANDS=CMD+nonrootlist
	
	
	#print COMMANDS
	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)
	
	if scripton==0:
		cmd=raw_input(path1)
	else:
		
		if first=="yes":
			time2=start_time=time.time()
			scriptcmd=open(scriptname,"r")
			log=open(scriptname+".out","w")
			cmd=scriptcmd.readline()
			out("Executing "+cmd)
			first="no"
		else:
			cmd=scriptcmd.readline()
			if len(cmd)==0:
				out("="*60)
				out("End of Script")
				
				taken2=time.time()-time2
				out("Time taken to run script is %5.3f seconds" %taken2)
				out("="*60)
				out("\n")
				scripton=0
			
	
	
	COMMANDS=[]
	nonrootlist=[]
	if cmd=="quit":
		print "Program finished"
		sys.exit()
		
	if cmd[0:2]=="cd":
		try:
			cmds=shlex.split(cmd)
		except ValueError:
			out("Missing quote")
			cmds=""
		
		if len(cmds)==2:
			option=chgpath(cmds[1])
			#print option
			if top==1:
				for temp in resp:
					if option==temp[1]:
						path1=option+": "
						#nf=filr.browsenf(srv,str(temp[0]),user,pw)
						#print temp[0]
						if option<>"/Shared With Me":
							nf=browse(srv,str(temp[0]),"","",1,0,s)
						else:
							nf=shared(srv,str(temp[0]),"","",s)
							#nf=shared(srv,str(temp[0]),"","",1,0,s)
						#print nf
						
						current=int(temp[0])
						
						#print "Please Wait.."
						#print nf
						top=2
						
			
			if top==2 and option=="/":
				# print "check 2"
				top=1
				path1="Command : "
				nf={}
				out("Top of Netfolder Selected")
				out("\n")
				
			if top==2 and option[0:1]<>"/":
				
				l=len(option)
				for temp1 in nf:
					dir=nf[int(temp1)]["path"]
					if str(dir[-l:])==option:
						t1=nf[int(temp1)]["path"]
						
						path=filr.filterpath(t1,["/Home Workspace/Net Folders","/Home Workspace/Personal Workspaces/"+fname+" ("+user+")"])
						
						
						
						t1=path
						out(path)
						temp[0]=temp1
						path1=t1+": "
						current=temp1
						#print current
					#print "=================="
				#print "check"
			
			if top==2 and option=="..":
				#print nf[current]
				parent=nf[current]["parent"]
				if parent<>1:
					path=nf[parent]["path"]
					path2=filr.filterpath(path,["/Home Workspace/Net Folders","/Home Workspace/Personal Workspaces/"+fname+" ("+user+")"])
					temp[0]=parent
					path1=path2+": "
					current=parent
				else:
					top=1
					out("Top of Netfolder Selected")
					nf={}
					path1="Command : "
			
		
	if cmd[0:3]=="dir":
		#print top
		out("")
		out("dir selected "+command)
		out("============")
		out("")
		try:
			cmds=shlex.split(cmd)
		except ValueError:
			out("Missing quote")
			cmds=""
			
		
		if top==1 and len(cmds)==1:
			cls()
			title()
			for temp in resp:
				out(temp[1])
			out("\n")
			out("\n")
		elif top==2 and len(cmds)==2:
			
			out("Current Path is "+nf[current]["path"])
			#print "up is "+str(up)
			if nf[current]["path"]<>"/Shared With Me":
				if up==1:
					#print "Change Detected!!!"
					nf=browse(srv,str(current),user,pw,2,1,s)
				else:
					nf=browse(srv,str(current),user,pw,2,0,s)
					
			else:
				nf=shared(srv,str(current),user,pw,2,0)
			root=current
			#print nf[root]["child"]
			
			l1=0
			for temp1 in nf[root]["content"]:
				#print temp1
				if fnmatch.fnmatch(temp1,cmds[1]):
					out(u"(file) "+temp1)
					l1=l1+1
			
			l2=0
			for temp1 in nf[root]["child"]:
				#print temp1
				dir=nf[temp1]["path"]
				#print dir
				#print temp1,cmds[1]
				if fnmatch.fnmatch(dir,cmds[1]):
					out(u"(dir) "+posixpath.basename(dir))
					l2=l2+1
			out("\n")
			out(str(l1)+" files and "+str(l2)+" directories")
			print
		
		elif top==2 and len(cmds)==1:
			out("Current Path is "+nf[current]["path"])
			#print "up is "+str(up)
			out("")
			if nf[current]["path"]<>"/Shared With Me":
				if up==1:
					nf=browse(srv,str(current),user,pw,2,up,s)
					up=0
				else:
					nf=browse(srv,str(current),user,pw,2,up,s)
			else:
				nf=shared(srv,str(current),user,pw,s)
			root=current
			
			l1=len(nf[root]["content"])
			for temp1 in nf[root]["content"]:
				
				out(u"(file) "+temp1)
			
			l2=len(nf[root]["child"])
			for temp1 in nf[root]["child"]:
				#print temp
				dir=nf[temp1]["path"]
				out(u"(dir) "+posixpath.basename(dir))
			out("\n")
			out(str(l1)+" files and "+str(l2)+" directories")
			out("\n")

		cpath=temp[1]
	
	if cmd[0:2]=="up" and top==2:
		print 
		print "File Upload Selected"
		print "===================="
		print
		try:
			if comp<>"Windows":
				cmds=shlex.split(cmd)
			else:
				cmds=cmd.split(" ")
		except ValueError:
			out("Missing quote")
			cmds=""
		
		if len(cmds)<>2:
			out("Command Invalid- up \"source-file\"")
		if len(cmds)==2:
			source=filr.raw(cmds[1])
			#print cmds[1],source
			status=filr.mup(current,source,srv,"","",s)
			up=1
			
			
	if cmd[0:3]=="del":
			print "File Delete Selected"
			try:
				cmds=shlex.split(cmd)
			except ValueError:
				print "Missing quote"
				cmds=""
			if len(cmds)==2:
				source=cmds[1]
				sourcefolderid=current
				if scripton==0:
					cmd=raw_input("Delete File "+source+ "(y/n) ? ")
					if cmd=="y" or cmd=="Y":
						status=filr.delfile(source,str(sourcefolderid),srv,"","",s)
						up=1
						if status==0:
							#print nf[sourcefolderid]["content"]
							nf[sourcefolderid]["content"].remove(source)
				else:
					status=filr.delfile(source,str(sourcefolderid),srv,"","",s)
					
					up=1
					if status==0:
						out("")
						out("Deleted file Name "+source)
						out("")
						#print nf[sourcefolderid]["content"]
						nf[sourcefolderid]["content"].remove(source)
					
						
	if cmd[0:6]=="rights":
			#cmds=cmd.split(" ")
			try:
				cmds=shlex.split(cmd)
			except ValueError:
				print "Missing quote"
				cmds=""
			
			if len(cmds)==2:
				print
				source=cmds[1]
				sourcefolderid=current
				filr.rights(source,str(sourcefolderid),srv,user,pw,s)
			if len(cmds)==1:
				print "Error Missing file name"
			print
	
	if cmd[0:2]=="dl":
		print 
		print "Download Selected"
		print "================="
		print
		if comp<>"Windows":
			try:
				cmds=shlex.split(cmd)
				#print cmds
			except ValueError:
				print "Missing quote"
				cmds=""
		else:
			cmds=cmd.split()
			
		
			
		#print len(cmds)
		if len(cmds)==3:
			dlname=cmds[1]
			dlpath=cmds[2]
			status=filr.download(dlname,str(current),srv,dlpath,"","",s)
			if status==0:
				print "File Download Completed Successfully"
				print
			else:
				print "Error in File Download"
				print
		else:
			print "Error in Command"
			print "dl filename localpath"
			print
			
	if cmd[0:4]=="view":
		print 
		print "View Selected"
		print "================="
		print
		try:
			cmds=shlex.split(cmd)
		except ValueError:
			print "Missing quote"
			cmds=""
		
		if len(cmds)==2:
			dlname=cmds[1]
			dlpath="c:/temp"
			status=filr.download(dlname,str(current),srv,dlpath,user,pw,s)
			if status==0:
				print "File Download Completed Successfully"
				print
				#cmd="start \""+dlpath+"/"+dlname+"\""
				cmd="\""+dlpath+"/"+dlname+"\""
				print cmd
				os.system(cmd)
			else:
				print "Error in File Download"
				print
		else:
			print "Error in Command"
	
	
	if cmd[0:6]=="loadnf":
		print
		print "Restore NF and NF Server Selected"
		print "==============================="
		if comp<>"Windows":
			try:
				cmds=shlex.split(cmd)
			except ValueError:
				print "Missing quote"
				cmds=""
		else:
			cmds=cmd.split()
			
		if len(cmds)==3:
			print
			path=filr.raw(cmds[1])
			proxy_user_pw=cmds[2]
			nf=path+"-nf"
			nfs=path+"-nfs"
			print "Restoring two files: "
			print nf
			print nfs
			print "\n"
			print "One holds the Netfolders and one the Netfolder Servers"
			print "\n"
			temp=filr.restnfs(srv,nf,proxy_user_pw,user,s)
			temp=filr.restnf(srv,nfs,s)
			print
		else:
			print
			print "ERROR: Command Missing path"
			print
	
	
	
	if cmd[0:6]=="savenf":
		print
		print "Save NF and NF Server Selected"
		print "==============================="
		if comp<>"Windows":
			try:
				cmds=shlex.split(cmd)
			except ValueError:
				print "Missing quote"
				cmds=""
		else:
			cmds=cmd.split()
			
		if len(cmds)==2:
			print
			path=filr.raw(cmds[1])
			nf=path+"-nf"
			nfs=path+"-nfs"
			print "Creating two files: "
			print nf
			print nfs
			print "\n"
			print "One holds the Netfolders and one the Netfolder Servers"
			print "\n"
			temp=filr.savenf(srv,nf,user,s)
			temp=filr.savenfs(srv,nfs,user,s)
			print
		else:
			print
			print "ERROR: Command Missing path"
			print
	
	
			
	if cmd[0:6]=="shares":
		print 
		print "Shares Selected"
		print "================="
		print
		try:
			cmds=shlex.split(cmd)
		except ValueError:
			print "Missing quote"
			cmds=""
		
		if len(cmds)==1:
			filr.shares(srv,user,pw,s)
		else:
			print "Error in Command"
			print "shares"
		print
	
	if cmd[0:6]=="script":
		print 
		print "Script Selected"
		print "==============="
		print
		try:
			cmds=shlex.split(cmd)
		except ValueError:
			print "Missing quote"
			cmds=""
		if len(cmds)==2:
			scriptname=cmds[1]
			print "scriptname is "+scriptname
			print
			scriptname=scriptname.replace("\\","/")
			if os.path.isfile(scriptname):
				print "script execution of "+scriptname+" started"
				scripton=1
			else:
				print "No file found"
		else:
			print "ERROR: command is script \"filename\""
			
		
			
	if cmd[0:5]=="about":
		print 
		print "About Selected"
		print "================="
		print
		#cmds=cmd.split(" ")
		cmds=shlex.split(cmd)
		#print len(cmds)
		if len(cmds)==1:
			cls()
			print "Program PyFilr Version "+version
			print "Written in Python 2.7"
			print " ========================="
			print "By David Shepherd"
			print "Novell Consulting"
			print "14th January 2013"
			print "fixes:"
			print "0.71:\ttab complete, improved username handling"
			print "0.90:\tUpload fixed, partial support of shared with me"
			print "0.91:\tWildcard name handling"
			print "0.95:\tBasic script handling"
			print "0.97:\tTested on the Raspberry PI"
			print "0.98:\tSharing of folders and nf sync added"
		print
		
	if cmd[0:4]=="size":
		print 
		print "Size Selected"
		print "================="
		print
		try:
			cmds=shlex.split(cmd)
		except ValueError:
			print "Missing quote"
			cmds=""
		if len(cmds)==2:
			dlname=cmds[1]
			status=filr.size(dlname,str(current),srv,user,pw,s)
			
		else:
			print "Error in Command"
			print "size filename"
		print
	
	if cmd[0:5]=="mkdir" and top==2:
		print
		print "mkdir selected"
		print
		up=1
		cmds=shlex.split(cmd)
		if len(cmds)==2:

			status=filr.mkdir(current,cmds[1],srv,user,pw,s)
			folderid=filr.dirinbinder(srv,str(current),cmds[1],user,pw,s)
			if status==0:
				print nf[current]
				nf[current]["child"].append(folderid)
				path=nf[current]["path"]+"/"+cmds[1]
				nf.update({int(folderid):{"parent":current,"child":[],"path":path,"content":[]}})
				
				print nf[current]
			up=1
		else:
			print "Error in Command"
			print "mkdir dirname"
	
	if cmd[0:5]=="rmdir":
		print 
		print "Remove Directory Selected"
		print
		cmds=shlex.split(cmd)
		
		if len(cmds)==2:
			folderid=filr.dirinbinder(srv,str(current),cmds[1],user,pw,s)
			#print folderid
			status=filr.rmdir(str(folderid),srv,"","",s)
			#print status
			if status==0:
				#print nf[current]
				#print nf[current]["child"]
				#print folderid
				nf[current]["child"].remove(folderid)
				del nf[folderid]
				#print nf[current]
				up=1
		else:
			print "Error in Command"
			print "rmdir dirname"
			
	
	if cmd[0:6]=="userid":
		print
		print "User ID Selected"
		print
		cmds=shlex.split(cmd)
		if len(cmds)==2:
			suser=cmds[1]
			data=filr.usersearch(suser,srv,user,pw,s)
			
			print "User Details for "+str(data[0]["name"])
			print "="*40
			print "\n"
			print "ID Number is\t"+str(data[0]["id"])
			print "Email Address\t"+str(data[0]["email_address"])
			print "\n"
			
		else:
			print "Error in Command"
			print "userid username"	
	
			
	if cmd[0:5]=="shdir":
		print 
		print "Share Directory Selected"
		print
		cmds=shlex.split(cmd)
		if len(cmds)==6:
			folderid=filr.dirinbinder(srv,str(current),cmds[1],user,pw,s)
			userid=filr.usersearch(cmds[2],srv,user,pw,s)
			usrnum=userid[0]["id"]
			if usrnum=="None":
				print "User Not Found"
			else:
				status=filr.dirshare(folderid,usrnum,srv,user,pw,cmds[3],cmds[4],cmds[5])
				#print status
				
			if status=="success":
				print "Folder "+cmds[1]+" Has been shared with User "+cmds[2]
				print
			
		else:
			print "Error in Command"
			print "shdir folder user expiration(days) rights(c,v,e) notify(true/false)"
	
	if cmd[0:7]=="unshdir":
		print 
		print "Remove All Shares for Folder Selected"
		print
		cmds=shlex.split(cmd)
		#print len(cmds)
		if len(cmds)==2:
			status=filr.unshdir(str(current),cmds[1],user,srv,pw)
					
			
		else:
			print "Error in Command"
			print "unshdir folder"
	
	if cmd[0:3]=="who":
		print 
		print "Who is selected "
		print "================="
		print
		#cmds=cmd.split(" ")
		cmds=shlex.split(cmd)
		#print len(cmds)
		if len(cmds)==1:
			print "User is logged in as "+user
			
		else:
			print "Error in Command"
			print "who"
		print
	
	if cmd[0:8]=="syncstat":
		cmds=shlex.split(cmd)
		if len(cmds)==2:
			for temp in resp:
				try:
					if temp.index(cmds[1])<>0:
						print "Folder Valid"
						filr.syncstat(cmds[1],srv,user,pw)
						break
				except:
					print ""
		else:
			print "Error in Command"
			print "syncstat foldername"
					
					
	if cmd[0:4]=="sync":
		cmds=shlex.split(cmd)
		if len(cmds)==2:
			for temp in resp:
				try:
					if temp.index(cmds[1])<>0:
						print "Folder Valid"
						filr.sync(cmds[1],srv,user,pw)
						break
				except:
					print ""
		else:
			print "Error in Command"
			print "sync foldername"
	
	if cmd[0:4]=="lsnf":
		print 
		print "lsnf is selected"
		print "================="
		cmds=shlex.split(cmd)
		if len(cmds)==1:
			temp=filr.lsnf(srv,user,"",s)
		else:
			print "Error in Command"
			print "lsnf"
		
		
	
		
	if cmd[0:4]=="ldir":
		print 
		print "ldir is selected "
		print "================="
		print
		files=0
		dirs=0
		cmds=shlex.split(cmd)
		if len(cmds)==2:
			path2=str(cmds[1])
			print "Local Dir of "+cmds[1]
			
			path3=posixpath.dirname(path2)
			
			filenam=posixpath.basename(path2)
			
			try:
				temp=sorted(os.listdir(path3))
			except:
				print "ERROR: Directory Not Found"
			print
			
			for line in temp:
			
				fpath=path3+"/"+str(line)
				if os.path.isfile(fpath):
					if fnmatch.fnmatch(line,filenam):
					
						print "(file) "+line
						files=files+1
				if os.path.isdir(path3+"/"+str(line)):
					if fnmatch.fnmatch(line,filenam):
						print "(dir) "+line
						dirs=dirs+1
			print
			print str(files)+" files and "+str(dirs)+" directories"
			print
		
			
		else:
			print "ERROR: Command wrongly formatted"
			print "ldir localdirname"
		print
	
	if cmd[0:4]=="help":
		print 
		print "Help Selected"
		print "============="
		print "The following commands are supported:"
		print
		print "dir\t\tDirectory Listing"
		print "cd folder	Change directory to new folder"
		print "cd ..\t\tChange directory to parent"
		print "del name\tDelete file"
		print "up file		Uploads file to current folder"
		print "dl file path	Downloads file from folder to named path"
		print "size file	Size of current File"
		print "view file	Downloads file from current folder and attempts to view it"
		print "rights file\tUsers who have been granted access to the file"
		print "shares \t\tLists all shares for the current user"
		print "about \t\tDetails about the client"
		print "who\t\tCurrent logged in user"
		print "ldir dir\tLocal Directory Listing"
		print "script scrname\tRuns an External Script"
		print "mkdir dirname\tMake a folder on Filr"
		print "rmdir dirname\tRemove a Folder on Filr"
		print "shdir fname user expiry-time rights notify"
		print "\t\t shares a directory with a user"
		print "unshdir fname \tstops an existing share"
		print "sync fldr \tSyncs a netfolder"
		print "syncstat fldr \tStatus of a netfolder sync"
		print "lsnf\t\tLists Netfolders in system"
		print "folderid \tFolderid of current folder"
		print "fileid filename\tFile id of selected file"
		print "savenf path\\filename\t saves nf and nfs to files"
		print "quit\t\tEnds program"
		print
	
	if cmd[0:4]=="cred":
		print
		print "Credential Save Selected"
		print "========================"
		print
		cmds=shlex.split(cmd)
		out("\n")
		if len(cmds)==3:
			cmds[1]=srvname
			cmds[2]=username
			cmds[3]=passwd
			print srvname,username,passwd
		else:
			out("ERROR: Invalid number of parameters")
		
			
		
	if cmd[0:8]=="folderid":
		print
		print "Folderid Selected"
		print "================="
		if tp<>0:
			try:
				out("Current Folder id is "+str(current))
			except:
				out("ERROR: Folder ID cannot be found from Root")
		else:
			print "No Netfolder Currently Selected"
			
		print
	
	if cmd[0:6]=="fileid":
		print
		print "Fileid Selected"
		print "================"
		print
		print "current is "+str(current)
		cmds=shlex.split(cmd)
		out("\n")
		if len(cmds)==2:
			if cmds[1] in nf[current]["content"]:
				id=filr.filetoidr(cmds[1],str(current),srv,"","",s)
				out("File ID is "+str(id))
			else:
				out("ERROR: File Name Not Found")
		out("\n")
		
		
	
	
	
				
				
				
				
			
			
			
			
		
		


	


