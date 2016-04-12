import os
import filr
srv="filrutp.utopia.novell.com"
user="admin"
user,pw=filr.pw(srv,user,None)
#print user,pw
s=filr.auth(user,pw)
rescount=100
term=raw_input("Search for ?")
temp=filr.srch(srv,"","",term,"true",s,rescount)
htmlfile=open("c:\\filr\\found.html","r").readlines()
results=open("c:\\filr\\results.html","w")
for temp1 in htmlfile:
	results.write(temp1)


print "Number of items found "+str(len(temp))
results.write("<table style=width=\"width:100%\">\n")
results.write("<tr>\n")
results.write("<th>Found Files</th>\n")
results.write("</tr>\n")
results.write("<tr>\n")
for line in temp:
	l1="<td><a href=\"file:///c:/users/"+user+"/Filr"+line+"\">"+line+"</a></td>\n"
	l1=l1.replace("/Home Workspace","")
	print l1
	results.write(l1+"\n")
	#results.write("<td><a href=\"file:///c:/users/"+user+"/Filr"+line+"\">"+line+"</a></td>\n")
	results.write("</tr>")
results.write("</body>\n")
results.write("</html>\n")
results.close()
os.system("c:\\filr\\results.html")

