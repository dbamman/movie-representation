import sys, glob
import os
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

filename=sys.argv[1]
outfile=sys.argv[2]

def proc_image(path, out):

	# path is structured like:
	# actorPics/pics/nm0639529/MV5BOWUxMTg1ZjMtNmJkMS00ZjEyLWIzM2MtZDA4MjNlYmJmOGM2XkEyXkFqcGdeQXVyMTI3MDk3MzQ@._V1_.jpg
	
	parts=path.split("/")
	actor_id=parts[-2]
	img_id=parts[-1]

	frame=cv2.imread(path)

	faces = app.get(frame)

	if len(faces) == 1:
		for f_idx, face in enumerate(faces):
			emb=face["embedding"]
			bbox=face["bbox"]

			for i in range(len(bbox)):
				if bbox[i] < 0:
					bbox[i]=0
					
			out.write("%s\t%s\t%s\t%s\t%s\t%s %s %s %s\t%s\n" % (actor_id, img_id, f_idx, 0, 0, bbox[0], bbox[1], bbox[2], bbox[3], ' '.join([str(x) for x in emb])))


def proc(folder):
	with open(outfile, "w") as out:
		for filename in glob.glob("%s/**/*.jpg" % folder, recursive=True):
			proc_image(filename, out)



proc(sys.argv[1])