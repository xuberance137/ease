EASE
====

Overview
---------------------
This is a repo with functions that can score arbitrary free text and numeric predictors.
This is licensed under the AGPL, please see LICENSE.txt for details.
The goal here is to provide a high-performance, scalable solution that can predict targets from arbitrary values.

Note that this is the basic library code modified from the original EASE algorithm implementation as part of edx-lra.

To run sample on kaggle training and test set, run 

$python ease/run_EASE.py

Detail documentation of the algorithm used, parameters set for tuning and system description is placed in the pages document at docs/

Sample Output
---------------------

Importing TSV to CSV

Importing CSV to JSON

Loading CSV to Pandas DataFrame

Initializing Test Scoring Object

Loading Data for Test Scoring Setup

Total number of data points as input:  17207

Model Creation

Overall Features Size:  (50, 505)

Feature Set Size (50, 505)

Score Set Size 50

Prediction Set Size 50

model score input :  [0, 2, 1, 0, 0, 1, 0, 0, 1, 3, 1, 0, 1, 0, 0, 1, 3, 2, 0, 1, 0, 0, 2, 0, 2, 0, 2, 1, 1, 0, 0, 1, 2, 3, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 2, 3, 3, 2, 1]

model prediction  :  [1, 2, 0, 0, 0, 1, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 2, 0, 2, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]

model KAPPA       :  0.30404523706

model MAE         :  0.8

Writing Feature Data

Model Based Grading

Overall Features Size:  (1, 505)

grader text input :  Pandas & Koalas are similar because they are both specialist who mostly eat herbs. But both of these species are different from pythons because Pandas and Koalas aren't as dangerous and they don't live in the everglades. Also pandas can live in arid weather and pythons can not.

grader score      :  0

grader confidence :  0.998105976275

grader feedback   :  {'spelling': 'Spelling: Ok.', 'grammar': 'Grammar: Ok.', 'markup-text': "pandas <bg>koalas are similar because</bg> they are both specialist who mostly eat herbs . but both of these species are different from pythons because pandas and koalas aren't as dangerous and they don't live in the everglades <bg>. also pandas can</bg> live in arid weather and pythons can not ."}
