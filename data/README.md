This directory contains several data files used in this analysis.

## top50.tsv

Information about the top 50 movies by U.S. box office from 1980-2022, including metadata (e.g., box office rank, year of release, director, etc.) and quantities output from our pipeline (e.g., screentime by race/ethnicity and gender).

## awards.tsv

Award-nominated films from 1980-2022, including metadata (e.g., box office rank, year of release, director, etc.) and quantities output from our pipeline (e.g., screentime by race/ethnicity and gender).  Awards are: Academy Awards (Best Motion Picture of the Year, Best Picture), Golden Globe (Best Motion Picture-Drama, Best Motion Picture-Comedy or Musical), British Academy of Film and Television Arts (Best Film), Los Angeles Film Critics Association (Best Picture), National Board of Review  (Top Films, Top Ten Films), and National Society of Film Critics (Best Film).



## gold_screentimes.tsv

Screentime information from [https://www.screentimecentral.com/](https://www.screentimecentral.com/) for Oscar-nominated best actors and best supporting actors, linked to information about the actor and film IMDB ID.


## wikidata.actor.historical.gender.tsv

Gender information over the period 2014ff. extracted from Wikidata using data dumps from the [Internet Archive](https://archive.org/details/wikimediadownloads?tab=collection&query=wikidata) and [Wikidata](https://dumps.wikimedia.org/wikidatawiki/).



## actor\_race\_top90.tsv 

Perceptions of race/ethnicity for 6,740 actors by 10 participants on the Prolific survey platform, one each from participants who identify as {Black, East Asian, Hispanic/Latino, South Asian, White} x {Man (including trans men), Women {including trans women)}.  The 6,740 actors are those who together comprise 90% of all faces recognized in our dataset.

## The rest

All other files in this directory are generated through scripts found in the `scripts` directory.