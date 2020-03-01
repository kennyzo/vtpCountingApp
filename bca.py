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

input_video = "input_images_and_videos/M02-10h20"

is_color_recognition_enabled = 0 

detection_graph, category_index = backbone.set_model('output-33818', 'parcel.pbtxt')

roi_y = 700 # roi line position

# Count lines for couting chutes : [x_start, x_end, y_line]
# M02
roi_chutes = [[515, 528, 710], [545, 393, 535], [571, 292, 400],
              [591, 218, 298], [608, 160, 222], [620, 115, 161],
              [1045, 515, 700], [1007, 389, 530], [970, 292, 397],
              [939, 218, 299], [911, 160, 222], [888, 115, 164]]
#M16
# roi_chutes = [[315, 563, 720], [335, 428, 574], [370, 338, 436],
#               [399, 268, 340], [420, 216, 271], [436, 175, 218],
#               [936, 518, 720], [869, 393, 538], [813, 308, 410],
#               [772, 243, 315], [743, 195, 240], [720, 156, 200]]
# the constant that represents the object counting area
deviation = 25

vlClient = pymongo.MongoClient(MONGO_DB_LINK)
vlDB = vlClient[MONGO_DB_NAME]
vlParcelCollection = vlDB[MONGO_DB_COLL]

object_counting_api.vlCouting_parcel_passed_line(vlParcelCollection, input_video, detection_graph, category_index, is_color_recognition_enabled, roi_y, roi_chutes, deviation, True, True) # counting all the objects
