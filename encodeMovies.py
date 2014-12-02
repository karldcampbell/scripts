#!/usr/bin/python
#HandBrakeCLI -i <filename> -o <filename>.mp4 --preset="Android Tablet" -N eng --subtitle-burned

import os
import sys
from subprocess import call


def doEncode(srcFileName, destFileName):
	tmp = os.popen("mediainfo " + srcFileName).read()
	arr = tmp.split("\n\n")
	
	audioTrack=1
	subtitleTrack = 1

	for line in arr:
		if(line.startswith("Text") and "English" in line):
			subtitleTrackStr = line.split('\n')[0]
			if("Text #" in subtitleTrackStr):
				subtitleTrack = subtitleTrackStr.replace("Text #", "").strip()

	for line in arr:
		if(line.startswith("Audio") and "English" in line):
			audioTrackStr = line.split('\n')[0]
			if("Audio #" in audioTrackStr):
				audioTrack = audioTrackStr.replace("Audio #", "").strip()

	call(["HandBrakeCLI","-i", infile, "-o", outfile, "--preset=Android Tablet",
		"-a", str(audioTrack), "-N","eng", "-s", str(subtitleTrack), "--subtitle-burned"])

def getFilesInDir(sourceDir):
	sourceFiles = []
	for root, dirs, files in os.walk(sourceDir):
		files = [f for f in files if (not f.startswith('.') and f.endswith('.mkv'))]
		dirs[:] = [d for d in dirs if not d.startswith('.')]

		for f in files:
			sourceFiles.append(root + f)
	return sourceFiles

print(sys.argv)
if(len(sys.argv) != 2):
	print("Usage:  encodeMovies <sourceDir> <destDir>");
	sys.exit(1)

for f in getFilesInDir(sys.argv[1]):
	print(f)
