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

def removeCurrent(playlist, currentlyPlaying, keepFirstLine=True):
	nowPlaying = playlist[0] if (keepFirstLine and len(playlist) > 0) else ""
	filesToRemove = [x for x in currentlyPlaying if x != nowPlaying ]
	for f in filesToRemove:
		if f in playlist:
			playlist.remove(f)
	return playlist


def writePlaylistFile(baseDir, fileName, oldLines, newLines, debug=False):
	playlistFilename = baseSync + fileName	
	
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
		if(debug):
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

def getLinesFromFile(filename):
	lines = []
	if(os.path.exists(filename)):
		playlistFile = open(filename, "r")
		lines = [x for x in playlistFile.readlines() if not x.startswith('#')]
		playlistFile.close()
	return lines

###########################################################

print("=== starting syncPlaylists.py  ===")
print("=== started at " + str(datetime.datetime.now()) + " ===")
		
baseSync = "/home/kdc/Public/sync/podcasts/"

commutePlaylistName = baseSync + "commute.m3u"
workoutPlaylistName = baseSync + "workout.m3u"
shortPlaylistName = baseSync + "short.m3u"

oldCommuteList = getLinesFromFile(commutePlaylistName)
oldWorkoutList = getLinesFromFile(workoutPlaylistName)
oldShortList = getLinesFromFile(shortPlaylistName)

#####

header = mixPodcasts(baseSync, ["News/Tech Talk Today", "News/CBS_World_News_Roundup", "News/CBS_Weekend_Roundup"]) + \
				 getPodcastsFromDir(baseSync, "Added", limit=1) + \
				 getPodcastsFromDir(baseSync, "Politics/Serial")

commuteOther = mixPodcasts(baseSync, ["Linux/Linux Action Show", "Linux/Linux Unplugged", "Sci_Tech/Omega Tau", "Sci_Tech/Freakonomics_Radio"])
commuteProgramming = mixPodcasts(baseSync, ["Programming/Java Posse", "Programming/Software Engineering Radio",
			"Programming/HanselMinutes", "Programming/Coder Radio", "Programming/Herding Code",
			"Sci_Tech/Omega Tau Old", "Sci_Tech/Freakonomics_Radio Old"])

commuteOld = mixPodcasts(baseSync, ["Programming/Coder Radio Old", "Programming/HanselMinutes Old",
					"Programming/Herding Code Old", "Programming/Java Posse Old", "Sci_Tech/Omega Tau"])

workoutNew = mixPodcasts(baseSync, ["Politics/Honey Badger Radio", "Politics/The Ricochet Podcast", 
				"Politics/The Libertarian - Richard Epstein",# "Sci_Tech/Omega Tau", "Sci_Tech/Freakonomics_Radio",
				"Politics/Law Talk", "Fitness/Get up and Code", "Religion/Catholic_Underground", "Religion/Word_On_Fire_Sermon"])

workoutOld = mixPodcasts(baseSync, ["Politics/AVFM Radio", "Politics/Law Talk Old",
					"Politics/The Ricochet Podcast Old", "Sci_Tech/Omega Tau Old", "Sci_Tech/Freakonomics_Radio Old", 
					"Fitness/Get up and Code Old", "Politics/Honey Badger Radio Old", "Religion/Word_On_Fire_Sermon Old"])

newCommuteList = generatePlaylist(
		[
			header,
			getPodcastsFromDir(baseSync, "Added",offset=1),
			commuteProgramming,
			commuteOther,
			workoutNew[0:3],
			commuteOld ], oldCommuteList, [])

newWorkoutList = generatePlaylist(
		[
			header,
			getPodcastsFromDir(baseSync, "Added", offset=1),
			workoutNew,
			commuteOther,
			workoutOld ], oldWorkoutList, [])

currentlyPlaying = [newCommuteList[0], newWorkoutList[0]]

newCommuteList = removeCurrent(newCommuteList, currentlyPlaying)
newWorkoutList = removeCurrent(newWorkoutList, currentlyPlaying)

shortList = generatePlaylist([
	mixPodcasts(baseSync, ["News/Tech Talk Today", "News/CBS_World_News_Roundup", "Politics/The Libertarian - Richard Epstein",
			"Religion/Word_On_Fire_Sermon", "Sci_Tech/Freakonomics_Radio"]),
	mixPodcasts(baseSync, ["Politics/The Libertarian - Richard Epstein Old", "Religion/Word_On_Fire_Sermon Old",
			"Sci_Tech/Freakonomics_Radio Old"])
	], oldShortList, currentlyPlaying)

writePlaylistFile(baseSync, "commute.m3u", oldCommuteList, newCommuteList) 
writePlaylistFile(baseSync, "workout.m3u", oldWorkoutList, newWorkoutList) 
writePlaylistFile(baseSync, "short.m3u", oldShortList, shortList)

writePlaylistFile(baseSync, "all.m3u", getLinesFromFile(baseSync + "all.m3u"),
	removeCurrent(mixPodcasts(baseSync, [
				"Added",
				
				"Fitness/Get up and Code",
				"Fitness/Get up and Code Old",

				"Linux/Linux Action Show",
				"Linux/Linux Unplugged",
				
				"News/Tech Talk Today",
				"News/CBS_Weekend_Roundup",
				"News/CBS_World_News_Roundup",
				
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

				"Religion/Catholic_Underground",
				"Religion/Word_On_Fire_Sermon",
				"Religion/Word_On_Fire_Sermon Old",
				
				"Sci_Tech/Omega Tau",
				"Sci_Tech/Omega Tau Old",
				"Sci_Tech/Freakonomics_Radio",
				"Sci_Tech/Freakonomics_Radio Old"
				
			], maxSequence=0), currentlyPlaying)
		)
writePlaylistFile(baseSync, "z0_current.m3u", getLinesFromFile(baseSync + "z0_current.m3u"), currentlyPlaying)
writePlaylistFile(baseSync, "z0_header.m3u", getLinesFromFile(baseSync + "z0_header.m3u"), removeCurrent(header, currentlyPlaying, keepFirstLine=False))

writePlaylistFile(baseSync, "z_commute_programming.m3u", getLinesFromFile(baseSync + "z_commute_programming.m3u"),
		removeCurrent(commuteProgramming, currentlyPlaying, keepFirstLine=False))
writePlaylistFile(baseSync, "z_commute_other.m3u", getLinesFromFile(baseSync + "z_commute_other.m3u"),
		removeCurrent(commuteOther, currentlyPlaying,  keepFirstLine=False))
writePlaylistFile(baseSync, "z_commute_old.m3u", getLinesFromFile(baseSync + "z_commute_old.m3u"),
		removeCurrent(commuteOld, currentlyPlaying,  keepFirstLine=False))

writePlaylistFile(baseSync, "z_workout_new.m3u", getLinesFromFile(baseSync + "z_workout_new.m3u"),
		removeCurrent(workoutNew, currentlyPlaying, keepFirstLine=False))
writePlaylistFile(baseSync, "z_workout_old.m3u", getLinesFromFile(baseSync + "z_workout_old.m3u"),
		removeCurrent(workoutOld, currentlyPlaying, keepFirstLine=False))


print("=== finished at " + str(datetime.datetime.now()) + " ===\n\n")
