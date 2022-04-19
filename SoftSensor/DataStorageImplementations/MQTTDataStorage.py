from functools import partial

from IPython.core.display import display
from tkinter import StringVar, Tk, Label, Entry, Button, OptionMenu
import mysql.connector
import pandas as pd
import paho.mqtt.client as mqtt
import time
import random
import numpy as np
import pandas as pd

from SoftSensor.SoftSensor_Admin.DataStorage import DataStorage


class MQTTDataStorage(DataStorage):

    def __init__(self, myDataReceiver=None):
        self.inputName = None
        self.outputName = None
        self.client = None
        self.newData = False
        self.connected = False
        self.new_data = []

        self.clientName = None
        self.broker = None
        self.port = None
        self.user = None
        self.password = None
        self.input = None
        self.output = None
        super().__init__(myDataReceiver)

    def setUp(self):
        # window
        tkWindow = Tk()
        tkWindow.title('MQTT Credentials')
        tkWindow.eval('tk::PlaceWindow . center')

        # client label and password entry box
        clientLabel = Label(tkWindow, text="MQTT Client").grid(row=0, column=0)
        client = StringVar()
        clientEntry = Entry(tkWindow, textvariable=client).grid(row=0, column=1)

        # broker url label and text entry box
        brokerLabel = Label(tkWindow, text="MQTT Broker").grid(row=2, column=0)
        broker = StringVar()
        brokerEntry = Entry(tkWindow, textvariable=broker).grid(row=2, column=1)

        # port number label and text entry box
        portLabel = Label(tkWindow, text="MQTT Port").grid(row=4, column=0)
        port = StringVar()
        portEntry = Entry(tkWindow, textvariable=port).grid(row=4, column=1)

        # username label and text entry box
        userLabel = Label(tkWindow, text="Username").grid(row=6, column=0)
        user = StringVar()
        userEntry = Entry(tkWindow, textvariable=user).grid(row=6, column=1)

        # password label and text entry box
        passwordLabel = Label(tkWindow, text="Password").grid(row=8, column=0)
        password = StringVar()
        passwordEntry = Entry(tkWindow, textvariable=password).grid(row=8, column=1)

        # input label and text entry box
        inputLabel = Label(tkWindow, text="Input Topic Name").grid(row=10, column=0)
        input = StringVar()
        inputEntry = Entry(tkWindow, textvariable=input).grid(row=10, column=1)

        # output label and text entry box
        outputLabel = Label(tkWindow, text="Output Topic Name").grid(row=12, column=0)
        output = StringVar()
        outputEntry = Entry(tkWindow, textvariable=output).grid(row=12, column=1)



        # login button
        validateLoginFunc = partial(self.validateLoginFunc,
                                    client,
                                    broker,
                                    port,
                                    user,
                                    password,
                                    input,
                                    output)
        validateButton = Button(tkWindow, text="Validate", command=validateLoginFunc)
        validateButton.grid(row=16, column=0)
        validateButton.grid(pady=20, padx=40)

        # quit button
        quitButton = Button(tkWindow, text="Exit", command=tkWindow.destroy)
        quitButton.grid(row=16, column=1)
        quitButton.grid(pady=20, padx=80)

        tkWindow.mainloop()
        return True

    def validateLoginFunc(self, client, broker, port, user, password, input, output ):
        self.clientName = client.get()
        self.broker = broker.get()
        self.port = int(port.get())
        self.user = user.get()
        self.password = password.get()
        self.input = input.get()
        self.output = output.get()
        self.validateLogin(self.clientName, self.broker, self.port, self.user, self.password, self.input, self.output)
        return

    def notifyDataUpdate(self):
        if (myDataReceiver != None):
            self.myDataReceiver.notifyDataUpdate(self)

    def validateLogin(self, clientName, broker, port, user, password, input, output):
        self.client = mqtt.Client(clientName)
        if user != None and password != None:
            self.client.username_pw_set(user, password=password)

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.connected = True
            else:
                print("Connection failed with MQTT broker")
        self.client.on_connect=on_connect
        try:
            self.client.connect(broker, port=port)
        except:
            print("Connection failed in validate login")
        self.inputName = input
        self.outputName = output
        print("MQTT Data Storage set up with following details:")
        print("client entered:", clientName)
        print("broker entered:", broker)
        print("port entered:", port)
        print("username entered:", user)
        print("password entered:", password)
        print("input topic name entered:", self.inputName)
        print("output topic name entered:", self.outputName)
        return

    def checkExistanceOfNewData(self):
        def on_message(client, userdata, message):
            inputReceived = str(message.payload.decode("utf-8"))
            try:
                self.new_data.append(float(inputReceived))
            except:
                print("Could not parse incoming data for MQTT")
            self.newData = True

        self.client.loop_start()
        self.client.subscribe(self.inputName)
        self.client.on_message=on_message
        time.sleep(1)

        return self.newData

    def getData(self):
        result_list=[]
        output_list = np.zeros(len(self.new_data)).tolist()
        result=pd.DataFrame({self.inputName: self.new_data, self.outputName: output_list})
        result_list.append(result)
        self.new_data = []
        self.newData = False
        return result_list

    def receiveResults(self, results):
        for result in results[0][self.outputName]:
            self.client.publish(self.outputName,result)
        return True