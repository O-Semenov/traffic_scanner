from nfstream import NFStreamer
import time
import os
from core.settings import READY_FILES_ROOT, BASE_DIR
import csv
import pandas as pd


class Scanning:

    def __init__(self):
        self.streamer = 0

    def setData(self, path_file):
        self.streamer = NFStreamer(source=BASE_DIR + '/' + str(path_file)).to_pandas()
        os.remove(BASE_DIR + '/' + str(path_file))

    def scan(self):
        name = str(int(time.time())) + '.csv'
        self.streamer.to_csv(READY_FILES_ROOT + '/' + name)
        return name

    def getOutputData(self, path_result):
        result = []
        file = pd.read_csv(READY_FILES_ROOT + '/' + str(path_result))
        application_names = file['application_name'].unique()
        for i in application_names:
            result.append(file.query(f'application_name == "{i}"').shape[0])
        return [application_names, result]
