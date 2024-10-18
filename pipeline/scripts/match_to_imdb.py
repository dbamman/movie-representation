import sys, re, os
import numpy as np
import random

from imdb_vecs import IMDBVecs

imdb_reps=sys.argv[1]
castDir=sys.argv[2]
imdb_id=sys.argv[3]
insightfaceFile=sys.argv[4]
outpath=sys.argv[5]

def proc(imdb_id, insightfaceFile, outfile, imdbvecs):

	track_actors={}

	missing={}

	trackreps={}

	with open(outfile, "w") as out:
		with open(insightfaceFile) as file:
			for line in file:
				cols=line.rstrip().split("\t")
				track=cols[0]

				vec=np.array(cols[-1].split(" "), dtype=float)

				trackreps[track]=vec

				top_actors=imdbvecs.get_actors(vec, imdb_id, num_to_get=10, aggregator=np.mean)
				out.write("%s\t%s\tACTOR\n" % ('\t'.join(cols[:-1]), ' '.join(top_actors)))



imdbvecs=IMDBVecs(imdb_reps, castDir)
proc(imdb_id, insightfaceFile, outpath, imdbvecs)

