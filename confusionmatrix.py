class ConfusionMatrix:
    def __init__(self, true_positive=0, false_positive=0, false_negative=0, true_negative=0):
        self.true_positive = true_positive
        self.false_positive = false_positive
        self.false_negative = false_negative
        self.true_negative = true_negative

    def total(self):
        """ Sum of all outcomes """
        return self.true_positive + self.false_positive + self.true_negative + self.false_negative

    def actual_false(self):
        """ Amount of times outcomes was false """
        return self.false_positive + self.true_negative

    def actual_true(self):
        """ Amount of times outcome was true """
        return self.true_positive + self.false_negative

    def predicted_false(self):
        """ Amount of times outcome was predicted false """
        return self.false_negative + self.true_negative

    def predicted_true(self):
        """ Amount of times outcome was predicted true """
        return self.true_positive + self.false_positive

    def correct(self):
        """ Amount of times outcome was predicted correctly """
        return self.true_positive + self.true_negative

    def incorrect(self):
        """ Amount of times outcome was classified incorrectly """
        return self.false_negative + self.false_positive

    def accuracy(self):
        """ Correct classification rate """
        try:
            return self.correct()/self.total()
        except:
            return 0

    def miclassification_rate(self):
        """ Incorrect classification rate """
        try:
            return self.incorrect()/self.total()
        except:
            return 0

    def true_positive_rate(self):
        try:
            return self.true_positive/self.actual_true()
        except:
            return 0

    def false_positive_rate(self):
        try:
            return self.false_positive/self.actual_false()
        except:
            return 0

    def specificity(self):
        """ Rate false outcome is predicted correctly """
        try:
            return self.true_negative/self.actual_false()
        except:
            return 0

    def precision(self):
        """ Rate true outcome is predicted correctly """
        try:
            return self.true_positive/self.predicted_true()
        except:
            return 0

    def prevalence(self):
        """ Rate true outcome occurs """
        try:
            return self.actual_true()/self.total()
        except:
            return 0

    def positive_predictive_value(self):
        # maybe implement this sometime in the future
        pass

    def null_error_rate(self):
        # maybe implement this in the future
        pass

    def cohens_kappa(self):
        # look into this
        pass

    def f_score(self):
        # implement later
        pass

    def roc_curve(self):
        # implement later
        pass

    def row(self):
        return [
            self.true_positive,
            self.false_positive,
            self.false_negative,
            self.true_negative,
            self.accuracy(),
            self.miclassification_rate(),
            self.true_positive_rate(),
            self.false_positive_rate(),
            self.specificity(),
            self.precision()
        ]

    @classmethod
    def generate_from_point_clouds(cls, actual_points, predicted_points):
        """ Generates a confusion matrix from two point clouds """
        confusion_matrix = cls()
        for point_pair in zip(actual_points, predicted_points):
            actual, assigned = point_pair
            if actual.clazz and assigned.clazz: confusion_matrix.true_positive += 1
            elif actual.clazz and not assigned.clazz: confusion_matrix.false_negative += 1
            elif not actual.clazz and assigned.clazz: confusion_matrix.false_positive += 1
            else: confusion_matrix.true_negative += 1
        return confusion_matrix

    @classmethod
    def headers(cls):
        headers = [
            "TruePositive",
            "FalsePositive",
            "FalseNegative",
            "TrueNegative",
            "Accuracy",
            "MisclassificationRate",
            "TruePositiveRate",
            "FalsePositiveRate",
            "Specificity",
            "Precision",
        ]
        return headers
