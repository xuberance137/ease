# http://www.gregreda.com/2013/10/26/intro-to-pandas-data-structures/
# http://jpython.blogspot.com/2012/09/python-jsonpickle-object-serialization.html


import csv
import sys
import os
import json
import pickle
import pandas
import create, grade
import random
import logging
from generic_test import GenericTest

pandas.set_option('display.max_rows', 100)

tsv_file_name = './data/kaggle/train.tsv'
csv_file_name = './data/kaggle/train.csv'
json_file_name = './data/kaggle/train.json'

print "Importing TSV to CSV"
csv.field_size_limit(sys.maxsize)
csv.writer(file(csv_file_name, 'w+')).writerows(csv.reader(open(tsv_file_name), delimiter="\t"))

csv_file = open(csv_file_name, 'r')
json_file = open(json_file_name, 'w')

csvreader = csv.DictReader(csv_file)
fieldnames = ("Id", "EssaySet", "Score1", "Score2", "EssayText")
output = []

for item in csvreader:
    row = {}
    for field in fieldnames:
        row[field] = item[field]
    output.append(row)

obj = {u"kaggle": output}

print "Importing CSV to JSON"
json.dump(obj, json_file, indent=4, sort_keys=True)

#pandas dataframe with kaggle data
print "Loading CSV to Pandas DataFrame"
df = pandas.read_csv(csv_file_name)

print "Initializing Test Scoring Object"
TestObj = GenericTest()

print "Loading Data for Test Scoring Setup"
scores = df['Score1']
text = df['EssayText']

print "Total number of data points as input: ", len(scores)
TestObj.generic_setup(scores, text)

print "Model Creation"
model = TestObj.model_creation()

# print "model text input  : ", model['text']
# print "model features    : ", model['feature_ext']
print "model score input : ", model['score']
print "model prediction  : ", model['prediction']
print "model KAPPA       : ", model['cv_kappa']
print "model MAE         : ", model['cv_mean_absolute_error']

print "Writing Feature Data"	
pickle.dump(model, open( "./data/model_data.p", "wb"))
model_data = pickle.load(open("./data/model_data.p", "rb" ))

print "Model Based Grading"
grader_output = TestObj.model_based_grading(model_data)
print "grader text input : ", grader_output['text']
print "grader score      : ", grader_output['score']
print "grader confidence : ", grader_output['confidence']
print "grader feedback   : ", grader_output['feedback']

#print "Assessing Scoring Accuracy"
#TestObj.scoring_accuracy()







