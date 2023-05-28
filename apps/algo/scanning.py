from nfstream import NFStreamer
import time
import os
from core.settings import READY_FILES_ROOT, BASE_DIR
from datetime import datetime
import pandas as pd
import numpy as np
from collections import Counter

USED_FIELDS = ['application_category_name', 'bidirectional_first_seen_ms']


class Scanning:

    def __init__(self):
        self.streamer = 0

    def scan(self, path_file):
        self.streamer = NFStreamer(source=BASE_DIR + '/' + str(path_file),
                                   statistical_analysis=True,
                                   decode_tunnels=True).to_pandas()
        name = str(int(time.time())) + '.csv'
        self.streamer.to_csv(READY_FILES_ROOT + '/' + name)
        return name

    def getOutputData(self, path_result):
        result = []
        file = pd.read_csv(READY_FILES_ROOT + '/' + str(path_result))
        application_names = file['application_category_name'].unique()
        for i in application_names:
            result.append(file.query(f'application_category_name == "{i}"').shape[0])
        return [application_names, result]

    def getTime(self, path_result):
        file = pd.read_csv(READY_FILES_ROOT + '/' + str(path_result))
        file["time"] = pd.to_datetime(file["bidirectional_first_seen_ms"] / 1000, unit="s")
        result = file.groupby(pd.Grouper(key="time", freq="1min")).count()
        result = result['bidirectional_packets']
        result.index = result.index.strftime('%Y-%m-%d %H:%M')
        return result

    def getWeight(self, path_result):
        file = pd.read_csv(READY_FILES_ROOT + '/' + str(path_result))
        file["time"] = pd.to_datetime(file["bidirectional_first_seen_ms"] / 1000, unit="s")
        result = file.groupby(pd.Grouper(key="time", freq="1min")).agg({"bidirectional_bytes": "sum"})
        result = result['bidirectional_bytes'].values / 1000000
        return result

    def getTable(self, path_result):
        need = ['bidirectional_first_seen_ms', 'src_ip', 'src_mac',
                'src_port', 'dst_ip', 'dst_mac', 'dst_port', 'protocol',
                'bidirectional_packets', 'bidirectional_bytes',
                'application_name', 'application_category_name',
                'requested_server_name', 'client_fingerprint', 'server_fingerprint']
        file = pd.read_csv(READY_FILES_ROOT + '/' + str(path_result))
        file['bidirectional_first_seen_ms'] = pd.to_datetime(file["bidirectional_first_seen_ms"] / 1000, unit="s")
        return file[need].replace(np.nan, '-').to_dict('records')
