
library(stats);

cs = read.csv("./collected_stats.csv");

# Manually filter some stats
cs = cs[-which(endsWith(cs$url, "#comments")), ];

summary(cs);

statnames = colnames(cs)[3:ncol(cs)];

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

trainDensitites = function(train, do.plot=FALSE) {
  stat_densities = list()

  # Compute the kernel density estimation for all different stats
  for(sn in statnames) {
    # cosine kernel because it is smoother than the gaussian kernel
    stat_densities[[sn]] = density(train[[sn]], kernel="cosine", n=1024, cut=30, na.rm=TRUE);
    
    if(do.plot) {
      xlim = range(stat_densities[[sn]]$x, na.rm=TRUE) + 0.3*c(-1, 1)*sum(c(-1, 1)*range(stat_densities[[sn]]$x, na.rm=TRUE));
      hist(train[[sn]], freq=FALSE, breaks=30, xlim=xlim, main=sn, xlab=sn);
      lines(stat_densities[[sn]]$x, stat_densities[[sn]]$y, col='red');
      
      score_func = getScoreFunction(stat_densities[[sn]]);
      lines(score_func$x, score_func$y * max(stat_densities[[sn]]$y), type='l', col='blue');
      legend("topright", legend=c("Estim. Kernel Dens.", "Scoring Function"), fill=c('red', 'blue'));
    }
    # plot(score_func$x, score_func$y, 'l', main=paste("Scoring values", sn), xlab=sn, ylab="score");
  }
  
  return (stat_densities);
}

getTestScores = function(stat_densities, test_stats) {
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


baselineCV = function(test.folds) {
  precision = c();
  recall = c();
  for(tf in test.folds) {
    tp = sum(tf$groundtruth == "generated" & tf$bl.genuinety == "generated"); # true positives
    fp = sum(tf$bl.genuinety == "generated") - tp; # false positives
    fn = sum(tf$groundtruth == "generated" & tf$bl.genuinety == "real"); # false negatives
    precision = c(precision, tp/(tp+fp));
    print(paste("Precision:", tp, "/", tp+fp, "=", tp/(tp+fp)));
    # NOTE: precision and recall are the same in our binary classification case
  }
  return (mean(precision));
}

evaluateCV = function(test.folds) {
  precision = c();
  recall = c();
  for(tf in test.folds) {
    tp = sum(tf$groundtruth == "generated" & tf$genuinety == "generated"); # true positives
    fp = sum(tf$genuinety == "generated") - tp; # false positives
    fn = sum(tf$groundtruth == "generated" & tf$genuinety == "real"); # false negatives
    precision = c(precision, tp/(tp+fp));
    print(paste("Precision:", tp, "/", tp+fp, "=", tp/(tp+fp)));
    # NOTE: precision and recall are the same in our binary classification case
  }
  return (mean(precision));
}


evaluation_stats = read.csv("./evaluation_stats.csv");
precisions = list()


# k-fold Cross Validation of collected_stats against nbc news
es = evaluation_stats[startsWith(evaluation_stats$url, "https://www.nbcnews.com/"), ]
es = es[1:min(nrow(es), 40), ];

set.seed(13);
k = round(nrow(cs) / ((3/2) * nrow(es)));
folds = sample(k, nrow(cs), replace=TRUE);
test.folds = list()
for(foldIx in 1:k) {
  train = cs[folds != foldIx, ];
  test = rbind(cs[folds == foldIx, ], es);
  test$groundtruth = factor(c(rep("real", nrow(cs[folds == foldIx, ])), rep("generated", nrow(es))), levels=c("real", "generated"));
  
  stat_densities = trainDensitites(train);
  test[is.na(test)] = 0;
  scores = getTestScores(stat_densities, test);
  
  weights = rep(1, length(statnames));
  weights = setNames(weights, statnames);
  # discard stats where we have NaN values for more than 20% of the entries
  weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$scores = rowSums(scores * weights);
  
  score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
  test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

  
  bl.weights = rep(0, length(statnames));
  bl.weights = setNames(bl.weights, statnames);
  # only use the WFProp stats for the baseline
  bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
  # discard stats where we have NaN values for more than 20% of the entries
  bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$bl.scores = rowSums(scores * bl.weights);
  
  bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
  test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  test.folds[[foldIx]] = test; # store the resulting dataframe in a list for evaluation
}
precisions[['CVNBCNews']] = evaluateCV(test.folds);
precisions[['BLCVNBCNews']] = baselineCV(test.folds);





# k-fold Cross Validation of collected_stats against sciencedaily
es = evaluation_stats[startsWith(evaluation_stats$url, "https://www.sciencedaily.com/"), ]
es = es[1:min(nrow(es), 40), ];

set.seed(13);
k = round(nrow(cs) / ((3/2) * nrow(es)));
folds = sample(k, nrow(cs), replace=TRUE);
test.folds = list()
for(foldIx in 1:k) {
  train = cs[folds != foldIx, ];
  test = rbind(cs[folds == foldIx, ], es);
  test$groundtruth = factor(c(rep("real", nrow(cs[folds == foldIx, ])), rep("generated", nrow(es))), levels=c("real", "generated"));

  stat_densities = trainDensitites(train);
  test[is.na(test)] = 0;
  scores = getTestScores(stat_densities, test);

  weights = rep(1, length(statnames));
  weights = setNames(weights, statnames);
  # discard stats where we have NaN values for more than 20% of the entries
  weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$scores = rowSums(scores * weights);
  
  score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
  test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  
  bl.weights = rep(0, length(statnames));
  bl.weights = setNames(bl.weights, statnames);
  # only use the WFProp stats for the baseline
  bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
  # discard stats where we have NaN values for more than 20% of the entries
  bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$bl.scores = rowSums(scores * bl.weights);
  
  bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
  test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  test.folds[[foldIx]] = test; # store the resulting dataframe in a list for evaluation
}
precisions[['CVScienceDaily']] = evaluateCV(test.folds);
precisions[['BLCVScienceDaily']] = baselineCV(test.folds);



# k-fold Cross Validation of collected_stats against pcmag articles
es = evaluation_stats[startsWith(evaluation_stats$url, "https://uk.pcmag.com/"), ]
es = es[1:min(nrow(es), 40), ];

set.seed(13);
k = round(nrow(cs) / ((3/2) * nrow(es)));
folds = sample(k, nrow(cs), replace=TRUE);
test.folds = list()
for(foldIx in 1:k) {
  train = cs[folds != foldIx, ];
  test = rbind(cs[folds == foldIx, ], es);
  test$groundtruth = factor(c(rep("real", nrow(cs[folds == foldIx, ])), rep("generated", nrow(es))), levels=c("real", "generated"));
  
  stat_densities = trainDensitites(train);
  test[is.na(test)] = 0;
  scores = getTestScores(stat_densities, test);
  
  weights = rep(1, length(statnames));
  weights = setNames(weights, statnames);
  # discard stats where we have NaN values for more than 20% of the entries
  weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$scores = rowSums(scores * weights);
  
  score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
  test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  
  bl.weights = rep(0, length(statnames));
  bl.weights = setNames(bl.weights, statnames);
  # only use the WFProp stats for the baseline
  bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
  # discard stats where we have NaN values for more than 20% of the entries
  bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$bl.scores = rowSums(scores * bl.weights);
  
  bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
  test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  test.folds[[foldIx]] = test; # store the resulting dataframe in a list for evaluation
}
precisions[['CVPCMag']] = evaluateCV(test.folds);
precisions[['BLCVPCMag']] = baselineCV(test.folds);


# k-fold Cross Validation of collected_stats against medium articles
es = read.csv("./../data/eval/MediumArticles/test_stats.csv");

set.seed(13);
k = round(nrow(cs) / ((3/2) * nrow(es)));
folds = sample(k, nrow(cs), replace=TRUE);
test.folds = list()
for(foldIx in 1:k) {
  train = cs[folds != foldIx, ];
  test = rbind(cs[folds == foldIx, ], es);
  test$groundtruth = factor(c(rep("real", nrow(cs[folds == foldIx, ])), rep("generated", nrow(es))), levels=c("real", "generated"));
  
  stat_densities = trainDensitites(train);
  test[is.na(test)] = 0;
  scores = getTestScores(stat_densities, test);
  
  weights = rep(1, length(statnames));
  weights = setNames(weights, statnames);
  # discard stats where we have NaN values for more than 20% of the entries
  weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$scores = rowSums(scores * weights);
  
  score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
  test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  
  bl.weights = rep(0, length(statnames));
  bl.weights = setNames(bl.weights, statnames);
  # only use the WFProp stats for the baseline
  bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
  # discard stats where we have NaN values for more than 20% of the entries
  bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
  test$bl.scores = rowSums(scores * bl.weights);
  
  bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
  test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));
  
  test.folds[[foldIx]] = test; # store the resulting dataframe in a list for evaluation
}
precisions[['CVMedium']] = evaluateCV(test.folds);
precisions[['BLCVMedium']] = baselineCV(test.folds);





# unseen nbcnews articles against medium articles
# https://www.kaggle.com/datasets/hsankesara/medium-articles
es = read.csv("./../data/eval/MediumArticles/test_stats.csv");

test.folds = list()
train = cs;
test.real = evaluation_stats[startsWith(evaluation_stats$url, "https://www.nbcnews.com/"), ];
test.real = test.real[1:min(nrow(test.real), 60), ];
test = rbind(test.real, es);
test$groundtruth = factor(c(rep("real", nrow(test.real)), rep("generated", nrow(es))), levels=c("real", "generated"));
  
stat_densities = trainDensitites(train);
test[is.na(test)] = 0;
scores = getTestScores(stat_densities, test);
  
weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$scores = rowSums(scores * weights);
  
score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

bl.weights = rep(0, length(statnames));
bl.weights = setNames(bl.weights, statnames);
# only use the WFProp stats for the baseline
bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
# discard stats where we have NaN values for more than 20% of the entries
bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$bl.scores = rowSums(scores * bl.weights);

bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));

test.folds[['NoCV']] = test; # store the resulting dataframe in a list for evaluation
precisions[['Medium']] = evaluateCV(test.folds);
precisions[['BLMedium']] = baselineCV(test.folds);



# unseen nbcnews articles against nips papers
# https://www.kaggle.com/datasets/benhamner/nips-papers
es = read.csv("./../data/eval/NIPSPapers/test_stats.csv");

test.folds = list()
train = cs;
test.real = evaluation_stats[startsWith(evaluation_stats$url, "https://www.nbcnews.com/"), ];
test.real = test.real[1:min(nrow(test.real), 60), ];
test = rbind(test.real, es);
test$groundtruth = factor(c(rep("real", nrow(test.real)), rep("generated", nrow(es))), levels=c("real", "generated"));

stat_densities = trainDensitites(train);
test[is.na(test)] = 0;
scores = getTestScores(stat_densities, test);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$scores = rowSums(scores * weights);

score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

bl.weights = rep(0, length(statnames));
bl.weights = setNames(bl.weights, statnames);
# only use the WFProp stats for the baseline
bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
# discard stats where we have NaN values for more than 20% of the entries
bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$bl.scores = rowSums(scores * bl.weights);

bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));

test.folds[['NoCV']] = test; # store the resulting dataframe in a list for evaluation
precisions[['NIPSPapers']] = evaluateCV(test.folds);
precisions[['BLNIPSPapers']] = baselineCV(test.folds);



# unseen nbcnews articles against wiki movie plots
# https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots
es = read.csv("./../data/eval/WikiMoviePlots/test_stats.csv");

test.folds = list()
train = cs;
test.real = evaluation_stats[startsWith(evaluation_stats$url, "https://www.nbcnews.com/"), ];
test.real = test.real[1:min(nrow(test.real), 60), ];
test = rbind(test.real, es);
test$groundtruth = factor(c(rep("real", nrow(test.real)), rep("generated", nrow(es))), levels=c("real", "generated"));

stat_densities = trainDensitites(train);
test[is.na(test)] = 0;
scores = getTestScores(stat_densities, test);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$scores = rowSums(scores * weights);

score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

bl.weights = rep(0, length(statnames));
bl.weights = setNames(bl.weights, statnames);
# only use the WFProp stats for the baseline
bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
# discard stats where we have NaN values for more than 20% of the entries
bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$bl.scores = rowSums(scores * bl.weights);

bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));

test.folds[['NoCV']] = test; # store the resulting dataframe in a list for evaluation
precisions[['WikiMoviePlot']] = evaluateCV(test.folds);
precisions[['BLWikiMoviePlot']] = baselineCV(test.folds);



# unseen nbcnews articles against data scientist job descriptions
# https://www.kaggle.com/datasets/diegosilvadefrana/2023-data-scientists-jobs-descriptions
es = read.csv("./../data/eval/DataScientistJobDescriptions/test_stats.csv");

test.folds = list()
train = cs;
test.real = evaluation_stats[startsWith(evaluation_stats$url, "https://www.nbcnews.com/"), ];
test.real = test.real[1:min(nrow(test.real), 60), ];
test = rbind(test.real, es);
test$groundtruth = factor(c(rep("real", nrow(test.real)), rep("generated", nrow(es))), levels=c("real", "generated"));

stat_densities = trainDensitites(train);
test[is.na(test)] = 0;
scores = getTestScores(stat_densities, test);

weights = rep(1, length(statnames));
weights = setNames(weights, statnames);
# discard stats where we have NaN values for more than 20% of the entries
weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$scores = rowSums(scores * weights);

score_quantile = quantile(test$scores, probs=c(nrow(es)/nrow(test)));
test$genuinety = factor(ifelse(test$scores <= score_quantile, "generated", "real"), levels=c("real", "generated"));

bl.weights = rep(0, length(statnames));
bl.weights = setNames(bl.weights, statnames);
# only use the WFProp stats for the baseline
bl.weights[which(startsWith(statnames, "WFProp"))] = 1;
# discard stats where we have NaN values for more than 20% of the entries
bl.weights[which(colSums(is.na(test[, statnames])) > (nrow(test)/5))] = 0;
test$bl.scores = rowSums(scores * bl.weights);

bl.score_quantile = quantile(test$bl.scores, probs=c(nrow(es)/nrow(test)));
test$bl.genuinety = factor(ifelse(test$bl.scores <= bl.score_quantile, "generated", "real"), levels=c("real", "generated"));

test.folds[['NoCV']] = test; # store the resulting dataframe in a list for evaluation
precisions[['DSJobDescriptions']] = evaluateCV(test.folds);
precisions[['BLDSJobDescriptions']] = baselineCV(test.folds);



par(mai=c(0.4, 1, 0.4, 0.4));
selected_tests = c('BLCVNBCNews', 'CVNBCNews', 'BLCVScienceDaily', 'CVScienceDaily', 'BLCVPCMag', 'CVPCMag', 'BLCVMedium', 'CVMedium');
selected_tests.names = c('WF NBC', 'NBC', 'WF SD', 'SD', 'WF PCM', 'PCM', 'WF Md', 'Md');
barplot(unlist(precisions[selected_tests]), names.arg=selected_tests.names, ylim = c(0, 1), col=c('lightblue', 'orange', 'lightblue', 'orange', 'lightblue', 'orange', 'lightblue', 'orange'), ylab="Precision");
abline(h=0.4, col='red', lty=2, lwd=2);
text(y=0.45, x=(length(selected_tests)+1)/2, "Random Guessing Baseline", col='red');

par(mai=c(0.4, 1, 0.4, 0.4));
selected_tests = c('BLMedium', 'Medium', 'BLNIPSPapers', 'NIPSPapers', 'BLWikiMoviePlot', 'WikiMoviePlot', 'BLDSJobDescriptions', 'DSJobDescriptions');
selected_tests.names = c('WF Md', 'Md', 'WF NP', 'NP', 'WF WMP', 'WMP', 'WF DSJD', 'DSJD');
barplot(unlist(precisions[selected_tests]), names.arg=selected_tests.names, ylim = c(0, 1), col=c('lightblue', 'orange', 'lightblue', 'orange', 'lightblue', 'orange', 'lightblue', 'orange'), ylab="Precision");
abline(h=0.4, col='red', lty=2, lwd=2);
text(y=0.45, x=(length(selected_tests)+1)/2, "Random Guessing Baseline", col='red');

