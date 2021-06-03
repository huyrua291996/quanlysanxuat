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

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 1

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
mqtt.subscribe("d/3c71bf6c0684/p/UP/3/W_SWITCH", 1)
mqtt.subscribe("d/3c71bf6c0684/p/UP/2/W_SWITCH", 1)
mqtt.subscribe("d/3c71bf6c0684/p/UP/1/W_SWITCH", 1)
global job_done, job_done1, job_done2
job_done = 0
job_done1 = 0
job_done2 = 0
start_job = False
with open("log.csv", "w") as log_file:
    log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    log_writer.writerow(['Vi tri', 'So san pham', 'Thoi gian'])

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
    data = json.loads(json_str)
    print(data['heso1'])
    print(data['muctieu1'])


# @socketio.on('unsubscribe_all')
# def handle_unsubscribe_all():
#     mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global job_done, job_done1, job_done2
    topic_list = []
    topic_list = message.topic.split('/')
    if (topic_list[1].startswith("3c71bf6c0684") == True):
        if (topic_list[4].startswith("3") == True):
            job_done = job_done + 1		
            now = datetime.now()
            with open("log.csv", "a") as log_file:
                log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                log_writer.writerow(['Position 1', job_done, now.strftime("%m/%d/%Y, %H:%M:%S")])
            #print(job_done)
        elif (topic_list[4].startswith("1") == True):
            job_done = 0
        elif (topic_list[4].startswith("2") == True):
            start_job = True
        socketio.emit('mqtt_message', data=job_done)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
    #app.run(debug=True)
