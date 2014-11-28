#!/usr/bin/python
#HandBrakeCLI -i <filename> -o <filename>.mp4 --preset="Android Tablet" -N eng --subtitle-burned

import os
from subprocess import call


audioTrack=1
subtitleTrack = 1

inputDir = "/home/kdc/tmp/"
outputDir = "/home/kdc/tmp/"
fileName= "Gilmore Girls - S01e04 - The Deer-Hunters"

#fileName = fileName.replace(" ", "\ ");

infile =  inputDir+fileName+".mkv"
outfile = outputDir + fileName + ".mp4"

#command = "HandBrakeCLI -i {0} -o {1} --preset=\"Android\"".format(infile, outfile)
#print(command)
#commandArr = ["HandBrakeCLI", "-i", infile, "-o", outfile, "--preset=Android Tablet"]
#call(commandArr)

tmp = os.popen("mediainfo ~/tmp/Gilmore\ Girls\ -\ S01e04\ -\ The\ Deer-Hunters.mkv Gilmore\ Girls\ -\ S01e04\ -\ The\ Deer-Hunters.mkv").read()
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



#call(["HandBrakeCLI","-i", inputDir+fileName+".mkv", "-o", outputDir + fileName + ".mp4"])

call(["HandBrakeCLI","-i", infile, "-o", outfile, "--preset=Android Tablet",
	"-a", str(audioTrack), "-N","eng", "-s", str(subtitleTrack), "--subtitle-burned"])
