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

input_video = "input_images_and_videos/20191126-M02-1"

# By default I use an "SSD with Mobilenet" model here. See the detection model zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
detection_graph, category_index = backbone.set_model('output_7kStepsSSD', 'parcel.pbtxt')

is_color_recognition_enabled = 0 # set it to 1 for enabling the color prediction for the detected objects
# Main count for count total parcels
roi_y = 600 # roi line position
# Count lines for couting chutes : [x_start, x_end, y_line]
roi_chutes = [[536, 563, 716], [565, 432, 546], [588, 316, 415], [605, 238, 318], [615, 176, 241], [630, 131, 181],
              [1023, 534, 711], [992, 412, 550], [958, 312, 419], [930, 242, 320], [904, 180, 244], [882, 125, 184]]
# the constant that represents the object counting area
deviation = 25

object_counting_api.vlCouting_parcel_passed_line(input_video, detection_graph, category_index, is_color_recognition_enabled, roi_y, roi_chutes, deviation, True, True) # counting all the objects
