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
from io import BytesIO
import base64
import re
from PIL import Image
import time

app = Flask(__name__, static_url_path='', static_folder='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

STATE_NEW = 'new'
STATE_TRAINING = 'training'
STATE_TRAINED = 'trained'

EVENT_CURRENT_STATE = 'state'
EVENT_CURRENT_TRAIN_STATE = 'train_state'
EVENT_ERROR = 'error'
EVENT_RESULT = 'result'

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
sess = None
result = None
train_accuracy = None

def generate_unit_image(units):
    filters = units.shape[3]

    images = []
    for i in range(filters):
        image = units[0,:,:,i]
        images.append(generate_image(image))
    
    return images


def generate_image(image, figsize=(1, 1)):
    buffer = BytesIO()

    spines = 'left', 'right', 'top', 'bottom'
    labels = ['label' + spine for spine in spines]

    tick_params = {spine : False for spine in spines}
    tick_params.update({label : False for label in labels})

    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.imshow(image, cmap='magma', interpolation='nearest', aspect='auto')

    for spine in spines:
        ax.spines[spine].set_visible(False)
        ax.tick_params(**tick_params)

    fig.savefig(buffer, bbox_inches='tight', pad_inches=0, transparent=True, format='png')
    plt.close(fig)
    base64data = base64.encodestring(buffer.getvalue()).decode('ascii').strip()
    
    return "data:image/png;base64,%s" % (base64data)


def getActivatedUnits(layer, stimuli):
    return sess.run(layer, feed_dict={network[0]:np.reshape(stimuli,[1,784],order='F'), network[1]:1.0})


def getActivateUnitImage(layer, stimuli):
    return generate_unit_image(getActivatedUnits(layer, stimuli))



def send_state(include_self=True):
    current_config = config.to_dict()
    print('sending:', current_config)
    socketio.emit(EVENT_CURRENT_STATE, current_config, broadcast=True, include_self=include_self)

def send_train(epoch, accuracy=[]):
    print('sending epoch:', epoch)
    socketio.emit(EVENT_CURRENT_TRAIN_STATE, {'epoch': epoch, 'accuracy': accuracy}, broadcast=True)

def send_error(error):
    print('sending error:', error)
    socketio.emit(EVENT_ERROR, error, broadcast=True)

def send_result(result):
    print('sending result:')
    socketio.emit(EVENT_RESULT, result, broadcast=True)


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
    global network, sess, train_accuracy
    print('Start Training')
    config.state = STATE_TRAINING
    send_state()
    
    tf.reset_default_graph()
    x = tf.placeholder(tf.float32, [None, 784],name="x-in")
    true_y = tf.placeholder(tf.float32, [None, 10],name="y-in")
    keep_prob = tf.placeholder("float")

    x_image = tf.reshape(x,[-1,28,28,1])
    network = [x, keep_prob, x_image]
    for layer_config in config.convolution_network:
        kernel_size = layer_config['kernel']
        nodes = layer_config['nodes']
        if layer_config['type'] == LAYER_CONVOLUTION:
            network.append(
                slim.conv2d(network[-1], nodes, [kernel_size, kernel_size]) 
            )
        elif layer_config['type'] == LAYER_AVG_POOL:
            network.append( 
                slim.avg_pool2d(network[-1], [kernel_size, kernel_size]) 
            )
        elif layer_config['type'] == LAYER_MAX_POOL:
            network.append( 
                slim.max_pool2d(network[-1], [kernel_size, kernel_size]) 
            )
        else:
            send_error("Something went wrong! Unknow layer type")
            break

    flatten = slim.flatten(network[-1])
    out_y = slim.fully_connected(flatten, 10, activation_fn=tf.nn.softmax)
    network.append(flatten)
    network.append(out_y)

    cross_entropy = -tf.reduce_sum(true_y*tf.log(out_y))
    correct_prediction = tf.equal(tf.argmax(out_y, 1), tf.argmax(true_y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    batchSize = config.batch_size
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    train_accuracy = []

    for i in range(config.epoch+1):
        batch = mnist.train.next_batch(batchSize)
        sess.run(train_step, feed_dict={x:batch[0],true_y:batch[1], keep_prob: config.dropout})
        if i % 10 == 0:
            train_accuracy.append(
                float(sess.run(accuracy, feed_dict={x:batch[0],true_y:batch[1], keep_prob:1.0}))
            )
            send_train(i, train_accuracy)

    send_train(config.epoch, train_accuracy)
    testAccuracy = sess.run(accuracy, feed_dict={x:mnist.test.images,true_y:mnist.test.labels, keep_prob:1.0})
    print("test accuracy %g"%(testAccuracy))

    config.state = STATE_TRAINED
    send_state()


def create_result(imageToUse):
    flatten = getActivatedUnits(network[-2], imageToUse).tolist()[0]
    flatten_len = len(flatten)
    flatten = np.reshape(flatten, [-1,flatten_len])

    res = {
        'input_image': generate_image(np.reshape(imageToUse, [28,28])),
        'convolution': [],
        'flatten': generate_image(flatten, figsize=(6,1)),
        'predict': []
    }

    for layer, layer_config in zip(network[3:-2], config.convolution_network):
        res['convolution'].append({
            'images': getActivateUnitImage(layer, imageToUse),
            'config': layer_config
        })

    res['predict'] = getActivatedUnits(network[-1], imageToUse).tolist()[0]

    return res


@socketio.on('runRandom')
def on_run_random(data):
    print('Start runing')

    number = int(data)
    index = 0

    if number > -1:

        locations = np.where(mnist.test.labels.argmax(axis=1) == number)[0]
        index = np.random.choice(locations)
    else:
        index = np.random.randint(0, len(mnist.test.images))
    
    imageToUse = mnist.test.images[ index ]

    res = create_result(imageToUse)
    send_result(res)


@socketio.on('runWithImage')
def on_run(data):
    print('Start runing')

    imgstr = re.search(r'base64,(.*)', data).group(1)
    image_bytes = BytesIO(base64.b64decode(imgstr))
    im = Image.open(image_bytes).convert('LA')
    im = im.resize((28, 28))

    rgb_image = np.array(im)
    gray_image = rgb_image[:,:,0]
    print(gray_image.shape)
    gray_image = gray_image / gray_image.max()

    imageToUse = gray_image.flatten()

    res = create_result(imageToUse)
    send_result(res)


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
    print('Client connected')
    send_state()

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    global config
    print('ERROR OCCURED')
    send_error(str(e))
    config.state = STATE_NEW
    send_state()

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
