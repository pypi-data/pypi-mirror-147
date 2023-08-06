#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.model_selection import cross_val_score, TimeSeriesSplit

__author__ = 'Yuen Shing Yan Hindy'
__license__= 'MIT License'
__contact__ = 'https://github.com/HindyDS/ForwardStepwiseFeatureSelection'

class ForwardStepwiseFeatureSelection:
    def __init__(self, estimators, cv, scoring, mode=None, max_trial=None, tolerance=None, least_gain=None, max_feats=None, prior=None, exclusions=None, n_jobs=-1, n_digit=4, verbose=1):
        self.estimators = estimators
        self.cv = cv
        self.scoring = scoring
        self.mode = mode
        self.max_trial = max_trial
        self.tolerance = tolerance
        self.least_gain = least_gain
        self.max_feats = max_feats
        self.prior = prior
        self.exclusions = exclusions
        self.n_jobs = n_jobs
        self.n_digit = n_digit
        self.verbose = verbose

        self.best_subsets = {}  
        self.summaries = {}
        
    def fit(self, X, y):
        trial_start_time = time.time()
        
        if type(self.estimators) != list:
            self.estimators = [self.estimators]

        for estimator in self.estimators:
            max_trial = self.max_trial
            tolerance = self.tolerance
            max_feats = self.max_feats
            
            best_com = {} # keys:n_trial, val: best_subset
            best_score = {} # keys:n_trial, val: best_score  
            trials_time_spend = {} # keys:n_trial, val: time spent 
            n_trial = 1

            if self.exclusions == None:
                self.exclusions = [[]]
            mainpool = self.exclusions.copy()
            if self.prior != None:
                for feature in self.prior:
                    for subpool in mainpool:
                        if feature in subpool:
                            raise Exception(f'''The feature "{feature}" in self.prior is in one of the subpool from self.exclusions.
                   Please either: 
                   1) Remove {feature} from the corresponding subpool
                   2) Remove {feature} from self.prior or
                   3) Remove corresponding subpool from self.exclusions
                   ''')

            if self.tolerance != None:    
                if self.tolerance < 0 or isinstance(self.tolerance, int) != True:
                    raise Exception('self.tolerance must be positive integer.')
            if self.tolerance == None:
                self.tolerance = 1

            if self.max_trial != None:
                if self.max_trial < 0 or isinstance(self.max_trial, int) != True:
                    raise Exception('self.max_trial must be positive integer.')    
            if self.max_trial == None:
                self.max_trial = 99999999999999

            if self.least_gain != None:
                if least_gain < 0 != True:
                    raise Exception('least_gain must be positive number.')

            if self.max_feats != None:
                if self.max_feats < 0 or isinstance(self.max_feats, int) != True:
                    raise Exception('self.max_feats must be positive integer.')
            if self.max_feats == None:
                self.max_feats = 99999999999999

            if self.prior != None:
                if isinstance(self.prior, list) != True:
                    raise Exception('self.prior must be a list of features.')

            if self.n_digit != None:
                if self.n_digit < 0 or isinstance(self.n_digit, int) != True:
                    raise Exception('self.n_digit must be positive integer.')
            if self.n_digit == None:
                self.n_digit = 9   
            
            estimator_str = str(estimator).split('(')[0]
            
            print(' ')
            if self.verbose >= 2:
                print(f'Searching the best subset of features with {estimator_str}...')
            if self.prior != None:
                print(f'Starting with {self.prior}...')

            if self.prior != None and type(self.prior) != list:   
                print('self.prior only accept list as argument.')
                return 

            if self.prior != None:
                features2 =[]
                if type(self.prior) == list:
                    features = list(X.columns)
                    for f in self.prior:
                        features.remove(f)

                    for feat in features:
                        features2.append(self.prior + [feat])
                features = features2

            if self.prior == None:    
                features = []
                for feature in X.columns:
                    features.append([feature])

            while True:
                start_time = time.time()
                # features as keys, score as values
                feat_com = {}
                if self.verbose > 2:
                    print(f'----------------------------------------------------------Trial {n_trial}----------------------------------------------------------')
                in_trial_count = 1
                # try out all features
                if n_trial == 1 and self.prior == None:
                    for feature in features:
                        if self.mode == 'ts':
                            cv = TimeSeriesSplit(n_splits=self.cv).split(X[feature])
                        else:
                            cv = self.cv

                        cross_val_score_res = cross_val_score(estimator, X[feature], y, cv=cv, scoring=self.scoring, n_jobs=self.n_jobs)
                        score = round(cross_val_score_res.mean(), self.n_digit)
                        std = round(cross_val_score_res.std(), self.n_digit)
                        feat_com[feature[0]] = score
                        self.scoring_str = ' '.join(self.scoring.split('_')).title().replace('Neg', 'Negative').replace('Rand', 'Random').replace('Max', 'Maximum')
                        if self.verbose > 3:
                            print(f'{in_trial_count}/{len(features)}: {feature}')
                            print(f'      {self.scoring_str}: {score}, Standard Deviation: {std}')
                            print(' ')
                        in_trial_count += 1

                if n_trial > 1 or self.prior != None:
                    for feature in features:
                        if self.mode == 'ts':
                            cv = TimeSeriesSplit(n_splits=self.cv).split(X[feature])
                        else:
                            cv = self.cv

                        cross_val_score_res = cross_val_score(estimator, X[feature], y, cv=cv, scoring=self.scoring, n_jobs=self.n_jobs)
                        score = round(cross_val_score_res.mean(), self.n_digit)
                        std = round(cross_val_score_res.std(), self.n_digit)
                        feat_com[tuple(feature)] = score
                        self.scoring_str = ' '.join(self.scoring.split('_')).title().replace('Neg', 'Negative').replace('Rand', 'Random').replace('Max', 'Maximum')
                        if self.verbose >= 3:
                            print(f'{in_trial_count}/{len(features)}: {feature}')
                            print(f'      {self.scoring_str}: {score}, Standard Deviation: {std}')
                            print(' ')
                        in_trial_count += 1

                # pick the and store trial best
                best_com[f'Trial {n_trial}'] = max(feat_com, key=feat_com.get)
                best_score[f'Trial {n_trial}'] = max(feat_com.values())

                # define the current trial best
                curr_trial_best = best_com[f'Trial {n_trial}']

                if n_trial == 1 and self.prior == None:
                    # features without the selected trial best
                    features.remove([curr_trial_best])
                    # generating new Subsets of features
                    features = [[curr_trial_best]+[i][0] for i in features]

                if n_trial > 1 or self.prior != None:
                    curr_trial_best2 = list(best_com.values())
                    features.remove(list(curr_trial_best2[n_trial-1]))
                    if type(curr_trial_best2[n_trial-2]) == tuple:

                        for feature in features:
                            for f in list(curr_trial_best2[n_trial-2]):
                                try:
                                    feature.remove(f)  
                                except:
                                    continue

                    if type(curr_trial_best2[n_trial-2]) == str:
                        for feature in features:
                            feature.remove(curr_trial_best2[n_trial-2])
                    features2 = []
                    for feature in features:
                        features2.append(list(curr_trial_best2[n_trial-1])+feature)

                    features = features2

                if mainpool != None:                                 # for pool elimination
                    for subpool in mainpool:
                        if curr_trial_best[-1] in subpool:       # if new added feature in any of the subpool, remove it from the subpool
                            subpool.remove(curr_trial_best[-1])
                            for feature in features:             # remove the rest of the features of the subpool from the subsets
                                for p in subpool:
                                    try:
                                        feature.remove(p)
                                    except:
                                        continue

                        for feature in features:                 # remove dups in nested list (features)
                            index = []
                            for i in range(len(features)):
                                if feature == features[i]:
                                    index.append(i)

                            index = index[-(features.count(feature) - 1):]

                            count = 0
                            for idx in index:
                                if features.count(feature) >1:
                                    del features[idx - count]
                                count += 1

                        index = []                               # remove unmatched length subset
                        for idx, feature in enumerate(features):
                            if self.prior != None:
                                if len(feature) != n_trial + 1 + len(self.prior):
                                    index.append(idx)

                            if self.prior == None:
                                if len(feature) != n_trial + 1:
                                    index.append(idx)

                        count = 0
                        for idx in index:
                            del features[idx - count]
                            count += 1

                curr_key = f'Trial {n_trial}'
                last_key = f'Trial {n_trial - 1}'

                if last_key != 'Trial 0':
                    if self.least_gain == None:
                        if best_score[curr_key] < best_score[last_key]:  # if fail to improve score, then take away one chance
                            self.tolerance = self.tolerance - 1
                            if self.verbose > 2:
                                print(f'Failed to improve {self.scoring_str}.')
                    if self.least_gain != None:                                         # if fail to improve score by a certain percentage, then take away one chance
                        if (best_score[curr_key] - best_score[last_key])/best_score[last_key] < least_gain:
                            self.tolerance = self.tolerance - 1
                            if self.verbose > 2:
                                print(f'Failed to improve {self.scoring_str} by {least_gain * 100}%.')
                            
                if self.verbose >= 3:
                    print(f'Best Subset Found in Trial {n_trial}: ')
                    if type(best_com[f'Trial {n_trial}']) == str:
                        print('    ',best_com[f'Trial {n_trial}'])

                    if type(best_com[f'Trial {n_trial}']) == tuple:
                        print('    ',list(best_com[f'Trial {n_trial}']))
                    print(' ')
                    print(f'Best {self.scoring_str} of Trial {n_trial}: ')
                    print('    ',best_score[f'Trial {n_trial}'])
                    print(' ')
                
                n_trial += 1
                self.max_trial = self.max_trial - 1

                end_time = time.time()
                
                trials_time_spend[f'Trial {n_trial - 1}'] = round(end_time - start_time, 2)
                if self.verbose > 2:
                    print(f"Time Spent for Trial {n_trial - 1}: {round(end_time - start_time, 2)}(s)")
                    print(' ')

                if self.tolerance <= 0:           
                    if self.verbose > 2:
                        print('Fail self.tolerance exceeded.')
                        print('Trial stops.')
                    break
                if self.max_trial <= 0:
                    if self.verbose > 2:
                        print('Round maximum reached.')
                        print('Trial stops.')
                    break
                if len(features) <= 0:
                    if self.verbose > 2:
                        print('All features subsets have been tried out.')
                    break
                if self.max_feats == n_trial - 1:
                    if self.verbose >= 2:
                        print(f'Top {self.max_feats} features have been selected.')
                    break    

            best_com2 = {}
            temp_list = []
            for key, val in best_com.items():
                if type(val) == str:
                    temp_list.append(val)
                    best_com2[key] = temp_list
                else:
                    best_com2[key] = list(val)

            best_com = best_com2
            self.summary = pd.DataFrame([best_com, best_score, trials_time_spend], 
                                        index=['Best Subset', f'Best {self.scoring_str}', 'Time Spent']).T
            
            best_subset = self.summary.sort_values(f'Best {self.scoring_str}', ascending=False).iloc[0, 0]
            best_score_all = max(self.summary.iloc[:, 1])
                
            self.summaries[estimator_str] = self.summary
            self.best_subsets[estimator_str] = best_subset               
            
            # store the result
            if self.verbose >= 2:
                print(f'--------------------------------------------------------Trial Summary--------------------------------------------------------')
            try:
                if self.verbose >= 2:
                    print(f'Best Subset Found: ')
                    print('    ',best_subset)
                    print(' ')
                    print(f'Best {self.scoring_str}: ')
                    print('    ',best_score_all)
                    print(' ')
            except:
                if self.verbose >= 2:
                    n_trial = n_trial - 1
                    print(f'Best Subset Found: ')
                    print('    ',best_subset)
                    print(' ')
                    print(f'Best {self.scoring_str}: ')
                    print('    ',best_score_all)
                    print(' ')
                
            trial_end_time = time.time()
            print(f"Total Time Spent: {round(trial_end_time - trial_start_time, 2)}(s)")
            
            if self.verbose > 0:
                # visualizing the trials
                sns.set_theme()
                fig, ax = plt.subplots(figsize=(15, 6))  
                #sns.lineplot(x=[i + 1 for i in range(len(best_com.keys()))], y=best_score.values(), markers=True)
                plt.plot(self.summary[f'Best {self.scoring_str}'], marker='o')
                plt.axvline(x = np.argmax(list(best_score.values())), color='black', linewidth=2, linestyle='--')
                plt.ylabel(f'{self.scoring_str}')
                plt.xlabel('Subsets')
                n_f = len(self.summary['Best Subset'].iloc[np.argmax(self.summary[f'Best {self.scoring_str}'])])
                plt.legend([f'Best {self.scoring_str}', f'n_features = {n_f}'])
                plt.title(f'Best {self.scoring_str} reached of each trial ({estimator_str})'.title())
                sns.despine();
                plt.show()
                print(f'--------------------------------End of Forward Stepwise Feature Selection Features Selection ({estimator_str})-------------------------------')
    
    def template(self):
        print(
            '''
            .search(self.estimators=estimator, 
           X=X_train, 
           y=y_train, 
           cv=5, 
           self.scoring=self.scoring, 
           self.max_trial=None, 
           self.tolerance=1, 
           least_gain=None,
           self.prior=None,
           self.exclusions=None,
           self.n_digit=4, 
           self.verbose=4)
           '''
        )
