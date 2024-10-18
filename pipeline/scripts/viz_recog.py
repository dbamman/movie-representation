# pip install unidecode
import sys, re
import cv2
from unidecode import unidecode

pred_threshold=0.18

movieFile=sys.argv[1]
outFile=sys.argv[2]
recogFile=sys.argv[3]
faceFile=sys.argv[4]
nameFile=sys.argv[5]

track_actors={}

start_tracks={}
end_tracks={}

names={}

def read_names(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			names[cols[0]]=cols[1]


read_names(nameFile)

def read_ids(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=int(cols[0])
			actor_parts=cols[3].split(" ")[0].split(":")
			actor=actor_parts[0]
			conf=float(actor_parts[1])
			
			track_actors[trackno]=actor,conf


def read_faces(filename):

	frame_faces={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=int(cols[0])
			fno=int(cols[1])
			faceno=int(cols[2])
			x1,y1,x2,y2=int(cols[3]), int(cols[4]), int(cols[5]), int(cols[6])

			if fno not in frame_faces:
				frame_faces[fno]=[]
			frame_faces[fno].append((x1,y1,x2,y2, trackno))

			if trackno not in start_tracks:
				start_tracks[trackno]=fno
				end_tracks[trackno]=fno
			else:
				end_tracks[trackno]=fno
	
	return frame_faces		


def proc(filename, outFile, all_faces):

	cap = cv2.VideoCapture(movieFile)

	fps = cap.get(cv2.CAP_PROP_FPS)

	vid_width=round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	vid_height=round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	idx=0

	output = cv2.VideoWriter(outFile, cv2.VideoWriter_fourcc(*'mp4v'), fps, (vid_width, vid_height))

	while (cap.isOpened()):

		ret, image = cap.read()

		if image is None:
			break

		if idx in all_faces:
			for face_no, face in enumerate(all_faces[idx]):
				
				x1,y1,x2,y2,track_no=face

				if track_no is None:
					cv2.rectangle(image, (x1,y1),(x2,y2), (0, 255, 0), 1)

				else:
					actor, conf=track_actors[track_no]

					if conf > pred_threshold:

						if actor in names:
							actor=unidecode(names[actor])
						
						color=(255,0,255)
	
						cv2.rectangle(image, (x1,y1), (x2,y2), color, 1)
						cv2.putText(image, "%s" % (actor), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, .5, color, 1)

		output.write(image) 

		idx+=1

	output.release()
	cap.release()


read_ids(recogFile)			
faces=read_faces(faceFile)

proc(movieFile, outFile, faces)




