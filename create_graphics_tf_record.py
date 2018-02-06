# --------------------------------------------------------
# Adapted from Tensorflow Object Detection API
# Written by Frank Julca Aguilar
# --------------------------------------------------------

import _init_paths
import tensorflow as tf

from object_detection.utils import dataset_util
import PIL.Image
import io
import os
import glob
from lxml import etree

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util
from evaluation_sets import evaluation_set

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('label_map_path', 'object_detection/data/flochart_label_map.pbtxt',
                    'Path to label map proto')
flags.DEFINE_string('dataset_directory', 'object_detection/flowcharts',
                    'Dataset directory')
flags.DEFINE_string('file_names', 'flowchart_train_set',
                    'Dataset directory')

FLAGS = flags.FLAGS


def create_tf_example(example, label_map_dict, dataset_directory):

  height = int(example['height']) # Image height
  width = int(example['width']) # Image width
  filename = example['file_name'] # Filename of the image. Empty if image is not from file
  # print(filename)

  full_path = os.path.join(dataset_directory, filename)
  with tf.gfile.GFile(full_path, 'rb') as fid:
    encoded_jpg = fid.read()
  encoded_image_data = io.BytesIO(encoded_jpg)
  image = PIL.Image.open(encoded_image_data)
  if image.format != 'JPEG':
    raise ValueError('Image format not JPEG')

  # encoded_image_data = example['encoded_image_bytes'] # Encoded image bytes
  image_format = example['image_format'].encode('utf8') # b'jpeg' or b'png'

  xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [] # List of normalized right x coordinates in bounding box
             # (1 per box)
  ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [] # List of normalized bottom y coordinates in bounding box
             # (1 per box)
  classes_text = [] # List of string class name of bounding box (1 per box)
  classes = [] # List of integer class id of bounding box (1 per box)

  for obj in example['object']:
    xmins.append(float(obj['bndbox']['xmin']) / width)
    ymins.append(float(obj['bndbox']['ymin']) / height)
    xmaxs.append(float(obj['bndbox']['xmax']) / width)
    ymaxs.append(float(obj['bndbox']['ymax']) / height)
    classes_text.append(obj['name'].encode('utf8'))
    classes.append(label_map_dict[obj['name']])


  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(example['file_name'].encode('utf8')),
      'image/source_id': dataset_util.bytes_feature(example['file_name'].encode('utf8')),
      'image/encoded': dataset_util.bytes_feature(encoded_jpg),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example


def generate_tf_record_for_files(output_path, label_map_path, file_names, dataset_directory):
  writer = tf.python_io.TFRecordWriter(output_path)

  label_map_dict = label_map_util.get_label_map_dict(label_map_path)

  files = evaluation_set[file_names]
  if files is None:
    print('invalid set')
    print('valid sets: %s' % evaluation_set.keys())
    return

  for example in files:
    example = os.path.join(dataset_directory, example + ".xml")
    if os.path.isfile(example):
      with tf.gfile.GFile(example, 'r') as fid:
          xml_str = fid.read()
      xml = etree.fromstring(xml_str)
      example_dict = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

      tf_example = create_tf_example(example_dict, label_map_dict, dataset_directory)
      writer.write(tf_example.SerializeToString())
    else:
      print('Not found file: %s', example)

  writer.close()


def main(_):
  generate_tf_record_for_files(FLAGS.output_path, FLAGS.label_map_path, 
    FLAGS.file_names, FLAGS.dataset_directory)


if __name__ == '__main__':
  tf.app.run()
