Get the movie processed data for all 2,307 movies.  This includes information on faces assigned to each track, actor information and metadata (fps, length, etc.)  Note this file is 19G.

```
cd data
wget yosemite.ischool.berkeley.edu/filmanalytics/data/MOVIE_ANALYSIS_DATA.tar
tar -xf MOVIE_ANALYSIS_DATA.tar
```

Calculate within-movie entropy

```
python calc_entropy.py ../data/all.movies.ids.txt ../data/actor_race_top90.tsv ../data/MOVIE_ANALYSIS_DATA > ../data/movie_entropy.txt
```

Calculate representation for gender and race/ethnicity

```
python count_gender_ethnicity.py ../data/all.movies.ids.txt ../data/actor_race_top90.tsv ../data/wikidata.actor.historical.gender.tsv ../data/MOVIE_ANALYSIS_DATA > ../data/movie_gender_ethnicity.txt

```

Compare representation in popular films to award nominees.

```
compare_awards.py
```

Count screentime by actor per movie.

```
python count_cast_screentime.py ../data/all.movies.ids.txt ../data/MOVIE_ANALYSIS_DATA > ../data/screentime.actor.full.txt
```

Measure Spearman rank correlation between screentime and facetime.

```
python measure_screentime.py ../data/gold_screentimes.tsv ../data/screentime.actor.full.txt
```

Find boundary between leads and non-leads.

```
python lead_vs_nonleads.py ../data/gold_screentimes.tsv ../data/screentime.actor.full.txt ../data/leads.txt
```

Calculate screentime for leads and non-leads separately.

```
python count_gender_ethnicity_leadvnonlead.py ../data/all.movies.ids.txt ../data/actor_race_top90.tsv ../data/wikidata.actor.historical.gender.tsv ../data/MOVIE_ANALYSIS_DATA > ../data/movie_gender_ethnicity_leads_maxratio.txt
```

Calculate year-level confidence intervals

```
python ci_by_year.py ../data/top50.tsv > ../data/ci_by_year.txt
```

Analyze representation by director gender

```
python analyze_director.py ../data/top50.tsv > ../data/dir_gender.txt
```

Rank actors by total facetime in top 50 movies (1980-2022).

```
wget --no-check-certificate https://datasets.imdbws.com/name.basics.tsv.gz
gunzip name.basics.tsv.gz
python get_top_screentime.py ../data/top50.tsv ../data/screentime.actor.full.txt name.basics.tsv > ../data/most_frequent_actors_top50movs.txt
```

Calculate bootstrap confidence intervals for all LOESS plots

```
./bootstrap_loess.sh
```