#----------------------------------------------
#--- Author         : Ahmet Ozlu
#--- Mail           : ahmetozlu93@gmail.com
#--- Date           : 27th January 2018
#----------------------------------------------

# Imports
import tensorflow as tf

# Object detection imports
from utils import backbone
from api import object_counting_api

input_video = "input_images_and_videos/20191123_M02_1"

# By default I use an "SSD with Mobilenet" model here. See the detection model zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
detection_graph, category_index = backbone.set_model('output_7kStepsSSD', 'parcel.pbtxt')

is_color_recognition_enabled = 0 # set it to 1 for enabling the color prediction for the detected objects
roi = 600 # roi line position
deviation = 25 # the constant that represents the object counting area

object_counting_api.couting_parcel_passed_line(input_video, detection_graph, category_index, is_color_recognition_enabled, roi, deviation, True, True) # counting all the objects
