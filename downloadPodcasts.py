#!/usr/bin/python3

import os
import sys
import datetime
import random
from shutil import move
from subprocess import call

def movePodcasts(sourceBase, destBase, directory,  count=3, oldEpisodes=False):
	destDir = os.listdir(destBase + directory)
	filesShort = count - len(destDir)
	filesInDest = len(destDir)
	#if filesShort > 0:
	print("Need " + str(filesShort) + " files for " + directory)
	files = [ x for x in os.listdir(sourceBase + directory) if not x.startswith('.') ]
	files.sort()
	for i in range(0, filesShort):
		if i < len(files):
			filesInDest += 1
			source = sourceBase + directory + "/" + files[i]
			dest = destBase + directory + "/" + str(datePrefix) + "_" + files[i]
			print(source + "  ->  " + dest)
			move(source, dest)

	if(oldEpisodes):
		newEpisodes = os.listdir(sourceBase + directory)
		if(len(newEpisodes) > count * 3):
			filesToMove = len(newEpisodes) - count
			print("Files to move to old: " + str(filesToMove))
			for i in range(0, filesToMove):
				source = sourceBase + directory + "/" + files[i]
				dest = sourceBase + directory + " Old/" + files[i]
				try:
					move(source, dest)
					print("  " + source + "  ->  " + dest)
				except:
					print("error moving file " + source)
		movePodcasts(sourceBase, destBase, directory + " Old", count=count-filesInDest)

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

movePodcasts(baseSource, baseSync, "Added")
movePodcasts(baseSource, baseSync, "News/Tech Talk Today")

movePodcasts(baseSource, baseSync, "Tech/Omega Tau")

movePodcasts(baseSource, baseSync, "Linux/Linux Action Show")
movePodcasts(baseSource, baseSync, "Linux/Linux Unplugged")

movePodcasts(baseSource, baseSync, "Programming/Coder Radio", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Programming/HanselMinutes", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Programming/Herding Code", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Programming/Java Posse", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Programming/Software Engineering Radio")

movePodcasts(baseSource, baseSync, "Politics/AVFM Radio")
movePodcasts(baseSource, baseSync, "Politics/Honey Badger Radio", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Politics/Law Talk", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Politics/The Libertarian - Richard Epstein", oldEpisodes=True)
movePodcasts(baseSource, baseSync, "Politics/The Ricochet Podcast", oldEpisodes=True)
#movePodcasts(baseSource, baseSync, "Politics/JB Unfilter")
#movePodcasts(baseSource, baseSync, "Politics/Serial/")

movePodcasts(baseSource, baseSync, "Fitness/Get up and Code", oldEpisodes=True)

print("=== finished at " + str(datetime.datetime.now()) + " ===")



