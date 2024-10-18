This directory contains R scripts to generate the plots found in this paper.  All scripts will generate pdfs that can be found in this directory.

Generate plots for race/ethnicity and gender representation (LOESS)

```
Rscript points_with_loess95.r
```

Generate plots for race/ethnicity and gender representation (yearly confidence intervals).

```
Rscript ci_by_year.r > ci_by_year_rho.txt
```

Generate distribution of lead vs. non-lead facetimes

```
Rscript lead_nonlead.r
```