from nfstream import NFStreamer
import time
import os
from core.settings import READY_FILES_ROOT, BASE_DIR


class Scanning:

    def __init__(self, path_file):
        self.streamer = NFStreamer(source=BASE_DIR + '/' + str(path_file)).to_pandas()
        os.remove(BASE_DIR + '/' + str(path_file))

    def scan(self):
        name = str(int(time.time())) + '.csv'
        self.streamer.to_csv(READY_FILES_ROOT + '/' + name)
        return name
