library(ggplot2)

plotter <- function(data, dem, boot_intervals, ylabel, ymin_val, ymax_val) {
 
  # Plot
  g=ggplot(data=data, aes(y=dem, x=year)) + 

    # plot original points
    theme_classic() +

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


data=read.table("../data/top50.tsv", sep="\t", quote = "", head=TRUE, na.strings="None", comment.char = "")
lauzen=read.table("../data/lauzen_protag.txt", sep="\t", head=TRUE)
ci_data_women=read.table("../data/ci/women.res.txt", sep="\t", quote = "", head=FALSE, na.strings="None", comment.char = "")
g_women=plotter(data, data$women, ci_data_women, "% Facetime, Women", 0, 1)


pdf("gender_comp_lauzen.pdf", width=6)
g_women + geom_point(data=lauzen, aes(x=lauzen$year, y=lauzen$major), col='red') + geom_point(data=lauzen, aes(x=lauzen$year, y=lauzen$speaking), col='purple') +
theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 16),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )
dev.off()


