#!/usr/bin/python3

import os
import sys
import datetime
import random
from shutil import move
from subprocess import call

defaultFileNum = 4
def movePodcasts(sourceBase, destBase, directory,  count=defaultFileNum):
	destDir = os.listdir(destBase + directory)
	filesShort = count - len(destDir)
	print("Need " + str(filesShort) + " files for " + directory)
	files = [ x for x in os.listdir(sourceBase + directory) if not x.startswith('.') ]
	files.sort()
	for i in range(0, filesShort):
		if i < len(files):
			source = sourceBase + directory + files[i]
			dest = destBase + directory + str(datePrefix) + "_" + files[i]
			print(source + "  ->  " + dest)
			move(source, dest)

print("=== starting downloadPodcasts.py ===")
print("=== started at " + str(datetime.datetime.now()) + " ===")

baseSource = "/mnt/share/Podcasts/"
baseSync = "/home/kdc/Public/Sync/podcasts/"

datePrefix = datetime.date.today();
sourceDirs = [	["Added_First"],
								["Added_Second"],
								["News/Tech Talk Today/"],

								["Gaming/Convert to Raid/"],
								["Gaming/Convert to Raid Old/"],
								["Gaming/Tauren Think Tank/"],
								["Gaming/Tauren Think Tank Old/"],
								
								["Linux/Linux Action Show/"],
								["Linux/Linux Unplugged/"],
								
								["Programming/Coder Radio/"],
								["Programming/HanselMinutes/"],
								["Programming/Herding Code/"],
								["Programming/Java Posse/"],
								["Programming/Java Posse Old/"],
								["Programming/Software Engineering Radio/"],

								["Politics/AVFM Radio/"],
								["Politics/JB Unfilter/"],
								["Politics/Honey Badger Radio/"],
								["Politics/Law Talk/"],
								["Politics/The Libertarian - Richard Epstein/"],
								["Politics/The Libertarian - Richard Epstein Old/"],
								["Politics/The Ricochet Podcast/"],
								["Politics/The Ricochet Podcast Old/"],
								["Politics/Serial/"],

								["Religion/One Peter Five/"]
							]

call("podget")

for tup in sourceDirs:
	if len(tup) == 2:
		movePodcasts(baseSource, baseSync, tup[0], count=tup[1])
	else:
		movePodcasts(baseSource, baseSync, tup[0])
		

print("=== finished at " + str(datetime.datetime.now()) + " ===")



