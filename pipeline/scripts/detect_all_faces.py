import sys
import numpy as np
import cv2 as cv

def proc():

	model=sys.argv[1]
	movieFile=sys.argv[2]
	outfile=sys.argv[3]

	yunet = cv.FaceDetectorYN.create(
		model=model,
		config='',
		input_size=(320, 320),
		score_threshold=0.6,
		nms_threshold=0.3,
		top_k=5000,
		backend_id=cv.dnn.DNN_BACKEND_DEFAULT,
		target_id=cv.dnn.DNN_TARGET_CPU
	)

	with open(outfile, "w") as out:

		cap = cv.VideoCapture(movieFile)
		idx=0
		while (cap.isOpened()):

			ret, image = cap.read()

			if image is None:
				break

			yunet.setInputSize((image.shape[1], image.shape[0]))
			_, faces = yunet.detect(image) # faces: None, or nx15 np.array

			if faces is not None:
				for fid, face in enumerate(faces):
					out.write("%s\t%s\t%s\n" % (idx, fid, ' '.join([str(x) for x in face])))

					# Tab output

					# 0 frame number
					# 1 face number within frame
					# 2 face information (space-separated):

						# Output
						# https://docs.opencv.org/4.x/df/d20/classcv_1_1FaceDetectorYN.html

						# 0-1: x, y of bbox top left corner
						# 2-3: width, height of bbox
						# 4-5: x, y of right eye (blue point in the example image)
						# 6-7: x, y of left eye (red point in the example image)
						# 8-9: x, y of nose tip (green point in the example image)
						# 10-11: x, y of right corner of mouth (pink point in the example image)
						# 12-13: x, y of left corner of mouth (yellow point in the example image)
						# 14: face score

						# box=face[:4]
						# landmarks=face[4:len(face)-1]
						# landmarks = np.array_split(landmarks, len(landmarks) / 2)

			idx+=1

if __name__ == "__main__":
	proc()