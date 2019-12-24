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


MONGO_DB_LINK = "mongodb://localhost:27017/"
MONGO_DB_NAME = "vlparceltracking"
MONGO_DB_COLL = "vlChuteMngt"

input_video = "input_images_and_videos/20191130_M02_08h39"

is_color_recognition_enabled = 0

detection_graph, category_index = backbone.set_model('output-141516', 'parcel.pbtxt')

roi_y = 580 # roi line position

# Count lines for couting chutes : [x_start, x_end, y_line]
roi_chutes = [[132, 450, 619], [156, 316, 452], [174, 214, 318], [188, 138, 215], [200, 79, 140], [210, 030, 80],
              [557, 444, 612], [523, 313, 440], [495, 214, 312], [470, 137, 211], [450, 80, 134], [432, 31, 76]]
# the constant that represents the object counting area
deviation = 25

vlClient = pymongo.MongoClient(MONGO_DB_LINK)
vlDB = vlClient[MONGO_DB_NAME]
vlParcelCollection = vlDB[MONGO_DB_COLL]

object_counting_api.vlCouting_parcel_passed_line(vlParcelCollection, input_video, detection_graph, category_index, is_color_recognition_enabled, roi_y, roi_chutes, deviation, True, True) # counting all the objects
