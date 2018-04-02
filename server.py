import numpy as np 
import matplotlib as mp
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.examples.tutorials.mnist import input_data
import math
import os
import json
from aiohttp import web
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send, emit
import copy
import time

app = Flask(__name__, static_url_path='', static_folder='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

sess = tf.Session()

STATE_NEW = 'new'
STATE_TRAINING = 'training'
STATE_TRAINED = 'trained'

EVENT_CURRENT_STATE = 'state'
EVENT_CURRENT_TRAIN_STATE = 'train_state'

LAYER_CONVOLUTION = 'convolution'
LAYER_MAX_POOL = 'max_pool'
LAYER_AVG_POOL = 'avg_pool'


class Layer(object):
    def __init__(self, type, kernel, nodes=5):
        self.type = type
        self.kernel = kernel
        self.nodes = nodes

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.__dict__) 

class Configuration(object):
    def __init__(self, state=STATE_NEW, learning_rate=0.01, epoch=1000, batch_size=70, dropout=0.5):
        self.state = STATE_NEW
        self.learning_rate = learning_rate
        self.epoch = epoch
        self.batch_size = batch_size
        self.dropout = dropout
        self.convolution_network = [
            Layer(LAYER_CONVOLUTION, 5, 5).to_dict(),
            Layer(LAYER_MAX_POOL, 2,).to_dict(),
            Layer(LAYER_CONVOLUTION, 5, 5).to_dict(),
            Layer(LAYER_MAX_POOL, 2).to_dict(),
            Layer(LAYER_CONVOLUTION, 5, 20).to_dict(),
            Layer(LAYER_MAX_POOL, 2).to_dict(),
        ]

    def to_dict(self):
        return self.__dict__


config = Configuration()
network = None
result = None


def send_state(include_self=True):
    current_config = config.to_dict()
    print('sending:', current_config)
    emit(EVENT_CURRENT_STATE, current_config, broadcast=True, include_self=include_self)

def send_train(epoch):
    print('sedning epoch:', epoch)
    emit(EVENT_CURRENT_TRAIN_STATE, {'epoch': epoch}, broadcast=True)

@socketio.on('change_learning_rate')
def on_change_learning_rate(data):
    print('change_learning_rate', data)
    config.learning_rate = float(data)
    send_state()

@socketio.on('change_dropout')
def on_change_dropout(data):
    print('change_dropout', data)
    config.dropout = float(data)
    send_state()

@socketio.on('change_epoch')
def on_change_epoch(data):
    print('change_epoch', data)
    config.epoch = int(data)
    send_state()

@socketio.on('change_batch_size')
def on_change_batch_size(data):
    print('change_batch_size', data)
    config.batch_size = int(data)
    send_state()

@socketio.on('change_layer_type')
def on_change_layer_type(data):
    print('change_layer_type', data)
    index = data['index']
    value = data['value']
    config.convolution_network[index]['type'] = value
    send_state()

@socketio.on('change_layer_kernel')
def on_change_layer_kernel(data):
    print('change_layer_kernel', data)
    index = data['index']
    value = data['value']
    config.convolution_network[index]['kernel'] = int(value)
    send_state()

@socketio.on('change_layer_nodes')
def on_change_layer_nodes(data):
    print('change_layer_nodes', data)
    index = data['index']
    value = data['value']
    config.convolution_network[index]['nodes'] = int(value)
    send_state()

@socketio.on('move_layer')
def on_move_layer(data):
    print('move_layer', data)
    index = data['index']
    level = data['level']
    to_index = index + level
    if to_index < 0 or to_index >= len(config.convolution_network):
        return
    config.convolution_network[index], config.convolution_network[to_index] = \
        config.convolution_network[to_index], config.convolution_network[index]

    send_state()

@socketio.on('remove_layer')
def on_remove_layer(data):
    print('remove_layer', data)
    index = int(data)
    del config.convolution_network[index]
    send_state()

@socketio.on('add_layer')
def on_add_layer():
    print('add layer')
    config.convolution_network.append(
        Layer(
            LAYER_MAX_POOL,
            5
        ).to_dict()
    )
    send_state()

@socketio.on('start_train')
def on_start_train():
    print('Start Training')
    config.state = STATE_TRAINING
    send_state()
    send_train(1)
    for epoch in range(1, config.epoch):
        time.sleep(0.05)
        if epoch % 100 == 0:
            send_train(epoch)
    config.state = STATE_TRAINED
    send_state()

@socketio.on('edit')
def on_edit():
    print('back to editing')
    config.state = STATE_NEW
    send_state()

@socketio.on('reset')
def on_reset():
    global config
    print('Start Training')
    config = Configuration()
    send_state()

@socketio.on('connect')
def on_connect():
    send_state()

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('frontend/dist/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('frontend/dist/css', path)

@app.route('/')
def root():
    return send_from_directory('frontend/dist', 'index.html')


if __name__ == '__main__':
    socketio.run(app)
