# movie-representation

This repository contains code and data to support "Measuring diversity in Hollywood through the large-scale computational analysis of film." See each directory below for README.md files documenting them.

* `pipeline/`: Given an input movie (in MP4 form), this pipeline recognizes all faces in the movie, assembles them into tracks, generates vector representations for those tracks and matches them to the actors from that movie's cast.

* `scripts/` : This directory contains code to measure representation for race/ethnicity and gender, for both lead and non-lead actors, and compare representation across popular vs. award-nominated films.

* `data/`: This directory contains metadata about movies (including the aggregated output of all computational analysis above), along with information about perceptions of actor gender (from Wikidata) and race/ethnicity (from Prolific).

* `plots/`: This directory contains code to generate the plots that appear in this article.