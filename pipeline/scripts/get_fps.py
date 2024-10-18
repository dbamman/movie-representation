import sys, re
import cv2

def proc(infile, outfile, idd):

	with open(outfile, "w", encoding="utf-8") as out:
		cap = cv2.VideoCapture(infile)

		fps = cap.get(cv2.CAP_PROP_FPS)
		width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

		out.write("%s\t%s\t%s\t%s\t%s\n" % (idd, length, width, height, fps))


proc(sys.argv[1], sys.argv[2], sys.argv[3])