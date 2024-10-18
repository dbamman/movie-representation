

class FaceTracker:

	def __init__(self, minIOU=0.3, min_track_length=2, min_track_conf=0.5, num_best=1):
		
		# minimum overlap between successive frames
		self.minIOU=minIOU
		
		# minimum number of frames for track
		self.min_track_length=min_track_length

		# minimum max confidence for single face in track
		self.min_track_conf=min_track_conf

		# number of best faces to average over when creating representation for track
		self.num_best=num_best

	def get_iou(self, bb1, bb2):
		"""
		https://stackoverflow.com/questions/25349178/calculating-percentage-of-bounding-box-overlap-for-image-detector-evaluation
		Calculate the Intersection over Union (IoU) of two bounding boxes.

		Parameters
		----------
		bb1 : dict
			Keys: {'x1', 'x2', 'y1', 'y2'}
			The (x1, y1) position is at the top left corner,
			the (x2, y2) position is at the bottom right corner
		bb2 : dict
			Keys: {'x1', 'x2', 'y1', 'y2'}
			The (x, y) position is at the top left corner,
			the (x2, y2) position is at the bottom right corner

		Returns
		-------
		float
			in [0, 1]
		"""


		# print(bb1, bb2)
		assert bb1['x1'] < bb1['x2']
		assert bb1['y1'] < bb1['y2']
		assert bb2['x1'] < bb2['x2']
		assert bb2['y1'] < bb2['y2']

		# determine the coordinates of the intersection rectangle
		x_left = max(bb1['x1'], bb2['x1'])
		y_top = max(bb1['y1'], bb2['y1'])
		x_right = min(bb1['x2'], bb2['x2'])
		y_bottom = min(bb1['y2'], bb2['y2'])

		if x_right < x_left or y_bottom < y_top:
			return 0.0

		# The intersection of two axis-aligned bounding boxes is always an
		# axis-aligned bounding box
		intersection_area = (x_right - x_left) * (y_bottom - y_top)

		# compute the area of both AABBs
		bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
		bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

		# compute the intersection over union by taking the intersection
		# area and dividing it by the sum of prediction + ground-truth
		# areas - the interesection area
		iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
		assert iou >= 0.0
		assert iou <= 1.0
		return iou


	def get_best_faces(self, rev_tracks, all_faces):

		track_best_reps=[]

		vals={}
		for (frame_no, face_no) in rev_tracks:
			
			face=all_faces[frame_no][face_no]
			vals[(frame_no, face_no)]=face["confidence"]

		sorted_list=[]
		for (frame_no, face_no), v in list(sorted(vals.items(), key=lambda item: item[1], reverse=True))[:self.num_best]:		
			track_best_reps.append((frame_no,face_no))

		return track_best_reps



	def get_best_frames(self, tracks, all_faces):
		
		# tracknum: (frame_no, face_no)
		rev_tracks={}
		for key in tracks:
			if tracks[key] not in rev_tracks:
				rev_tracks[tracks[key]]=[]
			rev_tracks[tracks[key]].append(key)

		track_best_reps={}

		for track_num in rev_tracks:
			if track_num is not None:
				track_best_reps[track_num]=self.get_best_faces(rev_tracks[track_num], all_faces)


			
		best_frames={}

		for track_num in track_best_reps:
			for frame_no,face_no in track_best_reps[track_num]:
				if frame_no not in best_frames:
					best_frames[frame_no]=[]
				best_frames[frame_no].append(face_no)


		return track_best_reps, best_frames

	# Bochinski et al. 2017, "High-Speed Tracking-by-Detection Without Using Image Information"
	def get_tracks(self, all_faces, boundaries):

		tracks={}

		highest_conf_in_track={}

		highID=0

		for i in range(0, len(all_faces)):

			# scene starts start a new track; 0 is in boundaries
			if i == 0 or i in boundaries:

				for j, face in enumerate(all_faces[i]):
					tracks[i,j]=highID
					conf=face["confidence"]
					highest_conf_in_track[highID]=conf
					highID+=1

			else:
		
				lastFaces=all_faces[i-1]
				currentFaces=all_faces[i]

				for j, face in enumerate(currentFaces):
					maxIOU=0
					highLastFace=None
					for k, lastFace in enumerate(lastFaces):
						iou=self.get_iou(face, lastFace)
						if iou > maxIOU and iou > self.minIOU:
							highLastFace=(i-1,k)
							maxIOU=iou

					# two frames back
					if i > 1 and i-1 not in boundaries:
						faces_2=all_faces[i-2]
						for k, lastFace in enumerate(faces_2):
							iou=self.get_iou(face, lastFace)
							if iou > maxIOU and iou > self.minIOU:
								highLastFace=(i-2,k)
								maxIOU=iou

					# three frames back						
					if i > 2 and i-1 not in boundaries and i-2 not in boundaries:
						faces_2=all_faces[i-3]
						for k, lastFace in enumerate(faces_2):
							iou=self.get_iou(face, lastFace)
							if iou > maxIOU and iou > self.minIOU:
								highLastFace=(i-3,k)
								maxIOU=iou

					if highLastFace is not None:
						tracks[(i,j)]=tracks[highLastFace]
					else:
						tracks[(i,j)]=highID
						highID+=1

					track=tracks[(i,j)]
					conf=face["confidence"]
					if track not in highest_conf_in_track:
						highest_conf_in_track[track]=conf
					else:
						if conf > highest_conf_in_track[track]:
							highest_conf_in_track[track]=conf

		rev_tracks={}
		for frame_no, face_no in tracks:
			track=tracks[frame_no, face_no]
			if track not in rev_tracks:
				rev_tracks[track]=[]
			rev_tracks[track].append((frame_no, face_no))

		invalid_tracks={}
		track_mapper={}

		for track_no in rev_tracks:
			if len(rev_tracks[track_no]) < self.min_track_length:
				invalid_tracks[track_no]="min_track"
			elif highest_conf_in_track[track_no] < self.min_track_conf:
				invalid_tracks[track_no]="low_track_conf"
			else:
				track_mapper[track_no]=len(track_mapper)


		for frame_no, face_no in tracks:
			track=tracks[frame_no, face_no]
			if track in invalid_tracks:
				tracks[frame_no, face_no]=None
			else:
				tracks[frame_no, face_no]=track_mapper[track]


		return tracks


