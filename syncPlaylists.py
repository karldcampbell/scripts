#!/usr/bin/python3
import os
import sys
import datetime

def areEqual(listA, listB):
	if len(listA) != len(listB):
		return False

	for i in range(0, len(listA)):
		if listA[i] != listB[i]:
			return False

	return True

def podKey(obj):
	l = obj.split('\\')
	
	return(l[len(l)-1])

def podcastName(obj):
	return obj.split('\\')[1]

def getFileList(baseDir, dirList):
	fileList = []
	for folder in dirList:
		folderPath = baseDir + folder
		filesToPlay = os.listdir(folderPath)
		filesToPlay.sort()
		for podcast in filesToPlay:
			if not podcast.startswith('.'):
				newCast = folder + "\\" + podcast + "\n"
				fileList.append(newCast)

	return(fileList)

def generatePlaylist(listOfNewLines, oldList):
	playlist = []
	for l in listOfNewLines:
		for i in l:
			playlist.append(i)

	lastPlayedFile = oldList[0] if len(oldList) > 0 else ""
	if lastPlayedFile in playlist:
		playlist.remove(lastPlayedFile)
		playlist = [lastPlayedFile] + playlist

	return playlist
	
def generatePlaylistFile(baseDir, fileName, listOfLines):
	playlistFilename = baseSync + fileName
	playlistFile = open(playlistFilename, "r")
	oldLines = [x for x in playlistFile.readlines() if not x.startswith('#')]
	playlistFile.close()

	newLines = generatePlaylist(listOfLines, oldLines)
	#print(oldLines)
	#print(newLines)
	
	if not areEqual(newLines, oldLines):
		print("playlist " + fileName + " has changed")
		playlistFile = open(playlistFilename, "w")
		for l in newLines:
			#print(l)
			playlistFile.write(l)
		playlistFile.close()
	else:
		print("no change in " + fileName)

def indexOfNextDifferentShow(podList, nameOfLastShow):
	index = 0;
	for i in range(0, len(podList)):
		if podcastName(podList[i]) != nameOfLastShow:
			index = i;
			break

	return index

def mixPodcasts(baseDir, dirList, maxSequence=2):
	podList = []

	for podDir in dirList:
		for x in getPodcastsFromDir(baseDir, podDir):
			podList.append(x)
	#tupList = [ x.split('\\') for x in podList ]
	podList = sorted(podList, key=podKey)

	if maxSequence > 0:
		#do some mixing..
		podListNew = []
		lastPodcastName = ""
		numInCurrentSequence = maxSequence - 1
		while(len(podList) > 0):

			index = 0 if maxSequence > numInCurrentSequence else indexOfNextDifferentShow(podList, lastPodcastName)
			numInCurrentSequence = numInCurrentSequence +1 if index == 0 else 0
			lastPodcastName = podcastName(podList[index])
			podListNew.append(podList.pop(index))
		podList = podListNew

	return podList


def getPodcastsFromDir(baseDir, directory, limit=0, offset=0):
	podcasts = [x for x in os.listdir(baseDir + directory) if not x.startswith('.')]
	podcasts.sort()
	num = limit if limit > 0 else len(podcasts)
	return [directory.replace("/", "\\") + "\\" +x+ '\n' for x in podcasts[offset:num]]

###########################################################

print("=== starting syncPlaylists.py  ===")
print("=== started at " + str(datetime.datetime.now()) + " ===")
		
baseSync = "/home/kdc/btsync/syncDir/Sync/podcasts/"

commutePlaylistName = baseSync + "commute.m3u"
workoutPlaylistName = baseSync + "workout.m3u"

header = getPodcastsFromDir(baseSync, "News/Tech Talk Today") + \
				 getPodcastsFromDir(baseSync, "Added_First", limit=1) + \
				 getPodcastsFromDir(baseSync, "Politics/Serial")


generatePlaylistFile(baseSync, "commute.m3u", 
		[ 
			header,
			mixPodcasts(baseSync, ["Linux/Linux Action Show", "Linux/Linux Unplugged",
					"Programming/Java Posse", "Programming/Software Engineering Radio"]),
			getPodcastsFromDir(baseSync, "Added_Second"),
			mixPodcasts(baseSync, ["Programming/Coder Radio", "Programming/HanselMinutes",
					"Programming/Herding Code", "Programming/Java Posse Old", "Religion/One Peter Five"])
		])

generatePlaylistFile(baseSync, "workout.m3u",
		[ 
			header,
			mixPodcasts(baseSync, ["Politics/Honey Badger Radio", "Politics/The Ricochet Podcast", 
				"Politics/The Libertarian - Richard Epstein", "Religion/One Peter Five",
				"Politics/Law Talk"]),
			getPodcastsFromDir(baseSync, "Added_Second"),
			mixPodcasts(baseSync, ["Linux/Linux Action Show", "Linux/Linux Unplugged"]),
			mixPodcasts(baseSync, ["Politics/JB Unfilter", "Politics/AVFM Radio",
					"Politics/The Ricochet Podcast Old"])
		])


generatePlaylistFile(baseSync, "gaming.m3u",
		[
			header,
			mixPodcasts(baseSync, ["Gaming/Convert to Raid", "Gaming/Tauren Think Tank"]),
			mixPodcasts(baseSync, ["Politics/Honey Badger Radio", "Politics/The Ricochet Podcast", 
				"Politics/The Libertarian - Richard Epstein", "Linux/Linux Action Show", "Linux/Linux Unplugged",
				"Politics/Law Talk", "Religion/One Peter Five"]),
			mixPodcasts(baseSync, ["Gaming/Convert to Raid Old", "Gaming/Tauren Think Tank Old"]),
		])

generatePlaylistFile(baseSync, "all.m3u",
		[ mixPodcasts(baseSync, [
				"Added_First",
				"Added_Second", 
				"News/Tech Talk Today",
				"Linux/Linux Action Show",
				"Linux/Linux Unplugged",
				"Programming/Coder Radio",
				"Programming/HanselMinutes",
				"Programming/Herding Code",
				"Programming/Java Posse",
				"Programming/Java Posse Old",
				"Programming/Software Engineering Radio",
				"Politics/AVFM Radio",
				"Politics/JB Unfilter",
				"Politics/Honey Badger Radio",
				"Politics/Law Talk",
				"Politics/The Libertarian - Richard Epstein",
				"Politics/The Ricochet Podcast",
				"Politics/The Ricochet Podcast Old",
				"Politics/Serial",
				"Gaming/Convert to Raid",
				"Gaming/Convert to Raid Old",
				"Religion/One Peter Five"
			], maxSequence=0)
		])

print("=== finished at " + str(datetime.datetime.now()) + " ===\n\n")
