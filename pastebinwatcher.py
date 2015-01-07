# -*- coding: utf-8 -*-

__author__ = 'n30'

import WebUtil #TODO: Replace this with the "requests" library
import FileUtil
import time
import re
import datetime

finish = False
sleepity = 3 #Seconds to sleep on each request. 1 second will make pastebin ban your ip.
numberoffounds = 0
print "Start of the search... "
linkcompare = "" #Prevents that we are re-watching the same link as before...

while (not finish):
	try:
		source = WebUtil.getWebPage("http://pastebin.com/archive","","")
		link = re.search('<ul class="right_menu"><li><a href="/([^"]*)">', source, re.IGNORECASE)
		source = WebUtil.getWebPage("http://pastebin.com/raw.php?i=" + link.group(1),"","")
		link = "http://pastebin.com/" + link.group(1)

		###REGULAR EXPRESSIONS###
		mails = re.findall(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+\.[a-zA-Z]{1,4}' , str(source).lower())
		password = re.search(r'.*password.*', source,re.IGNORECASE)
		passonly = re.search(r'.*pass[^a-z].*', source,re.IGNORECASE)
		user = re.search(r'.*user.*', source,re.IGNORECASE)

		###NUMBERS
		##Ask me for the part of this code
		##Regular expressions for Credit Cards

		#IP SEARCH
		ips = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', source, re.IGNORECASE)
		###END OF REGULAR EXPRESSIONS###
		#if cards:
		#	card = True
		#else:
		#	card = False

		if ((mails or password or passonly or card or user) and (linkcompare != link)):
			print "Found: ", link
			numberoffounds+=1
			FileUtil.appendToFile("<a href=\""+link+"\">"+link+"</a> Keywords found: ", "pastebinurls.html")

			if mails:
				FileUtil.appendToFile("E-mails ", "pastebinurls.html")
				print "[Saving e-mails...]"
				for mail in mails:
					FileUtil.appendToFile(mail+"\n","pastebinmails.txt")
			if password:
				FileUtil.appendToFile("Password ", "pastebinurls.html")
			if passonly:
				FileUtil.appendToFile("Pass ", "pastebinurls.html")
			if user:
				FileUtil.appendToFile("USER ", "pastebinurls.html")
			if ips:
				FileUtil.appendToFile("IPS ", "pastebinurls.html")
				print "[Saving ips...]"
				for ip in ips:
					FileUtil.appendToFile(ip + " <br/>\n", "pastebinIPS.html")
			#if card:
			#	#5up3r53cr3t

			FileUtil.appendToFile("<br/>", "pastebinurls.html")
			print "Continue searching... ", numberoffounds, " ocurrences at the time"
			linkcompare = link

		time.sleep(sleepity)
	except Exception, e:
		print ("[-] OOOPS:"), e.message
