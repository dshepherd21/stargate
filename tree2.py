import wx
import filr
from wx.lib.mixins.treemixin import VirtualTree
import sys
import time
import posixpath
from multiprocessing import Process, Queue
import threading
import Queue
import os
import requests
import urllib2
import json
import platform


from wx.lib.wordwrap import wordwrap

def rights(filename,folderid,srvname,user,pw):
	"""(REST) List Filr Shares for a file"""
	filename=filename.replace("(file) ","")
	id=filr.filetoidr(filename,folderid,srvname,user,pw,s)
	reply=[]
	if id<>0:
		rights=filr.filrapi(srvname,"folder_entries/"+str(id)+"/shares","","","",0,0,s)
		#recipient=rights["items"][0]["recipient"]
		#print shareing
		count = 1
		
		count=0
		reply.append("Access Rights for File "+filename+":")
		for temp in rights["items"]:
		
			#print temp["recipient"]
			reply.append("\n")
			reply.append("File Granted to User "+filr.idtoname(str(temp["recipient"]["id"]),srvname,user,pw))
			reply.append("Access Granted is :"+str(temp["access"]["role"]))
			reply.append("Reshare right granted "+str(temp["access"]["sharing"]["grant_reshare"]))
		if len(reply)==1:
			reply.append("File is shared with Nobody")
	else:
		print "ERROR file not found"
	return(reply)

def itemsearch(path1,templist):
	print "Running Item Search"
	#print templist[0][0]
	print templist
	print "Path is "+path1
	pathbits=path1.split("/")
	l=len(pathbits)
	print l
	print pathbits
	base="templist"
	count1=0
	marker=[]
	for count in range(1,l):
		print "tempbase="+base
		exec "tempbase="+base
		print tempbase
		print "=================="
		print count
		path1=pathbits[count]
		if count>1:
			path1="(dir) "+path1
		print "Path is "+path1
		for line in tempbase:
			print line[0]
			if line[0]==path1:
				print "found"
				print "index is "+str(count1)
				marker.append(count1)
				
				base=base+"["+str(count1)+"][1]"
				print "Base is "+base
				count1=0
				break
			count1=count1+1
		count1=0
	
		
		
		
	print base
	exec "print "+base
	base=base.replace("templist","items")
	exec "print "+base
	print marker
	return(base)
	


def findfolderid(folder,foldername):
	print folder
	print "foldername is"+foldername
	for temp in folder:
		print "temp item in loop is "+str(temp)
		path=nf[temp]["path"]
		print "Path is "+path
		print foldername[6:]
		if path.endswith(foldername[6:]):
			print "folderid is "+str(temp)
			return(temp)
	return(0)

def check1(val,temp,t1=""):
	print "Check Temp"
	print "-----------"
	val=val.replace("/","")
	print "Value is :"+val
	print len(temp)
	count=0
	for line in temp:
		print line
		print len(line)
		print "------"
		print line[0],val
		print "------"
		if line[0]==val:
		#if val in line:
			print "found"
			return(count)
		count=count+1
	print "----------------"
	print val
	print unicode(val)
	print "error"
	print "Index Test"
	print t1
	print temp
	#print temp.index(unicode(val))
	sys.exit()
	return(999)


def browse(server,folderid,user,pword,parent=1):
	userinfo=filr.userinfo(server,user,pword,s)
	wx.Yield()
	fname=userinfo["title"]
	start_time=time.time()
	global nf
	data=filr.filrapi(server,"folders/"+folderid,"","","",0,1,s)
	wx.Yield()
	path=data["path"].replace("/Home Workspace/Net Folders","")
	path=data["path"].replace("/Home Workspace/Personal Workspaces/"+fname+" ("+user+")","")
	
	data=filr.filrapi(server,"folders/"+folderid+"/folders","","","",0,1,s)
	#data=filr.filrapi(server,"folders/"+folderid+"/folders","","","",debug=1)
	wx.Yield()
	if parent==1:
		nf.update({int(folderid):{"parent":parent,"child":[],"path":path,"content":[]}})
	
	
	for temp in data["items"]:
		tempath=temp["path"].replace("/Home/Workspace/Net Folders","")
		tempath=tempath.replace("/Home Workspace/Personal Workspaces/"+fname+" ("+user+")","")
		
		nf.update({temp["id"]:{"parent":int(folderid),"child":[],"path":tempath,"content":[]}})
		print temp["id"]
		print "folderid is "+folderid
		print nf
		if temp["id"] not in nf[int(folderid)]["child"]:
			nf[int(folderid)]["child"].append(temp["id"])
			
	data=filr.filrapi(server,"folders/"+folderid+"/files","","","",0,1,s)
	wx.Yield()
	
	for temp in data["items"]:
		#print temp["name"]
		if temp["name"] not in nf[int(folderid)]["content"]:
			nf[int(folderid)]["content"].append(temp["name"])
			
			
	taken=time.time()-start_time
	print
	print "Time taken to run command is %5.3f seconds" %taken
	print	
	return(nf)	

class MyPopupMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        wx.Menu.__init__(self, *args, **kwargs)
		
        #self.WinName = "t

        item = wx.MenuItem(self, wx.NewId(), "Edit File")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.edit, item)

        item = wx.MenuItem(self, wx.NewId(),"Download File")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem2, item)

        item = wx.MenuItem(self, wx.NewId(),"View File")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)
        
    
        
    def OnItem3(self, event):
        print "View File selected in the %s window"%self.WinName


class MyTree(VirtualTree, wx.TreeCtrl):
    global p
    def __init__(self, *args, **kw):
        super(MyTree, self).__init__(*args, **kw)
        self.RefreshItems()
        #self.color="white"
        #OnTest emulates event that causes data to change
        self.Bind(wx.EVT_KEY_DOWN, self.OnTest)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.ExpanDed)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.edit)
        self.Bind(wx.EVT_TREE_ITEM_MENU,self.menu)
        

 
    def itemsel(self, evt):
		obj=evt.GetEventObject()
		item=evt.GetItem()
		root=self.GetItemText(item)
		print "============================"
		print "Item Selected"
		print root
		if root[0:5]<>"(dir)":
			print "File Found"
			print nf[folderid]
			
		print "============================="
       
    def ExpanDed(self, evt):
		global ind
		global parent
		parent=1
		global path
		global nf
		global folderid
		print "Item selected"
		# Get Items from gui
		obj=evt.GetEventObject()
		item=evt.GetItem()
		root=self.GetItemText(item)
		print "============================"
		print root
		print items
		print "============================="
		#ind=check1(root,items)
		#print "index1 "+str(ind)
		
		
		
		
		print "Entr Selected is "+root
		if root[0:5]=="(dir)":
			# If not root item then look in netfolder
			obj=nf[int(folderid)]["child"]
			folderid=findfolderid(obj,root)
			folderid=str(folderid)
			parent=0
			
		else:
			if parent==1:
				print "Root root is "+root
				ind=check1(root,items)
				folderid=str(resp[ind][0])
				#parent=0
		print "="*80
		print "Folder ID is "+str(folderid)
		print "Print Parent Value is "+str(parent)
		print "folderid "+folderid
		print "About to run Browse"
		print "="*80
		#text=raw_input("Press Any Key")
		nf=browse(srv,folderid,user,pw,parent)
		print "======="
		print nf
		print len(nf)
		print "========"
		
		print "Scan of Netfolder Completed"
		filtpath="/Home Workspace/Net Folders"
		#text=raw_input("Press Any Key")
		path=nf[int(folderid)]["path"].replace(filtpath,"")
		fullpath=path
		print "Path is "+path
		#items[0][1].append(('temp',[]))=
		#items[0][1].append(('dir2',[]))
		#items[0][1][0][1].append(('dir4',[]))
		#items[0][1][0][1][0][1].append(('dir6',[]))
		
		print "Path is :"+path
		
	
		l=len(temp)
		tempstr="items"
		fid=int(folderid)
		#items=items.remove(("temp",[]))
		#count=0
		
		for count in range(l-1):
			print count
			if count<>0:
				#tempstr=tempstr+"[0][1]"
				tempstr=tempstr+"[1]"
				#tempstr=tempstr+"[0]"
				
			else:
				#tempstr=tempstr+"[1]"
				#tempstr=tempstr+"[ind]"+"[1][0]"
				tempstr=tempstr+"[ind]"
			count=count+1
		temp2=[]
		
		
		print "================"
		print ind
		print
		print tempstr,temp[1]
		
		exec "print "+tempstr
		exec "templist="+tempstr
		print
		count1=0
		print "root is "+root
		print len(templist)
		print templist
		for temp99 in templist[1]:
			print temp99[0]
			if temp99[0]==root:
				print temp99[0]
				print "found"
				break
		
			count1=count1+1
			#print temp99
			#print count1
		ind1=count1
		print "counter value is "+str(count1)
		print "Index is "+str(count1)
		print "root index value is "+str(ind)
		#text=raw_input("Press a Key")
		
		count1=0
		print "================"
		#t9=raw_input("Press Any key to continue")
		
		print "================"
		#print items[0]
		#exec "print "+tempstr
		count1=0
		fid=int(folderid)
		print nf[fid]["content"]
		for temp1 in nf[fid]["content"]:
			value="(file) "+temp1
			print value
			temp2.append((value,[]))
			count1=count1+1
			#print appd
			#exec appd
			
		fid=int(folderid)
		print "FOLDER ID"
		print fid
		print "INDEX"
		print ind
		#count1=0
		#text=raw_input("press a key")
		l2=len(nf[fid]["child"])
		for temp1 in nf[fid]["child"]:
			dir=nf[temp1]["path"]
			value="(dir) "+posixpath.basename(dir)
			#temp2[count1][0].append((value,[]))
			temp2.append((value,[]))
			print temp2[0]
			temp2[count1][1].append((message,[]))
			#appd=tempstr+"[0][1].append((\"temp\",[]))"
			#print appd
			#exec appd
			count1=count1+1
			
			print u"(dir) "+posixpath.basename(dir)
			#sys.exit()
		print "1)"
		print temp2
		print "2)"
		print tempstr
		#sys.exit()
		rootpath=temp[1]
		print "-----------------"
		print rootpath
		print "-----------------"
		#ind=check1(rootpath,items)
		print temp2
		#print items[ind]
		#items[ind]=(items[ind][0],temp2)
		#items[ind]=(items[ind][0],temp2)
		
		#cmd1="items[ind]=("+str(tempstr)+"[0][0],temp2)"
		if root[0:5]=="(dir)":
			
			base=itemsearch(fullpath,items)
			print "fullpath is "+fullpath
			print "************************"
			print "Sample Base Is "+base
			print "************************"
			tempstr=base
			#cmd1=tempstr+"="+str(temp2)
			#cmd1="items[ind]=("+str(tempstr)+",temp2)"
			#exec "print "+tempstr+"[1][0]"
			exec "print "+tempstr+"[0]"
			#cmd1="del "+tempstr+"[1][0]"
			cmd1="del "+tempstr+"[0]"
			print "=============================="
			print cmd1
			exec cmd1
			print "=============================="
			print len(temp2)
			print temp2[0]
			print temp2[1]
			print tempstr
			exec "print "+tempstr
			print "==============================="
			for line in temp2:
				print "Line is "+str(line)
				#cmd1=tempstr+"[1].append(line)"
				cmd1=tempstr+".append(line)"
				print cmd1
				exec cmd1
				exec "print "+tempstr
			print "==============================="
			
			
			#text=raw_input("enter text")
			
			
		else:	
			cmd1="items[ind]=("+str(tempstr)+"[0],temp2)"
			exec cmd1
		print "INDEX"
		print ind
		print "value of cmd1 is "+cmd1

		
		print "======="
		
		#items[ind]=(items[ind][0],temp2)
		print items[ind]
		#text=raw_input("Enter a Key")
		
		
		#print temp
		#exec temp
		print items[ind]
		print items
		#sys.exit()
		self.RefreshItems() 
		#sys.exit()
			
		
		
    def OnTest(self, evt): 
        items[0]=(temp[1], [('item 2', [('a1', []),('b1', [])]), ('item 3', [])])
        #items[0][0]=(([('file1',[('file2',[]),('file2',[])])]))
        self.RefreshItems()        
    def OnGetItemText(self, index):
        #print index
        return self.GetText(index)
    def OnGetChildrenCount(self, indices):
        return self.GetChildrenCount(indices)
    def GetItem(self, indices):
        #print indices
        #print "====================="
        text, children = 'Hidden root', items
        for index in indices:
            text, children = children[index]
            #print index
            #print text,children
        return text, children
    def GetText(self, indices):
        return self.GetItem(indices)[0]
    def GetChildrenCount(self, indices):
        return len(self.GetChildren(indices))
    def GetChildren(self, indices):
        return self.GetItem(indices)[1]
    
    def menu(self,event):
        global filename
        global parent
        #menu1 = MyPopupMenu(self.color)
        item=event.GetItem()
        filename=self.GetItemText(item)
        print "File is "+filename
        print filename[0:5]
        menu1=wx.Menu()
        print "Parent Value is "+str(parent)
        if filename[0:6]=="(file)":
			item = wx.MenuItem(menu1, wx.NewId(), "Edit File")
			menu1.AppendItem(item)
			self.Bind(wx.EVT_MENU, self.edit, item)

			item = wx.MenuItem(menu1, wx.NewId(),"Download File")
			menu1.AppendItem(item)
			self.Bind(wx.EVT_MENU, self.download, item)

			item = wx.MenuItem(menu1, wx.NewId(),"View File")
			menu1.AppendItem(item)
			self.Bind(wx.EVT_MENU, self.view, item)
			
			item = wx.MenuItem(menu1, wx.NewId(),"Shared With")
			menu1.AppendItem(item)
			self.Bind(wx.EVT_MENU, self.shared, item)
			
			
        
        item = wx.MenuItem(menu1, wx.NewId(),"Upload File")
        menu1.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.upl, item)
        
        
        self.PopupMenu(menu1, event.GetPoint())
        menu1.Destroy()
        
    def shared(self,event):
		global folderid
		print "Filename is "+filename
		print "Server is "+srv
		print "Password is "+pw
		sharelist=""
		shares=rights(filename,folderid,srv,user,pw)
		for line in shares:
			sharelist=sharelist+line+"\n"
		print sharelist
		dlg = wx.MessageDialog(self, sharelist,
								"Access rights on file",
								wx.OK | wx.ICON_INFORMATION
								#wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
		dlg.ShowModal()
		dlg.Destroy()
	    
    def edit(self, event):
		#global s
		global filename
		print filename
		global folderid
		print "Folderid is "+str(folderid)
		obj=event.GetEventObject()
		if filename=="":
			item=event.GetItem()
			filename=self.GetItemText(item)
		
		
		print "File Edit Selected"
		file1=filename.replace("(file) ","")
		print file1
		tempdir=os.getenv("TEMP")
		dest=tempdir.replace("\\","/")+"/"+file1
		print "Destination path is "+dest
		print folderid
		
		name=posixpath.basename(dest)
		dirname=posixpath.dirname(dest)
		wx.Yield()
		id=filr.filetoidr(name,folderid,srv,user,pw,s)
		data=filr.filrapi(srv,"folders/"+folderid+"/files","","","",0,1,s)
		wx.Yield()
		filr_url=""
		for temp in data["items"]:
			if name==temp["name"]:
				filr_url=temp["permalinks"][-1]["href"]
				length=temp["length"]
	
		if filr_url=="":
			status=1
			print "Error"
			return(status)
		max = length
		
		
		#status=filr.download(posixpath.basename(dest),str(folderid),srv,posixpath.dirname(dest),user,pw)
		

		dlg = wx.ProgressDialog("File Download",
                               "File being downloaded "+posixpath.basename(dest),
                               maximum = max,
                               parent=self,
                               style = 0
                                | wx.PD_APP_MODAL
                                #| wx.PD_CAN_ABORT
                                #| wx.PD_CAN_SKIP
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME
                                #| wx.PD_AUTO_HIDE
                                )

		keepGoing = True
		count = 0
		status=0
		
		start_time=time.time()
		wx.Yield()
		
				
		local_filename = urllib2.unquote(filr_url.split('/')[-1])
		local_filename=dirname+"/"+local_filename
		print local_filename+" of size "+str(length)+"k"
		print "Being Downloaded ..."
		header1 = {'Content-type': 'application/json'}
		max=length
		chunk=2048
		count=0
		r=requests.get(filr_url,data="",headers=header1,auth=(user,pw),stream=True,verify=False)
		with open(local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=chunk): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					f.flush()
					count=count+3072
					#wx.MilliSleep(250)
					wx.Yield()
					if count<max:
						skip=dlg.Update(count)

		dlg.Destroy()
		print 
		taken=time.time()-start_time
		
		os.system("\""+dest+"\"")
		
		fname=dest
		size=os.path.getsize(fname)
		size=size/1024
		print "File Download Finished"
		taken=time.time()-start_time
		print "File Downloaded in %5.3f Seconds" %taken
		dlg = wx.ProgressDialog("File Uploaded",
								"File being Uploaded "+os.path.basename(fname),
								maximum = size,
								parent=self,
								style = 0
								| wx.PD_APP_MODAL
								#| wx.PD_CAN_ABORT
								#| wx.PD_CAN_SKIP
								| wx.PD_ELAPSED_TIME
								| wx.PD_ESTIMATED_TIME
								| wx.PD_REMAINING_TIME
								#| wx.PD_AUTO_HIDE
								)

		keepGoing = True
		count = 0
		status=0
		start_time=time.time()
		identity=folderid
		#filr_url = "https://"+srv+"/rest/folders/"+identity+"/library_files?file_name="+os.path.basename(fname)+"&force_overwrite=true"
		filr_url = "https://"+srv+"/rest/folders/"+identity+"/library_files?file_name="+os.path.basename(fname)+"&overwrite_existing=true"
		data = json.dumps({'file_name':fname})
		if os.path.isfile(fname):
			files = open(fname, 'rb')
		else:
			print "ERROR: Source File Not Found"
			return
		print "Please Wait ...."
		skip=dlg.Update(size)
		wx.Yield()
		r = requests.post(filr_url, files, auth=(user, pw),verify=False)
		data=json.loads(r.text)
		wx.Yield()
		l=len(data)
		print data
		if l<=2:
			print "ERROR: "+str(data["message"])
		else:
			#print d
			print str(data["name"])+" size "+str(data["length"]/1024)+ "k Uploaded Successfully...."
			taken=time.time()-start_time
			print "File Uploaded in %5.3f Seconds" %taken
		
         

        # Compare this with the debug above; did we change working dirs?
        

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
		dlg.Destroy()

		
		
	
    def download(self, event):
		global file1
		print self
		print "File Download Selected"
		print filename
		wildcard="All files (*.*)|*.*"
		file1=filename.replace("(file) ","")
		print file1
		dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), defaultFile=file1, wildcard=wildcard, style=wx.SAVE)
		dlg.SetFilterIndex(2)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			dest=path.replace("\\","/")
			print "Destination path is "+dest
			print folderid
			name=posixpath.basename(dest)
			dirname=posixpath.dirname(dest)
			id=filr.filetoidr(name,folderid,srv,user,pw,s)
			data=filr.filrapi(srv,"folders/"+folderid+"/files","","","",0,1,s)
			wx.Yield()
			filr_url=""
			for temp in data["items"]:
				if name==temp["name"]:
					filr_url=temp["permalinks"][-1]["href"]
					length=temp["length"]
	
			if filr_url=="":
				status=1
				print "Error"
				return(status)
			max = length

			dlg = wx.ProgressDialog("File Download",
                               "File being downloaded "+posixpath.basename(dest),
                               maximum = max,
                               parent=self,
                               style = 0
                                | wx.PD_APP_MODAL
                                | wx.PD_CAN_ABORT
                                #| wx.PD_CAN_SKIP
                                #| wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME
                                #| wx.PD_AUTO_HIDE
                                )

			keepGoing = True
			count = 0
			status=0
			
			start_time=time.time()
			wx.Yield()
			
			wx.Yield()
			
		
			
			local_filename = urllib2.unquote(filr_url.split('/')[-1])
			local_filename=dirname+"/"+local_filename
			print local_filename+" of size "+str(length)+"k"
			print "Being Downloaded ..."
			header1 = {'Content-type': 'application/json'}
			max=length
			chunk=3072
			count=0
			r=requests.get(filr_url,data="",headers=header1,auth=(user,pw),stream=True,verify=False)
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=chunk): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
						f.flush()
						count=count+3072
						#wx.MilliSleep(250)
						wx.Yield()
						if count<max:
							skip=dlg.Update(count)

			dlg.Destroy()
			print 
			taken=time.time()-start_time
			print "File Downloaded in %5.3f Seconds" %taken
			dlg = wx.MessageDialog(self, 'File '+posixpath.basename(local_filename)+" "+str(length)+"k downloaded in %5.3f seconds" %taken,
			'Download Completed',
			wx.OK | wx.ICON_INFORMATION
			#wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
			)
			dlg.ShowModal()
			dlg.Destroy()    
			
		

			
			
			
			
            # Normally, at this point you would save your data using the file and path
            # data that the user provided to you, but since we didn't actually start
            # with any data to work with, that would be difficult.
            # 
            # The code to do so would be similar to this, assuming 'data' contains
            # the data you want to save:
            #
            # fp = file(path, 'w') # Create file anew
            # fp.write(data)
            # fp.close()
            #
            # You might want to add some error checking :-)
            #
			print "Download Done"

		# Destroy the dialog. Don't do this until you are done with it!
		# BAD things can happen otherwise!
		#dlg.Destroy()

        
    def view(self, event):
		global file1
		print "File View Selected"
		print filename
		file1=filename.replace("(file) ","")
		print file1
		tempdir=os.getenv("TEMP")
		dest=tempdir.replace("\\","/")+"/"+file1
		print "Destination path is "+dest
		print folderid
		
		name=posixpath.basename(dest)
		dirname=posixpath.dirname(dest)
		wx.Yield()
		id=filr.filetoidr(name,folderid,srv,user,pw,s)
		data=filr.filrapi(srv,"folders/"+folderid+"/files","","","",0,1,s)
		wx.Yield()
		filr_url=""
		for temp in data["items"]:
			if name==temp["name"]:
				filr_url=temp["permalinks"][-1]["href"]
				length=temp["length"]
	
		if filr_url=="":
			status=1
			print "Error"
			return(status)
		max = length
		
		
		#status=filr.download(posixpath.basename(dest),str(folderid),srv,posixpath.dirname(dest),user,pw)
		

		dlg = wx.ProgressDialog("File Download",
                               "File being downloaded "+posixpath.basename(dest),
                               maximum = max,
                               parent=self,
                               style = 0
                                | wx.PD_APP_MODAL
                                #| wx.PD_CAN_ABORT
                                #| wx.PD_CAN_SKIP
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME
                                #| wx.PD_AUTO_HIDE
                                )

		keepGoing = True
		count = 0
		status=0
		
		start_time=time.time()
		wx.Yield()
		
		#wx.Yield()			
		local_filename = urllib2.unquote(filr_url.split('/')[-1])
		local_filename=dirname+"/"+local_filename
		print local_filename+" of size "+str(length)+"k"
		print "Being Downloaded ..."
		header1 = {'Content-type': 'application/json'}
		max=length
		chunk=3072
		count=0
		r=requests.get(filr_url,data="",headers=header1,auth=(user,pw),stream=True,verify=False)
		with open(local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=chunk): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					f.flush()
					count=count+3072
					#wx.MilliSleep(250)
					wx.Yield()
					if count<max:
						skip=dlg.Update(count)

		dlg.Destroy()
		print 
		taken=time.time()-start_time
		
		os.system("\""+dest+"\"")
	
    def upl(self,event):
		print folderid
		dlg = wx.FileDialog(
			self, message="Choose a file to upload",
			defaultDir=os.getcwd(), 
			defaultFile="",
			wildcard="*.*",
			style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
			)

		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			for path in paths:
				print path
			fname=path
			size=os.path.getsize(fname)
			size=size/1024
           
		dlg = wx.ProgressDialog("File Uploaded",
								"File being Uploaded "+os.path.basename(fname),
								maximum = size,
								parent=self,
								style = 0
								| wx.PD_APP_MODAL
                                #| wx.PD_CAN_ABORT
                                #| wx.PD_CAN_SKIP
                                #| wx.PD_ELAPSED_TIME
								| wx.PD_ESTIMATED_TIME
								| wx.PD_REMAINING_TIME
                                #| wx.PD_AUTO_HIDE
								)

		keepGoing = True
		count = 0
		status=0
		start_time=time.time()
		identity=folderid
		filr_url = "https://"+srv+"/rest/folders/"+identity+"/library_files?file_name='"+os.path.basename(fname)+"'&overwrite_existing=true"
		print filr_url
		data = json.dumps({'file_name':fname})
		if os.path.isfile(fname):
			files = open(fname, 'rb')
		else:
			print "ERROR: Source File Not Found"
			return
		print "Please Wait ...."
		skip=dlg.Update(size)
		wx.Yield()
		r = requests.post(filr_url, files, auth=(user, pw),verify=False)
		data=json.loads(r.text)
		wx.Yield()
		l=len(data)
		#print data
		line1=str(data["name"])+" size "+str(data["length"]/1024)+ "k Uploaded Successfully...."
		taken=time.time()-start_time
		line2="File Uploaded in %5.3f Seconds" %taken
		if l<=2:
			print "ERROR: "+str(data["message"])
		else:
			dlg = wx.MessageDialog(self,line1+"\n"+line2,
								"Operation Completed",
								#wx.OK | wx.ICON_INFORMATION
								#wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
								)
			dlg.ShowModal()
			#dlg.Destroy()
			#print da
			print str(data["name"])+" size "+str(data["length"]/1024)+ "k Uploaded Successfully...."
			taken=time.time()-start_time
			print "File Uploaded in %5.3f Seconds" %taken
		
         

        # Compare this with the debug above; did we change working dirs?
        

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
		dlg.Destroy()


class TreeFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Filr Netfolder Browser',size = wx.Size(1000,1000))
        ico = wx.Icon('app.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
         
        menuBar = wx.MenuBar()
        # 1st menu from left
        menu1 = wx.Menu()
        menu1.Append(101, "&Filr Server", "Filr Options")
        menu1.Append(102, "&About", "")
        menu1.AppendSeparator()
        menu1.Append(103, "&Close", "Exit Programe")
        # Add menu to the menu bar
        menuBar.Append(menu1, "&Options")
        self.SetMenuBar(menuBar)
        self.tree = MyTree(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT) # Menu events
        
        
        
        self.Bind(wx.EVT_MENU_HIGHLIGHT_ALL, self.OnMenuHighlight)
        self.Bind(wx.EVT_MENU, self.CloseWindow, id=103)
        self.Bind(wx.EVT_MENU, self.server, id=101)
        self.Bind(wx.EVT_MENU, self.About, id=102)
        

        
    def OnMenuHighlight(self, event):
        id = event.GetMenuId()
        item = self.GetMenuBar().FindItemById(id)
        if item:
            text = item.GetText()
            help = item.GetHelp()

        # but in this case just call Skip so the default is done
        event.Skip()
    def server(self, evt):
		print "Server Selected"
		if os.path.isfile(os.getcwd()+"\\"+"server.conf"):
			print "File Found"
			server=open(os.getcwd()+"\\server.conf","r").readlines()
			print server
		else:
			server=open(os.getcwd()+"\\server.conf","w")
		dlg = wx.TextEntryDialog(self, 'Default Filr Server','Server Name', server[0])
		dlg.SetValue(server[0])
		if dlg.ShowModal() == wx.ID_OK:
			#print "value entered "+dlg.getvalue()
			server1=open(os.getcwd()+"\\server.conf","w")
			server1.write(server[0])
			server1.close()
		

		dlg.Destroy()
		
			
			
    
    
    def About(self, evt):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "PyFilr"
        info.Version = "0.5 Beta"
        info.Copyright = "(C) 2014 Novell Consulting"
        info.Description = wordwrap(
            "Experimental Filr Client Written with Python 2.7\nShould be CrossPlatform\nNo need to sync netfolders",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.novell.com")
        info.Developers = [ "David Shepherd",
                            "Polly the Cat",
                            "Victor the Cat" ]
        licenseText="Copyright Novell Consulting 2014"
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
    
    
    
    
    
    def CloseWindow(self, event):
        self.Close()
        
    




        

if __name__ == '__main__':
	# Initialise Global Variables
	osname=platform.system()
	print "os is "+osname
	ind=0
	tempstr=""
	filename=""
	path="/"
	nf={}
	folderid=0
	parent=1
	chunk=2048
	message="Waiting..."
	srv=open(os.getcwd()+"/server.conf","r").readlines()
	#srv="filr.novell.com"
	srv=srv[0]
	user=os.getenv("USERNAME")
	# Read Passwords from Credential Provider
	user,pw=filr.pw(srv,user,None)
	s=filr.auth(user,pw)
	# Extract User Info based on Credentials
	userinfo=filr.userinfo(srv,user,pw,s)
	fname=userinfo["title"]
	#print userinfo
	# Look at Root Folder Structure
	resp=filr.lf(srv,user,pw,s)
	print resp
	items=[]
	count=0
	for temp in resp:
		items.append((temp[1][1:],[]))
		items[count][1].append((message,[]))
		count=count+1
	
	print items
	#key=raw_input("Press Any Key")
	#ind=check1("test",items)
	app = wx.PySimpleApp()
	frame = TreeFrame()
	frame.Show()
	app.MainLoop()
