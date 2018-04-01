import numpy as np 
import matplotlib as mp
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.examples.tutorials.mnist import input_data
import math
import os

from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.6

sess = tf.Session(config=config)

graph = None

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('chat message')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', room=sid)




app.router.add_static('/result', 'result')
app.router.add_static('/', 'frontend/dist')

if __name__ == '__main__':
    web.run_app(app, port=5000)