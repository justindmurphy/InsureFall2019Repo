install.packages("AER")
library(AER)
install.packages("foreign")
library(foreign)

# rdd for RDestimate
install.packages("rdd")
library(rdd)
install.packages("stargazer")
library(stargazer)

# rddtools is for rdd_data
install.packages("rddtools")
library(rddtools)
install.packages("lme4")
library(lme4)
install.packages("rdrobust")
library(rdrobust)

# import data set
library(readr)
FULL_RDD_DATASET_FINAL_30DAYS <- read_csv("C:/Users/JDMpc/Desktop/PASER-Insure/FULL_RDD_DATASET_FINAL_30DAYS.csv")
View(FULL_RDD_DATASET_FINAL_30DAYS)

# checking linear models for comparison with lmer models
rdd1=lm(COMMIT_SIZE ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + AGE_AT_TRAVIS + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS)
summary(rdd1)
anova(rdd1)
rdd2=lm(BUG_COUNT ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + AGE_AT_TRAVIS + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS)
summary(rdd2)
anova(rdd2)
rdd3=lm(SEC_COUNT ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + AGE_AT_TRAVIS + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS)
summary(rdd3)
anova(rdd3)


# lmertest and anova tables
# commit_size
summary(lmerTest::lmer(COMMIT_SIZE ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + (1|AGE_AT_TRAVIS) + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS))
anova(lmerTest::lmer(COMMIT_SIZE ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + (1|AGE_AT_TRAVIS) + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS))
# bug count
summary(lmerTest::lmer(BUG_COUNT ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + (1|AGE_AT_TRAVIS) + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS))
anova(lmerTest::lmer(BUG_COUNT ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + (1|AGE_AT_TRAVIS) + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS))
# sec count
summary(lmerTest::lmer(SEC_COUNT ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + (1|AGE_AT_TRAVIS) + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS))
anova(lmerTest::lmer(SEC_COUNT ~ TIME_INDEX + INTERVENTION_FLAG + TIME_AFTER_INTERVENTION + log(REPO_DEV_COUNT) + (1|AGE_AT_TRAVIS) + log(REPO_COMMIT_COUNT), data=FULL_RDD_DATASET_FINAL_30DAYS))

# plots for commit size
plot1=RDestimate(COMMIT_SIZE ~ TIME_INDEX, data=FULL_RDD_DATASET_FINAL_30DAYS, cutpoint = 30)
plot(plot1)
rdplot(FULL_RDD_DATASET_FINAL_30DAYS$COMMIT_SIZE, FULL_RDD_DATASET_FINAL_30DAYS$TIME_INDEX, c = 30, x.label="TIME_INDEX", y.label="COMMIT_SIZE")

# plots for bug count
plot2=RDestimate(BUG_COUNT ~ TIME_INDEX, data=FULL_RDD_DATASET_FINAL_30DAYS, cutpoint = 30)
plot(plot2)
rdplot(FULL_RDD_DATASET_FINAL_30DAYS$BUG_COUNT, FULL_RDD_DATASET_FINAL_30DAYS$TIME_INDEX, c = 30, x.label="TIME_INDEX", y.label="BUG_COUNT")

# security bug count plots have errors due to insufficient data.  Has to do with there only being zeros on one side of the cutpoint
#plot3=RDestimate(SEC_COUNT ~ TIME_INDEX, data=FULL_RDD_DATASET_FINAL_30DAYS, cutpoint = 30)
#plot(plot3)
#rdplot(FULL_RDD_DATASET_FINAL_30DAYS$SEC_COUNT, FULL_RDD_DATASET_FINAL_30DAYS$TIME_INDEX, c = 30, x.label="TIME_INDEX", y.label="SEC_COUNT")
