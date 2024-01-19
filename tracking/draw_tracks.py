import cv2
import ast
import numpy as np

#Function to calculate the bottom center coordinate of a bounding box
def calculate_bottom_center(x1,y1,x2,y2):
    x_position = x1+((x2-x1)/2)
    y_position = y1+((y2-y1)/2)
    return [x_position, y_position]

#Function to draw tracking lines based on the tracks coming from SORT
def draw_multiple_polylines(image, polylines, is_closed = False, color = (0,0,255), thickness = 1):
    result_image = image.copy()
    polylines_to_draw = []
    for polyline in polylines:
        polyline_array = np.array(polyline,dtype = np.int32).reshape((-1,1,2))
        polylines_to_draw.append(polyline_array)
        cv2.polylines(result_image, polylines_to_draw, isClosed=is_closed, color=color,thickness=thickness)

    return result_image

image = '04_first_frame.jpg' #Path to background image
img = cv2.imread(image) #Read provided background image

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

#Draw tracks on background image (is a copy)
result_image = draw_multiple_polylines(img, polylines, is_closed=False, color= (0,255,0), thickness=4)

#Set counting lines
#Counting lines for whole image
#c1 = [(643,908),(659,1072)]
#c2 = [(743,643),(686,700)]
#c3 = [(840,616),(886,620)]
#c4 = [(1106,631),(1153,626)]
#c5 = [(1339,898),(1406,949)]
#c6 = [(1381,1036),(1333,1071)]

#counting lines for 300x300 image 01
c1 = [(66,66),(111,68)] #Bridge Pedestrian path left
c2 = [(60,66),(1,115)] #Exit of Ringier Building
c3 = [(264,57),(226,59)] #Bridge Pedestrian path right
c4 = [(220,217),(227,259)] # Pedestrian crossing
c5 = [(80,264),(0,252)] #Bottom right counting line
count_polylines = [[c1],[c2],[c3],[c4],[c5]] 

#counting lines for 300x300 image 02
c1_2 = [(74,57),(113,59)]
c2_2 = [(58,54),(1,115)]
c3_2 = [(281,63),(234,66)]
c4_2 = [(254,212),(257,258)]
c5_2 = [(86,258),(1,261)]
count_polylines2 = [[c1_2],[c2_2],[c3_2],[c4_2],[c5_2]] 

#counting lines for 300x300 image 03
c1_3 = [(115,28),(167,66)]
c2_3 = [(97,32),(3,96)]
c3_3 = [(252,230),(254,297)]
c4_3 = [(128,273),(0,240)]
count_polylines3 = [[c1_3],[c2_3],[c3_3],[c4_3]] 

#counting lines for 300x300 image 04
c1_4 = [(127,20),(175,43)]
c2_4 = [(113,22),(25,81)]
c3_4 = [(251,217),(258,280)]
c4_4 = [(132,266),(1,264)]
count_polylines4 = [[c1_4],[c2_4],[c3_4],[c4_4]] 
result_imagecount = draw_multiple_polylines(result_image, count_polylines4, is_closed=False, color=(89,141,252), thickness=2)
#Show results of drawing tracks
cv2.imshow('Result Image', result_imagecount)
cv2.imwrite("tracks_and_counting_lines.jpg", result_imagecount)
cv2.waitKey(0)
cv2.destroyAllWindows()
