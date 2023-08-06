# <img src="https://raw.githubusercontent.com/HindyDS/ForwardStepwiseFeatureSelection/main/logo/RFS%2010.5.2021.png" height="277">

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![PyPI version](https://badge.fury.io/py/RecursiveFeatureSelector.svg)](https://badge.fury.io/py/RecursiveFeatureSelector)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

ForwardStepwiseFeatureSelection aims to select the best features or the subset of features in machine learning tasks according to corresponding score with other incredible packages like numpy, pandas and sklearn.

This package is inspired by: 
PyData DC 2016 | A Practical Guide to Dimensionality Reduction 
Vishal Patel
October 8, 2016

- **Examples:** https://github.com/HindyDS/ForwardStepwiseFeatureSelection/tree/main/examples
- **Email:** hindy888@hotmail.com
- **Source code:** https://github.com/HindyDS/ForwardStepwiseFeatureSelection/tree/main/ForwardStepwiseFeatureSelection
- **Bug reports:** https://github.com/HindyDS/ForwardStepwiseFeatureSelection/issues

It requires at least six arguments to run:

- estimators: machine learning model
- X (array): features space
- y (array): target
- cv (int): number of folds in a (Stratified)KFold
- scoring (str): see https://scikit-learn.org/stable/modules/model_evaluation.html

Optional arguments:
- max_trial (int): number of trials that you wanted RFS to stop searching
- tolerance (int): how many times RFS can fail to find better subset of features 
- least_gain (int): threshold of scoring metrics gain in fraction 
- max_feats (int): maximum number of features
- prior (list): starting point for RFS to search, must be corresponds to the columns of X
- exclusions (nested list): if the new selected feature is in one of the particular subpool 
		    (list in the nested list), then the features in that particular subpool with no 			    longer be avalible to form any new subset in the following trials
- n_jobs (int): Number of jobs to run in parallel.
- n_digit (int): Decimal places for scoring
- verbose (int): Level of verbosity of RFS

If you have any ideas for this packge please don't hesitate to bring forward!