import cv2
import ast
import numpy as np

def onSegment(p,q,r):
    if (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1])):
        return True
    return False

def orientation(p,q,r):
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if val > 0:
        return 1
    elif val < 0:
        return 2
    else:
        return 0

def doIntersect(p1,q1,p2,q2):
    o1 = orientation(p1,q1,p2)
    o2 = orientation(p1,q1,q2)
    o3 = orientation(p2,q2,p1)
    o4 = orientation(p2,q2,q1)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and onSegment(p1,p2,q1):
        return True
    if o2 == 0 and onSegment(p1,q2,q1):
        return True
    if o3 == 0 and onSegment(p2,p1,q2):
        return True
    if o4 == 0 and onSegment(p2,q1,q2):
        return True
    return False

def count_intersections(polyline, count_polyline):
    count = 0
    o_count = 0
    d_count = 0
    for i in range(len(polyline) - 1):
        p1 = polyline[i]
        q1 = polyline[i + 1]
        for j in range(len(count_polyline) - 1):
            p2 = count_polyline[j]
            q2 = count_polyline[j + 1]
            if doIntersect(p1,q1,p2,q2):
                count += 1
                #print(f'The polyline starts at {p1} and ends at {q1}')
                #print(f'The count polyline starts at {p2} and ends at {q2}')
                vec1 = np.array(q2)-np.array(p2)
                vec2 = np.array(q1)-np.array(p1)
                cross_product = np.cross(vec1,vec2)
                if cross_product > 0:
                    o_count += 1
                elif cross_product < 0:
                    d_count += 1
                else:
                    continue

                #with open('intersection_poly.txt', 'a') as f:
                #    f.write("%s\n"% [p1,q1,p2,q2])
                #f.close()
    return count,o_count,d_count

#counting lines for 300x300 image 01
c1 = [(1,115),(60,66)] #Exit of Ringier Building
c2 = [(66,66),(111,68)] #Bridge Pedestrian path left
c3 = [(226,59),(264,57)] #Bridge Pedestrian path right
c4 = [(220,217),(227,259)] # Pedestrian crossing
c5 = [(80,264),(0,252)] #Bottom left counting line
count_polylines = [[c1],[c2],[c3],[c4],[c5]] 

#counting lines for 300x300 image 02
c1_2 = [(1,115),(58,54)] #Exit of Ringier Building
c2_2 = [(74,57),(113,59)] #Bridge Pedestrian path left
c3_2 = [(234,66),(281,63)] #Bridge Pedestrian path right
c4_2 = [(254,212),(257,258)] #Pedestrian crossing
c5_2 = [(86,258),(1,261)] #Bottom left counting line
count_polylines2 = [[c1_2],[c2_2],[c3_2],[c4_2],[c5_2]] 

#counting lines for 300x300 image 03
c1_3 = [(3,96),(97,32)] #Exit of Ringier Building
c2_3 = [(115,28),(167,66)] #Bridge Pedestrian path left
c3_3 = [(252,230),(254,297)] #Pedestrian crossing
c4_3 = [(128,273),(0,240)]  #Bottom left counting line
count_polylines3 = [[c1_3],[c2_3],[c3_3],[c4_3]] 

#counting lines for 300x300 image 04
c1_4 = [(25,81),(113,22)] #Exit of Ringier Building
c2_4 = [(127,20),(175,43)] #Bridge Pedestrian path left
c3_4 = [(251,217),(258,280)] #Pedestrian crossing
c4_4 = [(132,266),(1,264)] #Bottom left counting line
count_polylines4 = [[c1_4],[c2_4],[c3_4],[c4_4]] 


#Extract tracks from txt file output of SORT
tracks = []
with open('tracks.txt') as f:
    for l in f:
        v = list(ast.literal_eval(l))
        frame_id, x1, y1, x2, y2, track_id = v
        x_pos = x1 + ((x2-x1)/2)
        y_pos = y1+((y2-y1)/2)
        cbot = (x_pos, y_pos)
        tracks.append([frame_id, x1, y1, x2, y2, track_id,cbot])
    f.close()

#Get all unique track_ids
unique_trackids = set(entry[5] for entry in tracks)

#Aggregate all cbot points by track ids
polylines =[]
for utrack in unique_trackids:
    polyline = []
    for track in tracks:
        if utrack == track[5]:
            polyline.append(track[6])
    polylines.append(polyline)

#intersection_counts = open('intersection_counts.txt', 'x')
#intersection_counts.close()
od_counts = open('od_counts.txt', 'x')
od_counts.close()

intersecting_polylines = []
for i, count_polyline in enumerate(count_polylines4):
    origin = 0
    destination = 0
    for j, polyline in enumerate(polylines):
        intersections, origin_count, destination_count = count_intersections(polyline, count_polyline[0])
        if intersections != 0:
            #print(f'Polyline {j + 1} intersects with the count polyline number {i + 1} : {intersections} times')
            #print(f'Count polyline {count_polyline[0]},Polyline {polyline}')
            intersecting_polylines.append(polyline)
        origin += origin_count
        destination += destination_count
        #with open('intersection_counts.txt', 'a') as f:
        #    f.write("%s\n"% [i,j,intersections,origin_count, destination_count])
        #f.close()
        #print(f"Count Polyline {i + 1} and Polyline {j + 1}: {intersections} intersections")
    with open('od_counts.txt', 'a') as ff:
        ff.write("%s\n"% [i, origin, destination])