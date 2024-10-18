import numpy as np
from numpy import linalg as LA
import os

class IMDBVecs:

	def __init__(self, actor_vec_path, castPath):

		self.castPath=castPath
		vecs={}

		self.casts={}

		with open(actor_vec_path) as file:
			for line in file:
				cols=line.rstrip().split("\t")
				actor_tt=cols[0]

				img_tt=cols[1]
				vec=np.array(cols[6].split(" "), dtype=float)

				if actor_tt not in vecs:
					vecs[actor_tt]={}

				if img_tt not in vecs[actor_tt]:
					vecs[actor_tt][img_tt]=[]

				vecs[actor_tt][img_tt].append(vec)

		self.actor_vecs={}
		for actor_tt in vecs:
			for img_tt in vecs[actor_tt]:
				# only keep actor images with one face detected
				if len(vecs[actor_tt][img_tt]) == 1:
					vec=vecs[actor_tt][img_tt][0]
					vec=vec/LA.norm(vec, 2)

					if actor_tt not in self.actor_vecs:
						self.actor_vecs[actor_tt]=[]
					self.actor_vecs[actor_tt].append(vec)

		for actor_tt in self.actor_vecs:
			self.actor_vecs[actor_tt]=np.array(self.actor_vecs[actor_tt])


	def read_cast(self, imdb_id):

		# cast list is a tab-separated file parsed from https://www.imdb.com/title/<IMDB_ID>/fullcredits/

		# 0 IMDB actor ID (starts with "tt")
		# 1 Actor name
		# 2 IMDB movie ID
		# 3 Character name

		path="%s/%s.txt" % (self.castPath, imdb_id)

		meta={}
		if os.path.exists(path):
			with open(path) as file:
				for line in file:
					cols=line.rstrip().split("\t")
					if len(cols) > 4:

						actor_tt=cols[0]
						character_name=cols[3]
						actor_name=cols[1]
						meta[actor_tt]=(character_name,actor_name)
		return meta



	def get_actors(self, vec, imdb, num_to_get=5, aggregator=np.mean):
		vec=vec/LA.norm(vec, 2)

		if imdb not in self.casts:
			self.casts[imdb]=self.read_cast(imdb)

		cast=self.casts[imdb]


		scores={}

		for actor_tt in cast:
			if actor_tt in self.actor_vecs:
				sims=self.actor_vecs[actor_tt].dot(vec)
				mean=aggregator(sims)

				scores[actor_tt]=mean

		vals=[]
		for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True):
			vals.append("%s:%.3f" % (k,v))

		return vals[:num_to_get]

	


	def get_actor(self, vec, imdb, aggregator=np.mean):
		vec=vec/LA.norm(vec, 2)

		if imdb not in self.casts:
			self.casts[imdb]=self.read_cast(imdb)

		cast=self.casts[imdb]
		
		high_score=0
		high_actor=None


		for actor_tt in cast:
			if actor_tt in self.actor_vecs:
				sims=self.actor_vecs[actor_tt].dot(vec)
				mean=aggregator(sims)

				if mean > high_score:
					high_score=mean
					high_actor=actor_tt

		if high_actor is None:
			return None, None, None, 0

		return high_actor, cast[high_actor][0], cast[high_actor][1], high_score






