
class Statistics(object):

    def __init__(self, false_positives_rate, false_negatives_rate, positives_rate, negatives_rate):
        self._false_positives_rate = false_positives_rate
        self._false_negatives_rate = false_negatives_rate
        self._positives_rate = positives_rate
        self._negatives_rate = negatives_rate

    def get_false_positives_rate(self):
        return self._false_positives_rate

    def get_false_negatives_rate(self):
        return self._false_negatives_rate

    def get_positives_rate(self):
        return self._positives_rate

    def get_negatives_rate(self):
        return self._negatives_rate
