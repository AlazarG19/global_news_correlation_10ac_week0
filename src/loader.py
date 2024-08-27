# preparing and importing the necessary packages
import pandas as pd


# creating wrapper classes for getting data
class NewsDataLoader:
    '''
    This class is used to load news data from the the different csv files
    '''
    def __init__(self, paths):
        '''
        path: path to the data
        '''
        self.paths = paths
        print(self.paths)

    def get_data(self,dataname):
        '''
        a function to get the data within the rating csv
        '''
        data = pd.read_csv(self.paths[dataname])
        

        return data

    