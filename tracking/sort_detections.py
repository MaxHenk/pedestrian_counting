from sort.sort import *
import ast
import sys


start_time = time.time()
tracker = Sort(max_age=60, min_hits=3, iou_threshold=0.3)

with open('detection_outputs.txt') as f:
    current_frame_id = -1
    detections = []
    for l in f:
        # Agréger les frames
        # [[x1,y1,x2,y2,score], [....]]
        v = ast.literal_eval(l)
        score, x1, y1, x2, y2, frame_id,class_id  = v[:7]
        if class_id == 0: #change class_id == : the class of interest
            if frame_id != current_frame_id: 
                matches = tracker.update(np.array(detections))
                with open('tracks.txt', 'a') as fout:
                    for match in matches:
                        fout.write('{}, {}\n'.format(current_frame_id, ', '.join(map(str, match))))
                current_frame_id = frame_id
                detections = []
        
            detections.append([x1, y1, x2, y2, score])
        else:
            continue
    matches = tracker.update(np.array(detections))
    with open('tracks.txt', 'a') as fout:
        for match in matches:
            fout.write('{}, {}\n'.format(current_frame_id, ', '.join(map(str, match))))
end_time = time.time()
# Calcul de la duree totale
total_time_seconds = end_time - start_time
print(f'Le temps d execution est de {total_time_seconds} secondes')