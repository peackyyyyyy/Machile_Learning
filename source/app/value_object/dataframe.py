

class Dataframe(object):

    def __init__(self, cots_dataframe):
        self._cots_dataframe = cots_dataframe

    def get_dataframe(self):
        return self._cots_dataframe