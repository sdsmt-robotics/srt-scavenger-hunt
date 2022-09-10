# Editor: Bennet Outland
# Team: Rocker Robotics
# Script: SRT NST Example
# Year: 2022

"""
I edited the code from: https://www.tensorflow.org/tutorials/generative/style_transfer to create an easy NST example for SRT.
"""

#+---------------------------------------------+
#          Change the Stuff Below!
#+---------------------------------------------+

# Name of the style image in the
# paintings folder
style_img_name = "daVinci"

#+---------------------------------------------+

import tensorflow as tf
import tensorflow_hub as hub
import os
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

import numpy as np
import PIL.Image
import time
import functools
import sys

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

def imshow(image, title=None):
  if len(image.shape) > 3:
    image = tf.squeeze(image, axis=0)

  plt.imshow(image)
  if title:
    plt.title(title)

def load_img(path_to_img):
  max_dim = 720
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

# arguments check
if (len(sys.argv) < 2):
    print("Usage: " + sys.argv[0] + " [input image]")
    exit()

style_img_name = "daVinci"

file_name_in = sys.argv[1]
content_image = load_img(file_name_in)
style_image = load_img("paintings/" + style_img_name + ".jpg")

hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

file_name = "your_frickin_masterpeice" + ".png"
tensor_to_image(stylized_image).save(file_name)
