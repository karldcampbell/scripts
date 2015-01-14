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

def generatePlaylist(listOfNewLines, oldList, currentlyPlaying, keepFirstLine=True):
	playlist = []
	for l in listOfNewLines:
		for i in l:
			playlist.append(i)

	lastPlayedFile = oldList[0] if keepFirstLine and len(oldList) > 0 else ""
	if lastPlayedFile in playlist:
		playlist.remove(lastPlayedFile)
		playlist = [lastPlayedFile] + playlist

	filesToRemove = [x for x in currentlyPlaying if x != lastPlayedFile ]
	for f in filesToRemove:
		if f in playlist:
			playlist.remove(f)

	return playlist
	
def generatePlaylistFile(baseDir, fileName, currentlyPlaying, listOfLines, keepFirstLine=True, debug=False):
	playlistFilename = baseSync + fileName	
	oldLines = []
	
	if(os.path.exists(playlistFilename)):
		playlistFile = open(playlistFilename, "r")
		oldLines = [x for x in playlistFile.readlines() if not x.startswith('#')]
		playlistFile.close()

	newLines = generatePlaylist(listOfLines, oldLines, currentlyPlaying, keepFirstLine)
	
	if(len(newLines) == 0 and os.path.exists(playlistFilename)):
		print("no audio files for " + fileName + ". Deleting playlist.")		
		os.remove(playlistFilename)
		return

	if(debug):
		print(oldLines)
		print(newLines)
	
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

def getCurrentlyPlaying(baseDir, fileList):
	playingList = []
	for f in fileList:
		try:
			infile = open(baseDir + f, 'r')
			oldLines = [x for x in infile.readlines() if not x.startswith('#')]
			playing = oldLines[0]
			playingList.append(playing)
		except IOError:
			print("Error opening file: " + f)
	return(playingList)
###########################################################

print("=== starting syncPlaylists.py  ===")
print("=== started at " + str(datetime.datetime.now()) + " ===")
		
baseSync = "/home/kdc/Public/sync/podcasts/"

commutePlaylistName = baseSync + "commute.m3u"
workoutPlaylistName = baseSync + "workout.m3u"

#####
currentlyPlaying = getCurrentlyPlaying(baseSync, ["commute.m3u", "workout.m3u"])

header = getPodcastsFromDir(baseSync, "News/Tech Talk Today") + \
				 getPodcastsFromDir(baseSync, "Added", limit=1) + \
				 getPodcastsFromDir(baseSync, "Politics/Serial")

commuteLinux = mixPodcasts(baseSync, ["Linux/Linux Action Show", "Linux/Linux Unplugged"])
commuteProgramming = mixPodcasts(baseSync, ["Programming/Java Posse", "Programming/Software Engineering Radio",
			"Programming/HanselMinutes", "Programming/Coder Radio", "Programming/Herding Code"])

commuteOld = mixPodcasts(baseSync, ["Programming/Coder Radio Old", "Programming/HanselMinutes Old",
					"Programming/Herding Code Old", "Programming/Java Posse Old", "Tech/Omega Tau"])
tmp = []


generatePlaylistFile(baseSync, "commute.m3u", currentlyPlaying,
		[ 
			header,
			getPodcastsFromDir(baseSync, "Added",offset=1),
			commuteProgramming,
			commuteLinux,
			commuteOld
		])

#####

workoutNew = mixPodcasts(baseSync, ["Politics/Honey Badger Radio", "Politics/The Ricochet Podcast", 
				"Politics/The Libertarian - Richard Epstein", "Religion/One Peter Five",
				"Politics/Law Talk", "Fitness/Get up and Code"])

workoutOld = mixPodcasts(baseSync, ["Politics/AVFM Radio", "Politics/Law Talk Old",
					"Politics/The Ricochet Podcast Old", "Tech/Omega Tau", "Fitness/Get up and Code Old",
					"Politics/Honey Badger Radio Old"])


generatePlaylistFile(baseSync, "workout.m3u", currentlyPlaying,
		[ 
			header,
			getPodcastsFromDir(baseSync, "Added", offset=1),
			workoutNew,
			commuteLinux,
			workoutOld
		])

####

gamingNew = []# mixPodcasts(baseSync, ["Gaming/Convert to Raid", "Gaming/Tauren Think Tank"]) 
gamingOld = [] # mixPodcasts(baseSync, ["Gaming/Convert to Raid Old", "Gaming/Tauren Think Tank Old","Tech/Omega Tau"])

#generatePlaylistFile(baseSync, "gaming.m3u", currentlyPlaying,
#		[
#			header,
#			gamingNew,
#			workoutNew,
#			commuteLinux,
#			gamingOld
#		])

#####

generatePlaylistFile(baseSync, "all.m3u", currentlyPlaying,
		[ mixPodcasts(baseSync, [
				"Added",
				
				"Fitness/Get up and Code",
				"Fitness/Get up and Code Old",

				"Linux/Linux Action Show",
				"Linux/Linux Unplugged",
				
				"News/Tech Talk Today",
				
				"Politics/AVFM Radio",
				"Politics/Honey Badger Radio",
				"Politics/Honey Badger Radio Old",
				"Politics/Law Talk",
				"Politics/Law Talk Old",
				"Politics/Serial",
				"Politics/The Libertarian - Richard Epstein",
				"Politics/The Libertarian - Richard Epstein Old",
				"Politics/The Ricochet Podcast",
				"Politics/The Ricochet Podcast Old",
				
				"Programming/Coder Radio",
				"Programming/Coder Radio Old",
				"Programming/HanselMinutes",
				"Programming/HanselMinutes Old",
				"Programming/Herding Code",
				"Programming/Herding Code Old",
				"Programming/Java Posse",
				"Programming/Java Posse Old",
				"Programming/Software Engineering Radio",
				
				"Religion/One Peter Five",
				
				"Tech/Omega Tau",
				
			], maxSequence=0)
		])
generatePlaylistFile(baseSync, "z0_current.m3u", [], [currentlyPlaying], keepFirstLine=False)
generatePlaylistFile(baseSync, "z0_header.m3u", currentlyPlaying, [header], keepFirstLine=False)
generatePlaylistFile(baseSync, "z_commute_programming.m3u", currentlyPlaying, [commuteProgramming], keepFirstLine=False)
generatePlaylistFile(baseSync, "z_commute_linux.m3u", currentlyPlaying, [commuteLinux], keepFirstLine=False)
generatePlaylistFile(baseSync, "z_commute_old.m3u", currentlyPlaying, [commuteOld], keepFirstLine=False)

generatePlaylistFile(baseSync, "z_workout_new.m3u", currentlyPlaying, [workoutNew], keepFirstLine=False)
generatePlaylistFile(baseSync, "z_workout_old.m3u", currentlyPlaying, [workoutOld], keepFirstLine=False)

#generatePlaylistFile(baseSync, "z_gaming_new.m3u", currentlyPlaying, [gamingNew], keepFirstLine=False)
#generatePlaylistFile(baseSync, "z_gaming_old.m3u", currentlyPlaying, [gamingOld], keepFirstLine=False)

print("=== finished at " + str(datetime.datetime.now()) + " ===\n\n")
