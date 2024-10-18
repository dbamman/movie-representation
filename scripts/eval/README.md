Get data (6.0 gb)

```
wget http://yosemite.ischool.berkeley.edu/filmanalytics/data/eval_data.tar
tar -xf eval_data.tar
```

Evaluate face detection with AP and generate evaluation data for recognition.

```
python eval_face_actor.py data/mov.splits.txt train,dev eval_data > train_dev.results.txt
python eval_face_actor.py data/mov.splits.txt test eval_data > test.results.txt
```

Evaluate face recognition, tuning the confidence threshold on the training/dev data.

```
python calc_face_recognition.py train_dev.results.txt test.results.txt
```


Calculate bias over test data, tuning the multiplier on the training/dev data.

```
python calculate_race_gender_bias.py ../../data/actor_race_top90.tsv ../../data/wikidata.actor.historical.gender.tsv train_dev.results.txt test.results.txt ../../data/all.movies.ids.txt
```


