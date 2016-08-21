import csv
import sys
import os
import json
import pandas
import create, grade
import random
import logging

log = logging.getLogger(__name__)

ROOT_PATH = os.path.abspath(__file__)
TEST_PATH = os.path.abspath(os.path.join(ROOT_PATH, ".."))

CHARACTER_LIMIT = 1000
TRAINING_LIMIT = 50
QUICK_TEST_LIMIT = TRAINING_LIMIT

class DataLoader():
    def load_text_files(self, pathname):
        filenames = os.listdir(pathname)
        text = []
        for filename in filenames:
            data = open(os.path.join(pathname, filename)).read()
            text.append(data[:CHARACTER_LIMIT])
        return text

    def load_json_file(self, filename):
        datafile = open(os.path.join(filename))
        data = json.load(datafile)
        return data

    def load_data(self):
        """
        Override when inheriting
        """
        pass
        
class ModelCreator():
    def __init__(self, scores, text):
        self.scores = scores
        self.text = text

        #Governs which creation function in the ease.create module to use.  See module for info.
        if isinstance(text, list):
            self.create_model_generic = False
        else:
            self.create_model_generic = True

    def create_model(self):
        if not self.create_model_generic:
            return create.create(self.text, self.scores, "")
        else:
            return create.create_generic(self.text.get('numeric_values', []), self.text.get('textual_values', []), self.scores)

class Grader():
    def __init__(self, model_data):
        self.model_data = model_data

    def grade(self, submission):
        if isinstance(submission, basestring):
            return grade.grade(self.model_data, submission)
        else:
            return grade.grade_generic(self.model_data, submission.get('numeric_values', []), submission.get('textual_values', []))

class GenericTest(object):
    loader = DataLoader
    data_path = ""
    expected_kappa_min = 0
    expected_mae_max = 0


    def load_data(self):
        data_loader = self.loader(os.path.join(TEST_PATH, self.data_path))
        scores, text = data_loader.load_data()
        return scores, text

    def generic_setup(self, scores, text):
        #Shuffle to mix up the classes, set seed to make it repeatable
        random.seed(1)
        shuffled_scores = []
        shuffled_text = []
        indices = [i for i in xrange(0,len(scores))]
        random.shuffle(indices)
        for i in indices:
            shuffled_scores.append(scores[i])
            shuffled_text.append(text[i])

        self.text = shuffled_text[:TRAINING_LIMIT]
        self.scores = shuffled_scores[:TRAINING_LIMIT]

    def model_creation_and_grading(self):
        score_subset = self.scores[:QUICK_TEST_LIMIT]
        text_subset = self.text[:QUICK_TEST_LIMIT]
        model_creator = ModelCreator(score_subset, text_subset)
        model_results = model_creator.create_model()
        assert model_results['success'] == True

        grader = Grader(model_results)
        grader_results = grader.grade(self.text[0])
        assert grader_results['success']==True
        
        return model_results, grader_results

    def model_creation(self):
        score_subset = self.scores[:QUICK_TEST_LIMIT]
        text_subset = self.text[:QUICK_TEST_LIMIT]
        model_creator = ModelCreator(score_subset, text_subset)
        model_results = model_creator.create_model()
        assert model_results['success'] == True
        
        return model_results

    def model_based_grading(self, model_results):

        grader = Grader(model_results)
        grader_results = grader.grade(self.text[0])
        assert grader_results['success']==True
        
        return grader_results

    def scoring_accuracy(self):
        random.seed(1)
        model_creator = ModelCreator(self.scores, self.text)
        results = model_creator.create_model()
        assert results['success']==True
        cv_kappa = results['cv_kappa']
        cv_mae = results['cv_mean_absolute_error']
        # print "MAE : ", cv_mae, "KAPPA : ", cv_kappa  ########
        # print "score : ", results['score']
        # print "predictions : ", results['prediction']
        assert cv_kappa>=self.expected_kappa_min
        #assert cv_mae <=self.expected_mae_max

    def generic_model_creation_and_grading(self):
        log.info(self.scores)
        log.info(self.text)
        score_subset = [random.randint(0,100) for i in xrange(0,min([QUICK_TEST_LIMIT, len(self.scores)]))]
        text_subset = self.text[:QUICK_TEST_LIMIT]
        text_subset = {
            'textual_values' : [[t] for t in text_subset],
            'numeric_values' : [[1] for i in xrange(0,len(text_subset))]
        }
        model_creator = ModelCreator(score_subset, text_subset)
        results = model_creator.create_model()
        assert results['success']==True

        grader = Grader(results)
        test_text = {
            'textual_values' : [self.text[0]],
            'numeric_values' : [1]
        }
        results = grader.grade(test_text)
        assert results['success']==True