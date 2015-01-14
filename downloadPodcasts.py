#!/usr/bin/python3

import os
import sys
import datetime
import random
from shutil import move
from subprocess import call

def movePodcasts(sourceBase, destBase, directory,  count=3):
	destDir = os.listdir(destBase + directory)
	filesShort = count - len(destDir)
	#if filesShort > 0:
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

skipDownload = False
if(len(sys.argv) > 1):
	if(sys.argv[1] == "--skipDownload"):
		skipDownload = True

defaultFileNum = 3

baseSource = "/mnt/share/Podcasts/"
baseSync = "/home/kdc/Public/sync/podcasts/"

datePrefix = datetime.date.today();

if(not skipDownload):
	call("podget")
else:
	print("Skiping download...")

movePodcasts(baseSource, baseSync, "Added/")
movePodcasts(baseSource, baseSync, "News/Tech Talk Today/")

movePodcasts(baseSource, baseSync, "Tech/Omega Tau/")

movePodcasts(baseSource, baseSync, "Linux/Linux Action Show/")
movePodcasts(baseSource, baseSync, "Linux/Linux Unplugged/")

movePodcasts(baseSource, baseSync, "Programming/Coder Radio/")
movePodcasts(baseSource, baseSync, "Programming/HanselMinutes/")
movePodcasts(baseSource, baseSync, "Programming/Herding Code/")
movePodcasts(baseSource, baseSync, "Programming/Java Posse/")
movePodcasts(baseSource, baseSync, "Programming/Java Posse Old/")
movePodcasts(baseSource, baseSync, "Programming/Software Engineering Radio/")

movePodcasts(baseSource, baseSync, "Politics/AVFM Radio/")
movePodcasts(baseSource, baseSync, "Politics/JB Unfilter/")
movePodcasts(baseSource, baseSync, "Politics/Honey Badger Radio/")
movePodcasts(baseSource, baseSync, "Politics/Law Talk/")
movePodcasts(baseSource, baseSync, "Politics/The Libertarian - Richard Epstein/")
movePodcasts(baseSource, baseSync, "Politics/The Libertarian - Richard Epstein Old/")
movePodcasts(baseSource, baseSync, "Politics/The Ricochet Podcast/")
movePodcasts(baseSource, baseSync, "Politics/The Ricochet Podcast Old/")
#movePodcasts(baseSource, baseSync, "Politics/Serial/")

movePodcasts(baseSource, baseSync, "Religion/One Peter Five/")
movePodcasts(baseSource, baseSync, "Fitness/Get up and Code/")

print("=== finished at " + str(datetime.datetime.now()) + " ===")



