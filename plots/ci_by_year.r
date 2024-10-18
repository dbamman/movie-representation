library(ggplot2)

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


data=read.table("../data/ci_by_year.txt", sep="\t")
black=data[data$V1 == "black",]
black_ci=ggplot(black) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,0.35) + ylab("Black") + theme_classic() + geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)  + theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )


east_asian=data[data$V1 == "east_asian",]
east_asian_ci=ggplot(east_asian) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,0.35) + ylab("East Asian") + theme_classic() +geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)  +theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )

hispanic_latino=data[data$V1 == "hispanic_latino",]
hispanic_latino_ci=ggplot(hispanic_latino) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,0.35) + ylab("Hispanic/Latino") + theme_classic() +geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)   +theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )

south_asian=data[data$V1 == "south_asian",]
south_asian_ci=ggplot(south_asian) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,0.35) + ylab("South Asian") + theme_classic() +geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)   + theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )

white=data[data$V1 == "white",]
white_ci=ggplot(white) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,1) + ylab("White") + theme_classic() + geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)   + theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )

men=data[data$V1 == "men",]
men_ci=ggplot(men) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,1) + ylab("Men") + theme_classic() + geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)   + theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )

women=data[data$V1 == "women",]
women_ci=ggplot(women) + geom_point(aes(x=V2, y=V3)) + geom_errorbar(aes(x=V2, ymin=V4, ymax=V5, width=0.5)) + xlab("") + ylim(0,1) + ylab("Women") + theme_classic() + geom_vline(xintercept = seq(1980,2020, by = 10), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 1, by = .05), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)   + theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 20),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )


pdf("row1_ci.pdf", width=21)
multiplot(black_ci, east_asian_ci, hispanic_latino_ci, cols=3)
dev.off()

pdf("row2_ci.pdf", width=14)
multiplot(south_asian_ci, white_ci, cols=2)
dev.off()

pdf("gender_ci.pdf", width=14)
multiplot(women_ci, men_ci, cols=2)
dev.off()

suppressWarnings({

cor_test_result=cor.test(black$V2, black$V3, method=c("spearman"))
print(paste("black", cor_test_result$estimate, cor_test_result$p.value))

cor_test_result=cor.test(east_asian$V2, east_asian$V3, method=c("spearman"))
print(paste("east_asian", cor_test_result$estimate, cor_test_result$p.value))

cor_test_result=cor.test(hispanic_latino$V2, hispanic_latino$V3, method=c("spearman"))
print(paste("hispanic_latino", cor_test_result$estimate, cor_test_result$p.value))

cor_test_result=cor.test(south_asian$V2, south_asian$V3, method=c("spearman"))
print(paste("south_asian", cor_test_result$estimate, cor_test_result$p.value))

cor_test_result=cor.test(white$V2, white$V3, method=c("spearman"))
print(paste("white", cor_test_result$estimate, cor_test_result$p.value))

cor_test_result=cor.test(women$V2, women$V3, method=c("spearman"))
print(paste("women", cor_test_result$estimate, cor_test_result$p.value))

cor_test_result=cor.test(men$V2, men$V3, method=c("spearman"))
print(paste("men", cor_test_result$estimate, cor_test_result$p.value))

})