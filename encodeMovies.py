#!/usr/bin/python
#HandBrakeCLI -i <filename> -o <filename>.mp4 --preset="Android Tablet" -N eng --subtitle-burned

import os
from subprocess import call

tmp = os.popen("mediainfo ~/tmp/Gilmore\ Girls\ -\ S01e04\ -\ The\ Deer-Hunters.mkv Gilmore\ Girls\ -\ S01e04\ -\ The\ Deer-Hunters.mkv").read()

audioTrack=1
subtitleTrack = 1


arr = tmp.split("\n\n")
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

print(audioTrack)
print(subtitleTrack)

inputDir = "/home/kdc/tmp/"
outputDir = "/home/kdc/tmp/"

fileName= "Gilmore Girls - S01e04 - The Deer-Hunters"

call(["HandBrakeCLI","-i", inputDir+fileName+".mkv", "-o", outputDir + fileName + ".mp4","--preset=\"Android Tablet\"",
	"-a " + str(audioTrack), "-N eng", "-s " + str(subtitleTrack), "--subtitle-burned"])
