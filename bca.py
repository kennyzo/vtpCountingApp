#----------------------------------------------
#--- Author         : HL-Zo
#--- Mail           : hunglaidangvn@gmail.com
#--- Date           : 2nd December 2019
#----------------------------------------------

# Imports
import tensorflow as tf

# Object detection imports
from utils import backbone
from api import object_counting_api
# Imports MongoDB Pylib
import pymongo

# Connect to MongoDB
MONGO_DB_LINK = "mongodb://localhost:27017/"
MONGO_DB_NAME = "vlparceltracking"
MONGO_DB_COLL = "vlChuteMngt"

input_video = "input_images_and_videos/M02-20191203-8h34"

# By default I use an "SSD with Mobilenet" model here. See the detection model zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
detection_graph, category_index = backbone.set_model('output-7737', 'parcel.pbtxt')

is_color_recognition_enabled = 0 # set it to 1 for enabling the color prediction for the detected objects
# Main count for count total parcels
roi_y = 600 # roi line position
# Count lines for couting chutes : [x_start, x_end, y_line]
roi_chutes = [[562, 550, 719], [586, 416, 552], [604, 314, 418], [618, 238, 315], [630, 179, 240], [640, 130, 180],
              [987, 544, 712], [953, 413, 540], [925, 314, 412], [900, 237, 311], [880, 180, 234], [862, 131, 176]]
# the constant that represents the object counting area
deviation = 10

vlClient = pymongo.MongoClient(MONGO_DB_LINK)
vlDB = vlClient[MONGO_DB_NAME]
vlParcelCollection = vlDB[MONGO_DB_COLL]

object_counting_api.vlCouting_parcel_passed_line(vlParcelCollection, input_video, detection_graph, category_index, is_color_recognition_enabled, roi_y, roi_chutes, deviation, True, False) # counting all the objects
