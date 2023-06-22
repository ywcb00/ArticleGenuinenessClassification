
library(stats);

cs = read.csv("./collected_stats.csv");

# Manually filter some stats
cs = cs[-which(endsWith(cs$url, "#comments")), ];

summary(cs);

statnames = colnames(cs)[3:ncol(cs)];

stat_densities = list()

scoreTransform = function(data, density) {
  scoring_densitites = log2(1 + (data / max(density$y))^{1/4});
  return (scoring_densitites);
}

movingAverage = function(data, n=48) {
  averaged_data = stats::filter(data, rep(1/n, n))
}

getScoreFunction = function(stat_dens) {
  score = scoreTransform(stat_dens$y, stat_dens);
  score = movingAverage(score);
  score[is.na(score)] = 0;
  return (list(x=stat_dens$x, y=score));
}

# Compute the kernel density estimation for all different stats
for(sn in statnames) {
  # cosine kernel because it is smoother than the gaussian kernel
  stat_densities[[sn]] = density(cs[[sn]], kernel="cosine", n=1024, cut=30, na.rm=TRUE);

  xlim = range(stat_densities[[sn]]$x, na.rm=TRUE) + 0.3*c(-1, 1)*sum(c(-1, 1)*range(stat_densities[[sn]]$x, na.rm=TRUE));
  hist(cs[[sn]], freq=FALSE, breaks=30, xlim=xlim, main=sn, xlab=sn);
  lines(stat_densities[[sn]]$x, stat_densities[[sn]]$y, col='red');

  score_func = getScoreFunction(stat_densities[[sn]]);
  lines(score_func$x, score_func$y * max(stat_densities[[sn]]$y), type='l', col='blue');
  legend("topright", legend=c("Estim. Kernel Dens.", "Scoring Function"), fill=c('red', 'blue'));
  
  # plot(score_func$x, score_func$y, 'l', main=paste("Scoring values", sn), xlab=sn, ylab="score");
}

getTestScores = function(test_stats) {
  scores = data.frame(matrix(ncol=0, nrow=nrow(test_stats)));
  for(sn in statnames) {
    nearest_x = c();
    for(counter in 1:nrow(test_stats)) {
      nearest_x = c(nearest_x, which.min(abs(stat_densities[[sn]]$x - test_stats[[sn]][counter])));
    }
    # density_val = stat_densities[[sn]]$y[nearest_x];
    # scores[[sn]] = scoreTransform(density_val, stat_densities[[sn]]);
    scores[[sn]] = getScoreFunction(stat_densities[[sn]])$y[nearest_x];
  }
  return (scores);
}

plotTestData = function(test_stats, weights, groupname="G") {
  for(sn in statnames) {
    score_func = getScoreFunction(stat_densities[[sn]]);
    plot(score_func$x, score_func$y, 'l', main=paste(groupname,"Test Data Plot", sn), xlab=sn, ylab="score", col='blue');
    abline(v=test_stats[[sn]], col=test_stats$genuinety, lwd=test_stats$genuinety);
    legend("topright", legend=c("Scoring Function", "Predicted Real", "Predicted Generated"), fill=c('blue', 'black', 'red'));
    mtext(paste("Weight:", weights[[sn]]));
  }
}

# Only for testing purposes
# test_stats = cs[500:520, ];

solutions = data.frame();

# Group 19
group_id = 19;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/team-red-19-articles/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No title
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 7
group_id = 7;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/Group7-texts/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# Even though some articles might have a title (first sentence), we ignore the title stats here
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 8
group_id = 8;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/red8-texts/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 2
group_id = 2;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/TeamRed2/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0; # remove stats which contain NaN

# The articles have paragraphs or sentence splits --> keeping the paragraph stats
# Some no titles but the others well defined --> keeping the title stats

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 4
group_id = 4;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/red_group_4_texts/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 29
group_id = 29;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/group_29_submission/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 40
group_id = 40;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/teamRed40_files/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 17
group_id = 17;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/Group17-news/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 13
group_id = 13;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/Team_Red_13_-_Texts/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# There are paragraphs
# About 40% of the articles have no title --> discard the title statistics
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 18
group_id = 18;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/TeamRed18_Dataset/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs (only the last few articles have nice paragraphs)
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 5
group_id = 5;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/Group5-results/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs (only the first 60 articles have nice paragraphs)
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 21
group_id = 21;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/group_red_21/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# No titles
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 1
group_id = 1;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/Group1Red/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# No paragraphs (only very few have paragraphs)
weights[which(startsWith(statnames, "Par"))] = 0;
weights[which(startsWith(statnames, "NER"))] = 0;
weights[which(startsWith(statnames, "NER"))[1:10]] = 1; # keep NER 0-9 (do not depend on paragraphs)
weights[which(startsWith(statnames, "PoSTag"))] = 0;
weights[which(startsWith(statnames, "PoSTag"))[1:12]] = 1; # keep PoSTag 0-12 (do not depend on paragraphs)
weights[which(startsWith(statnames, "SAS"))] = 0;
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "TCCom"))[1]] = 1; # keep TCCom 0 (does not depend on paragraphs)
# Almost all articles have titles --> incooperate title stats

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);



# Group 10
group_id = 10;
groupname = paste("G", group_id, sep='');
print(paste("===", "Testing articles from", groupname))
test_stats = read.csv('./../data/test/Group10-text_files/test_stats.csv');

imputed_test_stats = test_stats;
imputed_test_stats[is.na(imputed_test_stats)] = 0;

test_scores = getTestScores(imputed_test_stats);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test_stats[, statnames])) > (nrow(test_stats)/5))] = 0;

# Only few articles without paragraphs
# Some articles have no title
weights[which(startsWith(statnames, "TCCom"))] = 0;
weights[which(startsWith(statnames, "NPTCCom"))] = 0;

weighted_scores = rowSums(test_scores * weights);

test_stats$scores = weighted_scores;
score_quantile = quantile(weighted_scores, probs=c(0.4));
test_stats$genuinety = factor(ifelse(weighted_scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

print("Articles classified as generated:")
print(test_stats$url[test_stats$genuinety == "generated"]);

plotTestData(test_stats, weights, groupname);

group_sol = data.frame(group_id=rep(group_id, nrow(test_stats)), file_id=test_stats$url, prediction=as.numeric(test_stats$genuinety == "generated"));
solutions = rbind(solutions, group_sol);


solutions$file_id = gsub("\\..*","", solutions$file_id);
write.csv(solutions, "solutions.csv", row.names=FALSE);

