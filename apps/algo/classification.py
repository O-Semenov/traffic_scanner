from nfstream import NFPlugin, NFStreamer
import numpy as np
import time
from sklearn import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from core.settings import READY_FILES_ROOT, BASE_DIR


def score(train, test):
    return np.sum(train == test) / len(train)


def app_name_prediction(streamer, X):
    application_names = streamer["application_name"].unique()
    print(application_names)
    AN_indexs = dict(zip(application_names, list(range(0, len(application_names)))))
    y = np.array(streamer["application_name"])
    for ind in range(0, len(y)):
        y[ind] = AN_indexs[y[ind]]
    y = y.astype('int')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=13)

    model = KNeighborsClassifier(n_neighbors=len(application_names))
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return score(y_test, pred)


def category_name_prediction(streamer, X):
    application_category = streamer["application_category_name"].unique()
    print(application_category)
    AC_indexs = dict(zip(application_category, list(range(0, len(application_category)))))
    y = np.array(streamer["application_category_name"])
    for ind in range(0, len(y)):
        y[ind] = AC_indexs[y[ind]]
    y = y.astype('int')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=13)

    model = KNeighborsClassifier(n_neighbors=len(application_category))
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return score(y_test, pred)


def use_class(user_id, path_file):
    streamer = NFStreamer(source="main_test.pcap").to_pandas()
    streamer.to_csv('leha.csv')
    X = np.array(streamer[["bidirectional_packets", "bidirectional_bytes"]])
    print(len(X))
    print('{:%} predicted name app'.format(app_name_prediction(streamer, X)))
    print('{:%} predicted category'.format(category_name_prediction(streamer, X)))


class Classification:

    def __init__(self, path_file):
        self.streamer = NFStreamer(source=BASE_DIR + '/' + str(path_file)).to_pandas()

    def scan(self):
        name = str(int(time.time())) + '.csv'
        self.streamer.to_csv(READY_FILES_ROOT + '/' + name)

        return name
