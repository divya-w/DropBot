import tensorflow as tf
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import network

# disable future warnings and info messages
#os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
#tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def distance_frame(frame):
    network_params = {"height": 320, "width": 640, "is_training": False}

    # model
    model = network.Pydnet(network_params)
    tensor_image = tf.placeholder(tf.float32, shape=(320, 640, 3))
    batch_img = tf.expand_dims(tensor_image, 0)
    tensor_depth = model.forward(batch_img)
    tensor_depth = tf.nn.relu(tensor_depth)

    # restore graph
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, "ckpt/pydnet")

    # preparing image
    img = frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    img = cv2.resize(img, (640, 320))
    img = img / 255.0

    # inference
    depth = sess.run(tensor_depth, feed_dict={tensor_image: img})
    depth = np.squeeze(depth)
    min_depth = depth.min()
    max_depth = depth.max()
    depth = (depth - min_depth) / (max_depth - min_depth)
    depth *= 255.0

    # preparing final depth
    # depth = cv2.resize(depth, (w, h)) # resize to original size
    plt.figure(1)
    plt.clf()
    plt.axis("off")
    plt.imshow(depth, cmap="magma")
    plt.pause(0.1)