import sys,re
from bs4 import BeautifulSoup
import os
import requests
import random
random.seed(1)
import time
from requests.exceptions import ConnectionError
from random import shuffle


def get_names(filename):
	names={}
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			idd=cols[0]
			name=cols[1]
			names[idd]=name
	return names

def filter(text):
	text=re.sub("[\n\t\r ]+", " ", text)
	return text.lstrip().rstrip()

def get_table_cell(actor):
	actor_link=actor.findAll('a')[0].attrs["href"]
	actor_link=actor_link.split("/")[2]
	actor_name=filter(actor.text)

	return actor_link, actor_name


def get_cast(page):

	cast_info={}
	soup = BeautifulSoup(page, 'html.parser')

	items=soup.findAll('table', {"class":"cast_list"})
	if len(items) > 0:
		cast_list=items[0].findAll('tr')

		if len(cast_list) > 0:
			for cast in cast_list:
				tds=cast.findAll('td')
				if len(tds) == 4:
					
					try:
						pic_cell=tds[0].findAll('img')[0]
						actor_pic=None
						if "loadlate" in pic_cell.attrs:
							actor_pic=pic_cell.attrs["loadlate"]

						actor_link, actor_name=get_table_cell(tds[1])
						character_link, character_name=get_table_cell(tds[3])

						cast_info[actor_link]=actor_name, character_link, character_name, actor_pic

					except Exception as e:
						print(e)
						pass
		
	return cast_info

def get_page(tt, force=False):
	path="%s/%s.html" % (castDir,tt)
	if not os.path.exists(path) or force == True:
		url="https://www.imdb.com/title/%s/fullcredits/?ref_=tt_cl_sm" % tt
		try:
			r = requests.get(url)
			data=r.text

			with open(path, "w", encoding="utf-8") as out:
				out.write(data)
		except ConnectionError as e:
			print("ConnectionError2")
			time.sleep(60)

	else:
		with open(path) as file:
			data=file.read()

	return data

def get_actor_pic_page(tt, force=False):
	path="%s/metadata/%s.html" % (actorPics,tt)
	if not os.path.exists(path) or force == True:
		url="https://www.imdb.com/name/%s/mediaindex?ref_=nm_phs_md_sm" % tt

		try:
			r = requests.get(url)
			data=r.text

			with open(path, "w", encoding="utf-8") as out:
				out.write(data)
		except ConnectionError as e:
			print("ConnectionError3")				
			time.sleep(60)

	else:
		with open(path) as file:
			data=file.read()

	return data

def get_full_img(src):
	parts=src.split("_V1_");
	src=parts[0] + "_V1_" + ".jpg"
	return src

def get_pics(page, name):

	pic_list=[]
	soup = BeautifulSoup(page, 'html.parser')

	items=soup.findAll('div', {"class":"media_index_thumb_list"})
	if len(items) > 0:
		pics=items[0].findAll('img')
		# print(pics)
		if len(pics) > 0:
			for pic in pics:
				alt=pic.attrs["alt"].lstrip().rstrip()
				src=pic.attrs["src"]
				matcher=re.search("^(.*?) (in|at) ", alt)
				# print(alt)
				if matcher is not None:
					match=matcher.group(1)
					if match == name:
						src=get_full_img(src)
						pic_list.append(src)
				else:
					matcher2=re.search("^(.*?)$", alt)
					if matcher2 is not None:
						match=matcher2.group(1)
						if match == name:
							src=get_full_img(src)
							pic_list.append(src)

	return pic_list


def proc(tt, names):
	max_pics=10
	page=get_page(tt, force=False)
	cast=get_cast(page)
	# print(cast)
	with open("%s/%s.txt" % (castDir,tt), "w") as cast_out:
		for actor_tt in cast:
			actor_name, character_link, character_name, actor_pic=cast[actor_tt]

			cast_out.write("%s\t%s\t%s\t%s\t%s\n" % (actor_tt, actor_name, character_link, character_name, actor_pic))

			if actor_pic is not None and actor_tt in names:
				actor_page=get_actor_pic_page(actor_tt)
				pics=get_pics(actor_page, names[actor_tt])
				if len(pics) > 0:
					try:
						os.makedirs("%s/pics/%s" % (actorPics,actor_tt))
					except:
						pass

				shuffle(pics)

				for pic in pics[:max_pics]:
					filen=pic.split("/")[-1]
					path="%s/pics/%s/%s" % (actorPics, actor_tt, filen)

					if not os.path.exists(path):
						try:
							r = requests.get(pic)
							time.sleep(3)
							data=r.content

							with open(path, "wb") as out:
								out.write(data)
						except ConnectionError as e:
							print("ConnectionError, sleeping")
							time.sleep(60)

if __name__ == "__main__":

	# directory for cast information
	castDir=sys.argv[3]
	# diretory for actor pics
	actorPics=sys.argv[4]

	os.makedirs(castDir, exist_ok=True)
	os.makedirs("%s/metadata" % actorPics, exist_ok=True)



	names=get_names(sys.argv[1])
	proc(sys.argv[2], names)


