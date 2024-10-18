MOV_FILE=example/hitchhiker_clip_25.mp4
OUT_FILE=example/hitchhiker_clip_25.processed.mp4

MOV_ID=hitchhiker
IMDB_ID=tt0045877

# get input file
wget -P example http://yosemite.ischool.berkeley.edu/filmanalytics/data/hitchhiker_clip_25.mp4

OUTDIR=computed_data/$MOV_ID

mkdir -p $OUTDIR

wget -P data https://datasets.imdbws.com/name.basics.tsv.gz
gunzip data/name.basics.tsv.gz

# For movies in our data of 2,307 films, actor representations are found in data/imdb.actor.faces.insightface.txt
# For movies that are not in our collection, get the cast list from IMDB and generate representations of actors in them.

date

echo "getting cast pics"
# Get cast and sample of actor pics from IMDB (the Hitch-Hiker has IMDB ID tt0045877); this takes about 2.5 minutes for the Hitch-Hiker
python scripts/get_cast_pics.py data/name.basics.tsv $IMDB_ID example/casts example/actor_pics

echo "generating representations of cast"
# Generate representations of actors from those images, and store them in the file example/hitchhiker.insightface.txt
python scripts/get_reps_for_images.py example/actor_pics example/$MOV_ID.insightface.txt

#IMDB_REP_FILE=data/imdb.actor.faces.insightface.txt
#CAST_DIR=data/casts

IMDB_REP_FILE=example/$MOV_ID.insightface.txt
CAST_DIR=example/casts

FPS_FILE=$OUTDIR/$MOV_ID.fps.txt
FACES_FILE=$OUTDIR/$MOV_ID.faces_detected.txt
TRACK_REP_FILE=$OUTDIR/$MOV_ID.insightface.txt
TRACKS_FILE=$OUTDIR/$MOV_ID.tracks.txt
SCENES_FILE=$OUTDIR/$MOV_ID.scenes.txt
RECOG_FILE=$OUTDIR/$MOV_ID.recog.txt

# get metadata like fps and length

python scripts/get_fps.py $MOV_FILE $FPS_FILE $MOV_ID

# find shot boundaries using transnetv2

python scripts/get_shots.py TransNetV2/inference/transnetv2-weights/ $MOV_FILE $SCENES_FILE

# find faces

python scripts/detect_all_faces.py yunet/face_detection_yunet_2023mar.onnx $MOV_FILE $FACES_FILE

# generate face tracks and representations

python scripts/track_representation.py $SCENES_FILE $FACES_FILE $MOV_FILE $TRACK_REP_FILE $TRACKS_FILE

# match to IMDB

python scripts/match_to_imdb.py $IMDB_REP_FILE $CAST_DIR $IMDB_ID $TRACK_REP_FILE $RECOG_FILE

# for this public-domain movie, we can visualize the outputs onto the movie

python scripts/viz_recog.py $MOV_FILE $OUT_FILE $RECOG_FILE $TRACKS_FILE data/name.basics.tsv
