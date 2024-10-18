library(data.table)
library(ggplot2)

data=read.table("../data/leads.txt")

dt1=data[data$V1=="lead",]
dt2=data[data$V1=="nonlead",]

combined_dt <- rbindlist(list("lead" = dt1, "non-lead" = dt2), idcol = "group")

pdf("leadvnonlead.pdf", width=9)

ggplot(combined_dt, aes(x = V2, fill = group)) +
  geom_density(alpha = 0.5) +
  scale_fill_manual(values = c("blue", "red")) +
  labs(x = "facetime", y = "density") + guides(fill = guide_legend(title = NULL)) + xlim(0,1) + theme(legend.position="top") + theme_classic() + geom_vline(xintercept = seq(0,1, by = .1), linetype = "dotdash", size=.2, color = "grey", alpha = .5) + geom_hline(yintercept = seq(0, 15, by = 1), linetype = "dotdash", size=.2, color = "grey", alpha = 0.5)  +
theme(
      axis.title.x = element_text(size = 16),  # X axis title size
      axis.title.y = element_text(size = 16),  # Y axis title size
      axis.text.x = element_text(size = 14),   # X axis text size
      axis.text.y = element_text(size = 14)    # Y axis text size
    )
dev.off()
