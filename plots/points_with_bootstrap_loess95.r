library(ggplot2)

plotter <- function(data, dem, boot_intervals, ylabel, ymin_val, ymax_val) {
 
  # Plot
  g=ggplot(data=data, aes(y=dem, x=year)) + 

    # plot original points
    geom_point(alpha=0.1) + theme_classic() +

    # plot 95% confidence intervals over the LOESS predictions
    geom_line(data=boot_intervals, aes(x=V1, y=V3), col="#3e7fe6", size=1) +
    geom_ribbon(data=boot_intervals, aes(x=V1, ymin=V2, y=V3, ymax=V4), alpha=0.1, fill="black") +
    coord_cartesian(ylim = c(ymin_val, ymax_val)) + ylab(ylabel) + xlab("") +
    geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) +  # Horizontal grid lines with alpha +
    geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5) +  # Vertical grid lines with alpha
    theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 16),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )
  return (g)
}

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  # function to plot multiple graphs in one plot, from:
  # http://ianmadd.github.io/pages/multiplot.html

  require(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()     
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


# TOP 50

data=read.table("../data/top50.tsv", sep="\t", quote = "", head=TRUE, na.strings="None", comment.char = "")

ci_data_black=read.table("../data/ci/black.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_white=read.table("../data/ci/white.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_hl=read.table("../data/ci/hispanic_latino.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_ea=read.table("../data/ci/east_asian.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_sa=read.table("../data/ci/south_asian.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")


## ALL ##

# race/ethnicity

pdf("race_eth.pdf", width=7)
ggplot(data=data, aes(y=dem, x=year)) + 
geom_line(data=ci_data_black, aes(x=V1, y=V3), col="#ea5545", size=1) + geom_ribbon(data=ci_data_black, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#ea5545", alpha=0.2) +
geom_line(data=ci_data_ea, aes(x=V1, y=V3), col="#ef9b20", size=1) + geom_ribbon(data=ci_data_ea, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#ef9b20", alpha=0.2) +
geom_line(data=ci_data_sa, aes(x=V1, y=V3), col="#87bc45", size=1) + geom_ribbon(data=ci_data_sa, aes(x=V1, ymin=V2, y=V3, ymax=V4),  fill="#87bc45", alpha=0.2) +
geom_line(data=ci_data_hl, aes(x=V1, y=V3), col="#27aeef", size=1) + geom_ribbon(data=ci_data_hl, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#27aeef", alpha=0.2) +
geom_line(data=ci_data_white, aes(x=V1, y=V3), col="#b33dc6", size=1) + geom_ribbon(data=ci_data_white, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#b33dc6", alpha=0.2) +
coord_cartesian(ylim = c(0,1)) + ylab("% Facetime") + xlab("") + theme_classic() +
geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) +  # Horizontal grid lines with alpha +
geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5) +  # Vertical grid lines with alpha
theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 16),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )
dev.off()


pdf("race_eth_detail.pdf", width=7)
ggplot(data=data, aes(y=dem, x=year)) + 
geom_line(data=ci_data_black, aes(x=V1, y=V3), col="#ea5545", size=1) + geom_ribbon(data=ci_data_black, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#ea5545", alpha=0.2) +
geom_line(data=ci_data_ea, aes(x=V1, y=V3), col="#ef9b20", size=1) + geom_ribbon(data=ci_data_ea, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#ef9b20", alpha=0.2) +
geom_line(data=ci_data_sa, aes(x=V1, y=V3), col="#87bc45", size=1) + geom_ribbon(data=ci_data_sa, aes(x=V1, ymin=V2, y=V3, ymax=V4),  fill="#87bc45", alpha=0.2) +
geom_line(data=ci_data_hl, aes(x=V1, y=V3), col="#27aeef", size=1) + geom_ribbon(data=ci_data_hl, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#27aeef", alpha=0.2) +
geom_line(data=ci_data_white, aes(x=V1, y=V3), col="#b33dc6", size=1) + geom_ribbon(data=ci_data_white, aes(x=V1, ymin=V2, y=V3, ymax=V4), fill="#b33dc6", alpha=0.2) +
coord_cartesian(ylim = c(0,0.25)) + ylab("% Facetime") + xlab("") + theme_classic() +
geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) +  # Horizontal grid lines with alpha +
geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5) +  # Vertical grid lines with alpha
theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 16),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )
dev.off()



g_black=plotter(data, data$black, ci_data_black, "% Facetime, Black actors", 0, 0.25)

pdf("black_actors.pdf", width=7)
g_black
dev.off()
# gender

ci_data_women=read.table("../data/ci/women.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
g_women=plotter(data, data$women, ci_data_women, "% Facetime, Women", 0, 1)

pdf("gender.pdf", width=7)
multiplot(g_women, cols=1)
dev.off()



## LEADS ##

# race/ethnicity

ci_data_hl_lead=read.table("../data/ci/lead hispanic_latino.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_black_lead=read.table("../data/ci/lead black.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_white_lead=read.table("../data/ci/lead white.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_ea_lead=read.table("../data/ci/lead east_asian.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_sa_lead=read.table("../data/ci/lead south_asian.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")

g_hispanic_latino_lead=plotter(data, data$lead.hispanic_latino, ci_data_hl_lead, "Hispanic/Latino Lead", 0, 1)
g_black_lead=plotter(data, data$lead.black, ci_data_black_lead, "Black Lead", 0, 1)
g_white_lead=plotter(data, data$lead.white, ci_data_white_lead, "White Lead", 0, 1)
g_east_asian_lead=plotter(data, data$lead.east_asian, ci_data_ea_lead, "East Asian Lead", 0, 1)
g_south_asian_lead=plotter(data, data$lead.south_asian, ci_data_sa_lead, "South Asian Lead", 0, 1)

# gender

ci_data_men_lead=read.table("../data/ci/lead men.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_women_lead=read.table("../data/ci/lead women.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")

g_men_lead=plotter(data, data$lead.men, ci_data_men_lead, "Men Lead", 0, 1)
g_women_lead=plotter(data, data$lead.women, ci_data_women_lead, "Women Lead", 0, 1)

## NON-LEADS ##

# race/ethnicity

ci_data_hl_nonlead=read.table("../data/ci/non-lead hispanic_latino.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_black_nonlead=read.table("../data/ci/non-lead black.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_white_nonlead=read.table("../data/ci/non-lead white.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_ea_nonlead=read.table("../data/ci/non-lead east_asian.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_sa_nonlead=read.table("../data/ci/non-lead south_asian.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")


g_hispanic_latino_nonlead=plotter(data, data$non.lead.hispanic_latino, ci_data_hl_nonlead, "Hispanic/Latino Non-lead", 0, 1)
g_black_nonlead=plotter(data, data$non.lead.black, ci_data_black_nonlead, "Black Non-lead", 0, 1)
g_white_nonlead=plotter(data, data$non.lead.white, ci_data_white_nonlead, "White Non-lead", 0, 1)
g_east_asian_nonlead=plotter(data, data$non.lead.east_asian, ci_data_ea_nonlead, "East Asian Non-lead", 0, 1)
g_south_asian_nonlead=plotter(data, data$non.lead.south_asian, ci_data_sa_nonlead, "South Asian Non-lead", 0, 1)

# gender

ci_data_men_nonlead=read.table("../data/ci/non-lead men.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
ci_data_women_nonlead=read.table("../data/ci/non-lead women.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")


g_men_nonlead=plotter(data, data$non.lead.men, ci_data_men_nonlead, "Men Non-lead", 0, 1)
g_women_nonlead=plotter(data, data$non.lead.women, ci_data_women_nonlead, "Women Non-lead", 0, 1)

pdf("race_lead_full.pdf", width=10, height=15)
multiplot(g_black_lead, g_east_asian_lead, g_hispanic_latino_lead, g_south_asian_lead, g_white_lead, g_black_nonlead, g_east_asian_nonlead, g_hispanic_latino_nonlead, g_south_asian_nonlead, g_white_nonlead, cols=2)
dev.off()


g_hispanic_latino_lead=plotter(data, data$lead.hispanic_latino, ci_data_hl_lead, "Hispanic/Latino Lead", 0, .25)
g_black_lead=plotter(data, data$lead.black, ci_data_black_lead, "Black Lead", 0, .25)
g_white_lead=plotter(data, data$lead.white, ci_data_white_lead, "White Lead", 0, 1)
g_east_asian_lead=plotter(data, data$lead.east_asian, ci_data_ea_lead, "East Asian Lead", 0, .25)
g_south_asian_lead=plotter(data, data$lead.south_asian, ci_data_sa_lead, "South Asian Lead", 0, .25)


g_hispanic_latino_nonlead=plotter(data, data$non.lead.hispanic_latino, ci_data_hl_nonlead, "Hispanic/Latino Non-lead", 0, .25)
g_black_nonlead=plotter(data, data$non.lead.black, ci_data_black_nonlead, "Black Non-lead", 0, .25)
g_white_nonlead=plotter(data, data$non.lead.white, ci_data_white_nonlead, "White Non-lead", 0, 1)
g_east_asian_nonlead=plotter(data, data$non.lead.east_asian, ci_data_ea_nonlead, "East Asian Non-lead", 0, .25)
g_south_asian_nonlead=plotter(data, data$non.lead.south_asian, ci_data_sa_nonlead, "South Asian Non-lead", 0, .25)


pdf("race_lead.pdf", width=10, height=15)
multiplot(g_black_lead, g_east_asian_lead, g_hispanic_latino_lead, g_south_asian_lead, g_white_lead, g_black_nonlead, g_east_asian_nonlead, g_hispanic_latino_nonlead, g_south_asian_nonlead, g_white_nonlead, cols=2)
dev.off()



pdf("gender_lead.pdf", width=10, height=12)
multiplot(g_women_lead, g_men_lead, g_women_nonlead, g_men_nonlead, cols=2)

# ENTROPY
ci_data_entropy=read.table("../data/ci/entropy.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")

pdf("entropy.pdf", width=7)
plotter(data, data$entropy, ci_data_entropy, "Entropy", 0, 0.7)
dev.off()



# AWARDS

awards=read.table("../data/awards.tsv", sep="\t", quote = "", head=TRUE, na.strings="NA", comment.char = "")
black_awards=awards[!is.na(awards$black),]
ci_data_awards_black=read.table("../data/ci/black.awards.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")

pdf("black_award.pdf", width=7)
plotter(black_awards, black_awards$black, ci_data_awards_black, "% Facetime, Black actors", 0, 0.25)
dev.off()





