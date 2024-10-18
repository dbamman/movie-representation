import sys
from transnetv2 import TransNetV2

transnetWeights=sys.argv[1]
movieFile=sys.argv[2]
outFile=sys.argv[3]

model = TransNetV2(model_dir=transnetWeights)
video_frames, single_frame_predictions, all_frame_predictions = \
    model.predict_video(movieFile)

scenes=model.predictions_to_scenes(single_frame_predictions)

with open(outFile, "w") as out:
    for start, end in scenes:
        out.write("%s %s\n" % (start,end))
