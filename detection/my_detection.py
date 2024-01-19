#!/usr/bin/python

# Import packages
import jetson.inference
import jetson.utils

import argparse
import sys
from datetime import datetime
from jetson_utils import videoSource, videoOutput

print("Parses input argument to use afterwards")
# Parses input argument to use afterwards
parser = argparse.ArgumentParser(description="Locate objects in an image using an object detection DNN.", 
						   formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage())

parser.add_argument("file_in", type=str, help="filename of the input image to process")
parser.add_argument("file_out", type=str, default=None, nargs='?', help="filename of the output image to save")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load, see below for options") #pednet
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")
parser.add_argument("--profile", type=bool, default=False, help="enable performance profiling and multiple runs of the model")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--runs", type=int, default=15, help="if profiling is enabling, the number of iterations to run")

print("Test to see if required arguments")
# Test to see if required arguments are present : file_in
try:
	opt, argv = parser.parse_known_args()
except:
	print("")
	parser.print_help()
	sys.exit(0)

print("Load pretrained detection model")
# load the object detection network
net = jetson.inference.detectNet(opt.network, argv, opt.threshold)

print("Creating a text file")
# Creating a text file to put the detections on every frame
timestr = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour)
date = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day)
hour = str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

file_text = open("detection_output_" + timestr +".txt", "x")
file_text.close()

camera = videoSource(opt.file_in)
display = videoOutput(opt.file_out)
height = camera.GetHeight()
width = camera.GetWidth()

while True:
	img = camera.Capture()
	if img is None:
		break
	if datetime.now().minute == 0:
		timestr = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour)
		file_text = open("detection_output_"+ timestr +".txt", "x")
		file_text.close()
		detections = net.Detect(img, width, height)

		# print the detections
		#Detection object takes .ClassID .Left .Top .Right .Bottom .Width .Height .Area .Center argument
		print("detected {:d} objects in image".format(len(detections)))
		with open('detection_output_'+ timestr +'.txt', "a") as f:
			for detection in detections:
				print(detection) 
				date = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day)
				hour = str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)
				f.write("%s\n" % [detection.ClassID, detection.Left, detection.Top, detection.Right, detection.Bottom, detection.Area, detection.Center, date, hour])
		f.close()
		# wait for GPU to complete work
		jetson.utils.cudaDeviceSynchronize()

		# print out timing info
		net.PrintProfilerTimes()
	else:
		detections = net.Detect(img, width, height)
		#Detection object takes .ClassID .Left .Top .Right .Bottom .Width .Height .Area .Center argument
		print("detected {:d} objects in image".format(len(detections)))
		with open('detection_output_'+ timestr +'.txt', "a") as f:
			for detection in detections:
				print(detection)
				date = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day)
				hour = str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)
				f.write("%s\n" % [detection.ClassID, detection.Left, detection.Top, detection.Right, detection.Bottom, detection.Area, detection.Center, date, hour])
		f.close()
		# wait for GPU to complete work
		jetson.utils.cudaDeviceSynchronize()

		# print out timing info
		net.PrintProfilerTimes()
	#display.Render(img)
	#display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

