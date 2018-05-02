# ! -*- coding:utf-8 -*-
import logging

import tensorflow as tf
from tensorflow.contrib import rnn

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("data/", one_hot=True)

lr = 0.001
training_iters = 100000
batch_size = 128
display_step = 10

n_input = 28
n_step = 28
n_hidden = 128
n_classes = 10

x = tf.placeholder(tf.float32, [None, n_step, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
w = tf.Variable(tf.random_normal([n_hidden, n_classes]))
b = tf.Variable(tf.random_normal([n_classes]))

def RNN(x):
    cell = rnn.BasicLSTMCell(n_hidden)
    outputs, states = tf.nn.dynamic_rnn(cell, x, dtype=tf.float32)
    return tf.matmul(tf.transpose(outputs, [1, 0, 2])[-1], w) + b

pred = RNN(x)

cost = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y)
)

optimizer = tf.train.AdamOptimizer(lr).minimize(cost)
correct_pred = tf.equal(tf.arg_max(pred, 1), tf.arg_max(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

tf.summary.scalar('accuracy', accuracy)
tf.summary.scalar('loss', cost)
summaries = tf.summary.merge_all()

with tf.Session() as sess:
    train_writer = tf.summary.FileWriter('logs/', sess.graph)
    init = tf.global_variables_initializer()
    sess.run(init)
    step = 1
    while batch_size * step < training_iters:
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        batch_x = batch_x.reshape(batch_size, n_step, n_input)
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        if step % display_step == 0:
            acc, loss = sess.run(
                [accuracy, cost], feed_dict={x: batch_x,
                                             y: batch_y}
            )
            print("Iter " + str(step * batch_size) +
                  ",Miniba{:.6f}".format(loss) +
                  ", Training Accuracy{:.5f}".format(acc))
        if step % 100 == 0:
            s = sess.run(summaries, feed_dict={x: batch_x, y: batch_y})
            train_writer.add_summary(s, global_step=step)
        step += 1

    print("Optimization Finished!")

    test_len = 128
    test_data = mnist.test.images[:test_len].reshape((-1, n_step, n_input))
    test_label = mnist.test.labels[:test_len]
    print("Testing Accuracy:",
          sess.run(accuracy, feed_dict={x: test_data, y: test_label}))


