# Actor recognition

Given an input movie (in MP4 form), this pipeline recognizes all faces in the movie, assembles them into tracks, generates vector representations for those tracks and matches them to the actors from that movie's cast.  For our process digitizing movies and converting to MP4s, see [digitizing.md](digitizing.md).

## Install

```
conda create moviepipeline python=3.9
conda activate moviepipeline
pip install tensorflow
pip install ffmpeg-python pillow
pip install git+https://github.com/soCzech/TransNetV2.git
pip install opencv-python
pip install insightface
pip install onnxruntime
pip install bs4
pip install unidecode
```

## Download models

```
mkdir -p TransNetV2/inference/transnetv2-weights
wget -P TransNetV2/inference/transnetv2-weights/ https://github.com/soCzech/TransNetV2/raw/master/inference/transnetv2-weights/saved_model.pb
wget -P TransNetV2/inference/transnetv2-weights/variables/ https://github.com/soCzech/TransNetV2/raw/master/inference/transnetv2-weights/variables/variables.data-00000-of-00001
wget -P TransNetV2/inference/transnetv2-weights/variables/ https://github.com/soCzech/TransNetV2/raw/master/inference/transnetv2-weights/variables/variables.index

mkdir yunet
wget -P yunet/ https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx

mkdir data

wget --no-check-certificate https://figshare.com/ndownloader/files/50086221 -O data/imdb.actor.faces.insightface.txt.gz
gunzip data/imdb.actor.faces.insightface.txt.gz

wget --no-check-certificate https://figshare.com/ndownloader/files/50086176 -O data/casts.tar.gz
tar -xzvf data/casts.tar.gz -C data
```

## Process a movie

* `MOV_FILE` is the path to the movie to process (e.g. *.mp4 file)
* `MOV_ID` is an identifier you provide (used for output files)
* `IMDB_ID` is the IMDB identifier for the movie
* `OUTDIR` is a folder to write output files to.

```
# directory containing casts lists from IMDB 
CAST_DIR=data/casts/

# file containing face representations for actors from IMDB
IMDB_REP_FILE=data/imdb.actor.faces.insightface.txt

mkdir -p $OUTDIR/$MOV_ID

FPS_FILE=$OUTDIR/$MOV_ID.fps.txt
FACES_FILE=$OUTDIR/$MOV_ID.faces_detected.txt
TRACK_REP_FILE=$OUTDIR/$MOV_ID.insightface.txt
TRACKS_FILE=$OUTDIR/$MOV_ID.tracks.txt
SCENES_FILE=$OUTDIR/$MOV_ID.scenes.txt
RECOG_FILE=$OUTDIR/$MOV_ID.recog.txt

```

### get metadata like fps and length

```
python scripts/get_fps.py $MOV_FILE $FPS_FILE $MOV_ID
```

### find shot boundaries using transnetv2

`python scripts/get_shots.py TransNetV2/inference/transnetv2-weights/ $MOV_FILE $SCENES_FILE`

### find faces

`python scripts/detect_all_faces.py yunet/face_detection_yunet_2023mar.onnx $MOV_FILE $FACES_FILE`

### generate face tracks and representations

`python scripts/track_representation.py $SCENES_FILE $FACES_FILE $MOV_FILE $TRACK_REP_FILE $TRACKS_FILE`

### match to IMDB

`python scripts/match_to_imdb.py $IMDB_REP_FILE $CAST_DIR $IMDB_ID $TRACK_REP_FILE $RECOG_FILE`


## Output format

FPS_FILE contains one line, tab-separated with the following columns:

* movie ID
* total number of frames
* width
* height
* frames per second

SCENES_FILE contains one shot per line, tab-separated with the following columns:

* start frame number
* end frame number


FACES\_FILE contains one face per line, tab-separated with the following columns:

* frame number
* face number within frame
* face bounding box + landmarks (space-separated), cf. [here](https://docs.opencv.org/4.x/df/d20/classcv_1_1FaceDetectorYN.html):
	* 0-1: x, y of bbox top left corner
	* 2-3: width, height of bbox
	* 4-5: x, y of right eye 
	* 6-7: x, y of left eye
	* 8-9: x, y of nose tip 
	* 10-11: x, y of right corner of mouth 
	* 12-13: x, y of left corner of mouth
	* 14: face score

TRACKS\_FILE contains one face per line, along with the face track it belongs to.  This file is tab-separated, with the following columns:

* track number
* frame number
* face number within frame
* x of bbox top left corner
* y of bbox top left corner
* x of bbox bottom right corner
* y of bbox bottom right corner

TRACK\_REP\_FILE contains one track representation per line, tab-separated with the following columns:

* track number
* frame number of face that represents that track (i.e., the face in the track with the highest detection score)
* face-number-within-frame of face that represents that track (i.e., the face in the track with the highest detection score)
* insightface vector representation (512 dimensions)


RECOG\_FILE contains one track per line, tab-separated with the following columns:

* track number
* frame number of face that represents that track (i.e., the face in the track with the highest detection score)
* face-number-within-frame of face that represents that track (i.e., the face in the track with the highest detection score)
* ranked list of the 10 highest-matching actors to that track representation, space separated. Each actor is paired with their recognition score (colon-separated, e.g. -- actor:score) and the highest scoring actor is at position 0.  (For all experiments, we set 0.18 as the minimum recognition threshold.)
	

## Visualization (public domain)

To visualize the outcome of this process, the following script executes each of the steps above on a 1-minute clip from *The Hitch-Hiker* (1953), a film currently in the public domain in the United States, as determined by the [Library of Congress](https://www.loc.gov/item/mbrs00047382/).  Be sure to follow the installation and downloading instructions above, and then execute the following script from this directory.

```
./scripts/movie_pipeline.sh
```

This script downloads a 1-minute clip of the *The Hitch-Hiker* into the `example`/ folder, runs the pipeline on that movie, and overlays the recognized actors onto that movie in the file `example/hitchhiker_clip_25.processed.mp4` (which can be viewed since this is in a public domain film).

This output file can be viewed [here](https://drive.google.com/file/d/163-b5UE4cMkqIxe7Nv9lYoFxzYaGCfsi/view?usp=drive_link).


