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

input_video = "input_images_and_videos/20191130_M02_08h24"

detection_graph, category_index = backbone.set_model('output-35791', 'parcel.pbtxt')

is_color_recognition_enabled = 0 

roi_y = 600 # roi line position

roi_chutes = [[536, 563, 716], 
            [565, 432, 546], 
            [588, 316, 415], 
            [605, 238, 318], 
            [615, 176, 241], 
            [630, 131, 181],
            [1023, 534, 711], 
            [992, 412, 550], 
            [958, 312, 419], 
            [930, 242, 320], 
            [904, 180, 244], 
            [882, 125, 184]]

deviation = 15

vlClient = pymongo.MongoClient(MONGO_DB_LINK)
vlDB = vlClient[MONGO_DB_NAME]
vlParcelCollection = vlDB[MONGO_DB_COLL]

object_counting_api.vlCouting_parcel_passed_line(vlParcelCollection, input_video, detection_graph, category_index, is_color_recognition_enabled, roi_y, roi_chutes, deviation, True, False) # counting all the objects
