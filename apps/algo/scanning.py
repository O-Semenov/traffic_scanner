from nfstream import NFStreamer
import time
import os
from core.settings import READY_FILES_ROOT, BASE_DIR
from datetime import datetime
import pandas as pd
import numpy as np
from collections import Counter


class Scanning:

    def __init__(self):
        self.streamer = 0

    def scan(self, path_file):
        self.streamer = NFStreamer(source=BASE_DIR + '/' + str(path_file)).to_pandas()
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

    def getTime(self, path_result):
        file = pd.read_csv(READY_FILES_ROOT + '/' + str(path_result))
        time_query = file['bidirectional_first_seen_ms'] / 1000
        count_time = Counter([datetime.utcfromtimestamp(int(item)).strftime('%Y-%m-%d %H:%M') for item in time_query])
        count_time = sorted(count_time.items())
        list1, list2 = zip(*count_time)
        return [list1, list2]
