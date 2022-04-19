from abc import ABC
from typing import List
import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from keras import Sequential
from keras.layers import LSTM, Dense, Activation
from sklearn.metrics import mean_squared_error
from math import sqrt

from sklearn.preprocessing import MinMaxScaler

from SoftSensor.SoftSensor_Admin.MLModel import MLModel

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False
TRAIN_SPLIT = 300000
BATCH_SIZE = 256
BUFFER_SIZE = 10000
EVALUATION_INTERVAL = 200
EPOCHS = 9


class LSTMModel(MLModel, ABC):
    def __init__(self):
        self.model_type = None
        self.n_features = 0
        self.storedX = None
        super().__init__()

    # def read_data(self):
    #     zip_path = tf.keras.utils.get_file(
    #         origin='https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip',
    #         fname='jena_climate_2009_2016.csv.zip',
    #         extract=True)
    #     csv_path, _ = os.path.splitext(zip_path)
    #     df = pd.read_csv(csv_path)
    #     print(df.head())
    #     print("---------------------------------------------------")
    #     return df

    def setUp(self, model_name=None):
        if model_name is not None:
            self.model_type = model_name
        return

    def preprocessing(self, df, y):
        # print(df.columns)
        # features_considered = ['S_T_C', 'S_Pin_kPa', 'S_F_kgh', 'S_E_kW', 'S_Pout_kPa']
        # x_0 = None
        # x_1 = None
        # x_2 = None
        # x_3 = None
        # x_4 = None
        # x_5 = None
        # x_6 = None
        # x_7 = None
        # x_8 = None
        # list = [x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8]

        features_considered = df.columns.tolist()

        if 'CUR_DATE' in features_considered:
            features_considered.remove('CUR_DATE')

        if 'CUR_TIME' in features_considered:
            features_considered.remove('CUR_TIME')

        list = []
        for feature in features_considered:
            x_i = None
            list.append(x_i)
        features = df[features_considered]

        # features.index = df['CUR_TIME']
        # print(features.head())
        # features.plot(subplots=True)
        # df = features
        # plt.show()
        print("---------------------------------------------------")
        # convert to [rows, columns] structure
        for k in range(len(features_considered) - 1):
            list[k] = df.iloc[:, k].values

        # print(x_2)

        # x_0 = df.iloc[:, 0].values
        # x_1 = df.iloc[:, 1].values
        # x_2 = df.iloc[:, 2].values
        # x_3 = df.iloc[:, 3].values
        y = df.iloc[:, -1].values

        for k in range(len(features_considered) - 1):
            list[k] = list[k].reshape((len(list[k]), 1))

        # x_0 = x_0.reshape((len(x_0), 1))
        # x_1 = x_1.reshape((len(x_1), 1))
        # x_2 = x_2.reshape((len(x_2), 1))
        # x_3 = x_3.reshape((len(x_3), 1))

        y = y.reshape((len(y), 1))

        scaler = MinMaxScaler(feature_range=(0, 1))

        for k in range(len(features_considered) - 1):
            list[k] = scaler.fit_transform(list[k])
        # x_0_scaled = scaler.fit_transform(x_0)
        # x_1_scaled = scaler.fit_transform(x_1)
        # x_2_scaled = scaler.fit_transform(x_2)
        # x_3_scaled = scaler.fit_transform(x_3)
        y_scaled = scaler.fit_transform(y)

        # counter = 0
        # for i in range(len(list)):
        #     if not list[i]:
        #         counter += 1
        #         print(counter)

        # print("BEFORE",list,y_scaled)
        # if len(list) >= 4:
        #     dataset_stacked = np.hstack((list[0], list[1], list[2], list[3], y_scaled))
        # else:
        #     dataset_stacked = np.hstack((list[0], list[1], y_scaled))
        # print("AFTER",dataset_stacked)
        # print("x_0.shape", list[0].shape)
        # print("x_1.shape", list[1].shape)
        # print("x_2.shape", list[2].shape)
        # print("x_3.shape", list[3].shape)
        # print("dataset_stacked.shape", dataset_stacked.shape)
        print("y.shape", y.shape)
        dataset_stacked = []
        print(dataset_stacked)
        for i in range(y.shape[0]):
            tempList = []
            for arr_i in list:
                if arr_i is not None:
                    tempList.append(arr_i[i][0])
            tempList.append(y[i][0])
            dataset_stacked.append(tempList)

        dataset_stacked = np.array(dataset_stacked)
        print(dataset_stacked)
        print("dataset_stacked.shape", dataset_stacked.shape)
        print("---------------------------------------------------")
        self.n_features = dataset_stacked.shape[1] - 1
        return dataset_stacked

    def split_sequences(self, sequences, n_steps_in=10, n_steps_out=1):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out - 1
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix - 1:out_end_ix, -1]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)

    def multivariate_data(self, dataset, target, start_index, end_index, history_size,
                          target_size, step, single_step=False):
        data_ = []
        labels = []

        start_index = start_index + history_size

        if end_index is None:
            end_index = len(dataset) - target_size
        end_index = len(dataset) + 1
        print("start", start_index)
        print("end", end_index)

        for i in range(start_index, end_index):
            indices = range(i - history_size, i, step)
            print(indices)
            print(len(dataset))
            data_.append(dataset[indices])

            if single_step:
                labels.append(target[i + target_size - 1])
            else:
                labels.append(target[i:i + target_size])

        return np.array(data_), np.array(labels)

    def train_val_split(self, XX, yy):
        print(XX)
        print(yy)
        split = len(XX)//2
        print(split)
        train_X, train_y = XX[:split, :], yy[:split, :]
        test_X, test_y = XX[split:, :], yy[split:, :]

        print("train_X.shape", train_X.shape)
        print("train_y.shape", train_y.shape)
        print("test_X.shape", test_X.shape)
        print("test_y.shape", test_y.shape)
        print("n_features", self.n_features)

        return train_X, train_y, test_X, test_y, self.n_features

    def get_metrics(self, y_test, y_pred) -> List[float]:

        mse = mean_squared_error(y_test, y_pred)
        rmse = sqrt(mse)
        print('RMSE: %f' % rmse)
        return rmse

    def plot_train_history(self, history, title):
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(len(loss))

        plt.figure()

        plt.plot(epochs, loss, 'b', label='Training loss')
        plt.plot(epochs, val_loss, 'r', label='Validation loss')
        plt.title(title)
        plt.legend()

        plt.show()

    def create_time_steps(self, length):
        return list(range(-length, 0))

    def show_plot(self, plot_data, delta, title):
        labels = ['History', 'True Future', 'Model Prediction']
        marker = ['.-', 'rx', 'go']
        time_steps = self.create_time_steps(plot_data[0].shape[0])
        if delta:
            future = delta
        else:
            future = 0

        plt.title(title)
        for i, x in enumerate(plot_data):
            if i:
                plt.plot(future, plot_data[i], marker[i], markersize=10,
                         label=labels[i])

            else:
                plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])

        plt.legend()
        plt.xlim([time_steps[0], (future + 5) * 2])
        plt.xlabel('Time-Step')

        return plt

    def train_model(self, train_X, train_y, test_X, test_y):
        opt = tf.keras.optimizers.Adam(learning_rate=0.01)
        n_steps_in = 10
        n_steps_out = 1
        # define model
        model = Sequential()
        model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(n_steps_in, self.n_features)))
        model.add(Dense(n_steps_out))
        model.add(Activation('linear'))
        model.compile(loss='mse', optimizer=opt, metrics=['mse'])
        history = model.fit(train_X, train_y, epochs=25, steps_per_epoch=25, verbose=1,
                            validation_data=(test_X, test_y), shuffle=False)
        return model

    def save_model(self, model, name='LSTM_model'):
        model_to_save = model
        model_to_save.save(name + '.h5')
        print("Model successfully Saved.")

    def load_model(self, name='LSTM_model'):
        try:
            loaded_model = tf.keras.models.load_model(name + '.h5')
            print("Model successfully loaded.")
            return loaded_model
        except:
            print("Error in loading model!")

    def start_training(self, x, y):
        df1 = pd.DataFrame(x[0])
        df2 = self.storedX
        self.storedX = df1.append(df2, ignore_index=True)
        if len(self.storedX) < 11:
            return
        print("---------------Training Started--------------")
        print(self.storedX)
        df = self.storedX
        preprocessed = self.preprocessing(df, y)
        print(preprocessed)
        XX, yy = self.split_sequences(preprocessed)
        train_X, train_y, test_X, test_y, n_features = self.train_val_split(XX, yy)
        model = self.train_model(train_X, train_y, test_X, test_y)
        self.save_model(model)
        self.storedX = None
        print("--------------Training Ended---------------")
        pass


if __name__ == '__main__':
    test = LSTMModel()

    # test.start_training(1, 2)
    # data = test.read_data()

    # preprocessed_dataset = test.preprocessing(data)
    # print(preprocessed_dataset)
    # x_train, train_data, val_data = test.train_val_split(preprocessed_dataset)
    # test.train_model(x_train, train_data, val_data)
    # test.load_model()
