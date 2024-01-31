import matplotlib.pyplot as plt 
import ast
from datetime import datetime
from collections import defaultdict
import numpy as np

detections = []
with open('detection_outputs.txt') as f:
    for l in f:
        v = ast.literal_eval(l)
        score, x1, y1, x2, y2, frame_id,class_id,date,hour  = v
        if class_id == 0: 
            detections.append([x1, y1, x2, y2, score,frame_id])

# Extract frame_ids from detections
frame_ids = [detection[-1] for detection in detections]
max_frame = 112943
video_minutes = 359.25 #359.48
# Set the interval for the histogram (every 27,000 frames)
interval = int(max_frame*15/video_minutes)


plt.figure(figsize=(12, 6)) 
# Calculate the number of detections in each interval
hist_values, bin_edges, _ = plt.hist(frame_ids, bins=range(0, max(frame_ids) + interval, interval), color='skyblue')
labels = range(0,25)

bin_edges = np.concatenate([bin_edges[:-1], [bin_edges[-1]]])  # Make bin_edges have 24 elements
hist_values = np.concatenate([hist_values, [0]])  # Pad hist_values with 0 to have 24 elements
# Set labels and title
plt.ylabel('Number of Detections')
plt.title('Histogram of Detections Every 15 minutes')
plt.xticks(bin_edges, labels)
plt.savefig('chart.png')
plt.show()

