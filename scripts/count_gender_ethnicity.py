import sys, json
from collections import Counter

vals={}
minScore=0.18

demo={}
genders={}

eths=["black", "east_asian", "hispanic_latino", "south_asian", "white", "other"]

def get_gender_for_year(gender_json, year):
	ordered_years=sorted(list(gender_json.keys()))
	if len(ordered_years) == 1:
		return gender_json[ordered_years[0]].split("#")

	for idx, thisyear in enumerate(ordered_years):

		# if we've reach the last value, return that
		if idx == len(ordered_years)-1:
			return gender_json[thisyear].split("#")

		# otherwise check if the target year is between the current year and the next one in the list
		nextyear=ordered_years[idx+1]
		if year >= thisyear and year < nextyear:
			return gender_json[thisyear].split("#")


def str2int(x):
	return {int(k):v for k,v in x.items()}
	
def read_gender(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			gender_json=json.loads(cols[2], object_hook=str2int)
			genders[idd]=gender_json



def read_demo(filename):

	mapper={}
	mapper["Black (b)"]="black"
	mapper["East Asian (e)"]="east_asian"
	mapper["Hispanic/Latino (h)"]="hispanic_latino"
	mapper["None of the above (n)"]="other"
	mapper["South Asian/Indian (s)"]="south_asian"
	mapper["White (w)"]="white"


	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]

			# if cols[13] == NA, then at least two perceptions are that this actor is not a real person and we should skip
			if cols[13] != "NA":

				demo[idd]={}
				for val in eths:
					demo[idd][val]=0
				for col in cols[1:11]:
					for val in col.split("#"):
						if val.rstrip() != "This is not a real person - e.g., cartoon character or animal (c)":
							demo[idd][mapper[val]]+=1





def read_meta(filename):
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			year=int(cols[3])
			vals[idd]=year

def read_fps(filename):

	with open(filename) as file:
		cols=file.readline().split("\t")

		frames=int(cols[1])
		fps=float(cols[4])
		return frames, fps

def read_recog(filename):
	recog={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=cols[0]

			actor, score=cols[3].split(" ")[0].split(":")
			recog[trackno]=actor, float(score)

	return recog


def get_tracks(filename):
	tracks={}
	tracks2fno={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			trackno=cols[0]
			fno=cols[1]
			faceno=cols[2]
			x1=max(0,int(cols[3]))
			y1=max(0,int(cols[4]))
			x2=int(cols[5])
			y2=int(cols[6])

			if fno not in tracks:
				tracks[fno]=[]
			tracks[fno].append((trackno, faceno, x1,y1,x2,y2))

			if trackno not in tracks2fno:
				tracks2fno[trackno]=[]
			tracks2fno[trackno].append(fno)
	return tracks, tracks2fno


def proc(dataFolder):

	idx=0
	for mov_id in vals:

		actors={}
		eth_counts={}
		gender_counts={"male":{}, "female":{}}

		year=vals[mov_id]
		
		for eth in eths:
			eth_counts[eth]={}

		trackFile="%s/%s/%s.tracks.txt" % (dataFolder,mov_id,mov_id)
		recogFile="%s/%s/%s.recog.txt" % (dataFolder,mov_id,mov_id)
		fpsFile="%s/%s/%s.fps.txt" % (dataFolder,mov_id,mov_id)

		recog=read_recog(recogFile)
		tracks, tracks2fno=get_tracks(trackFile)
		total_frames, fps=read_fps(fpsFile)

		face_frames={}

		total_num_addressable_faces_in_frames=0
		total_num_addressable_faces_in_frames_gender=0

		for trackno in recog:
			for fno in tracks2fno[trackno]:
				face_frames[fno]=1


		eth_face_track_counts=Counter()
		gender_face_track_counts=Counter()


		for trackno in recog:

			actor, score=recog[trackno]

			if score > minScore:
				if actor in demo:

					total_num_addressable_faces_in_frames+=len(tracks2fno[trackno])
	
					for dem in demo[actor]:

						percent=demo[actor][dem]/10

						eth_face_track_counts[dem]+=len(tracks2fno[trackno]) * percent

						for fno in tracks2fno[trackno]:							
							eth_counts[dem][fno]=percent

				if actor in genders:

					total_num_addressable_faces_in_frames_gender+=len(tracks2fno[trackno])
	
					for gender in get_gender_for_year(genders[actor], year):

						if gender not in gender_counts:
							gender_counts[gender]={}

						gender_face_track_counts[gender]+=len(tracks2fno[trackno])

						for fno in tracks2fno[trackno]:
							gender_counts[gender][fno]=1


		for dem in eth_counts:
			addressable_ratio=None
			if total_num_addressable_faces_in_frames > 0:
				addressable_ratio=eth_face_track_counts[dem]/total_num_addressable_faces_in_frames
			print("%s\t%s\t%s" % (mov_id, dem, addressable_ratio))
			sys.stdout.flush()

		for gender in gender_counts:
			addressable_ratio=None
			if total_num_addressable_faces_in_frames_gender > 0:
				addressable_ratio=gender_face_track_counts[gender]/total_num_addressable_faces_in_frames_gender
			print("%s\t%s\t%s" % (mov_id, gender, addressable_ratio))
			sys.stdout.flush()

	


metaFile=sys.argv[1]
demoFile=sys.argv[2]
genderFile=sys.argv[3]
dataFolder=sys.argv[4]
read_meta(metaFile)
read_demo(demoFile)
read_gender(genderFile)
proc(dataFolder)

