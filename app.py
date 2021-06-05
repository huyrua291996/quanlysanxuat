"""

A small Test application to show how to use Flask-MQTT.

"""
import logging

import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import csv
from datetime import datetime
from models import db

eventlet.monkey_patch()

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'nguyenngochuy',
    'db': 'quanlysanxuat',
    'host': 'localhost',
    'port': '5432',
}
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'huyrua291996'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
# app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
# app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
# app.config['MQTT_LAST_WILL_QOS'] = 1
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#db.init_app(app)

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
# mqtt.subscribe("d/3c71bf6c0684/p/UP/3/W_SWITCH", 1)
# mqtt.subscribe("d/3c71bf6c0684/p/UP/2/W_SWITCH", 1)
# mqtt.subscribe("d/3c71bf6c0684/p/UP/1/W_SWITCH", 1)
# mqtt.subscribe("d/246f28a7a218/p/UP/3/W_SWITCH", 1)
# mqtt.subscribe("d/246f28a7a218/p/UP/2/W_SWITCH", 1)
# mqtt.subscribe("d/246f28a7a218/p/UP/1/W_SWITCH", 1)
mqtt.subscribe("d/246f28a6de88/p/UP/2/W_SWITCH", 1)
mqtt.subscribe("d/246f28a6de88/p/UP/1/W_SWITCH", 1)
global job_done, job_done1, job_done2, muctieu1, heso1, muctieu2, heso2, muctieu3, heso3
job_done = 0
job_done1 = 0
job_done2 = 0
muctieu1 = 0
heso1 = 0
muctieu2 = 0
heso2 = 0
muctieu3 = 0
heso3 = 0
start_job = False
#with open("log.csv", "w") as log_file:
#    log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    log_writer.writerow(['Vi tri', 'He so', 'Muc tieu','So san pham', 'Thoi gian'])

@app.route('/')
def index():
    global job_done
    return render_template('index.html')


# @socketio.on('publish')
# def handle_publish(json_str):
#     data = json.loads(json_str)
#     mqtt.publish(data['topic'], data['message'], data['qos'])


@socketio.on('data1')
def parse_data1(json_str):
    global muctieu1, heso1
    data = json.loads(json_str)
    muctieu1 = data['muctieu1']
    heso1 = data['heso1']

@socketio.on('data2')
def parse_data2(json_str):
    global muctieu2, heso2
    data = json.loads(json_str)
    muctieu2 = data['muctieu2']
    heso2 = data['heso2']

@socketio.on('data3')
def parse_data1(json_str):
    global muctieu3, heso3
    data = json.loads(json_str)
    muctieu3 = data['muctieu3']
    heso3 = data['heso3']


# @socketio.on('unsubscribe_all')
# def handle_unsubscribe_all():
#     mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global job_done, job_done1, job_done2, muctieu1, heso1, muctieu2, heso2, muctieu3, heso3
    topic_list = []
    topic_list = message.topic.split('/')
    if ("TOUCH" in message.payload.decode()):
        if (topic_list[1].startswith("3c71bf6c0684") == True):
            if (topic_list[4].startswith("3") == True):
                job_done = job_done + 1	
                job_cal = job_done * int(heso1)	
                now = datetime.now()
                #with open("log.csv", "a") as log_file:
                #    log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #    log_writer.writerow(['Position 1', heso1, muctieu1, job_done, now.strftime("%m/%d/%Y, %H:%M:%S")])
                #print(job_done)
            elif (topic_list[4].startswith("1") == True):
                job_done = 0
            elif (topic_list[4].startswith("2") == True):
                start_job = True
            socketio.emit('mqtt_message', data=job_cal)
        if (topic_list[1].startswith("246f28a7a218") == True):
            if (topic_list[4].startswith("3") == True):
                job_done1 = job_done1 + 1	
                job_cal1 = job_done1 * int(heso2)	
                now = datetime.now()
                #with open("log.csv", "a") as log_file:
                #    log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #    log_writer.writerow(['Position 2', heso2, muctieu2, job_done1, now.strftime("%m/%d/%Y, %H:%M:%S")])
                #print(job_done)
            elif (topic_list[4].startswith("1") == True):
                job_done1 = 0
            elif (topic_list[4].startswith("2") == True):
                start_job = True
            socketio.emit('mqtt_message1', data=job_cal1)
        if (topic_list[1].startswith("246f28a6de88") == True):
            if (topic_list[4].startswith("2") == True):
                job_done2 = job_done2 + 1	
                job_cal2 = job_done2 * int(heso3)	
                now = datetime.now()
                #with open("log.csv", "a") as log_file:
                #    log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #    log_writer.writerow(['Position 3', heso3, muctieu3, job_done2, now.strftime("%m/%d/%Y, %H:%M:%S")])
                #print(job_done)
            elif (topic_list[4].startswith("1") == True):
                job_done2 = 0
            #elif (topic_list[4].startswith("2") == True):
            #    start_job = True
            socketio.emit('mqtt_message2', data=job_cal2)        


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass

import os
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
    #socketio.run(app, use_reloader=False, debug=True)
    #app.run(debug=True)
