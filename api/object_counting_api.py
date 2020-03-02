#----------------------------------------------
#--- Author         : HL-Zo
#--- Mail           : hunglaidangvn@gmail.com
#--- Date           : 2nd December 2019
#----------------------------------------------

import tensorflow as tf
from utils import visualization_utils as vis_util
from time import gmtime, strftime
from datetime import datetime
import csv
import cv2
import numpy as np
import os

import pymongo

# Variables
#total_passed_vehicle = 0  # using it to count vehicles
'''
*****************************************************************
        ------------------------------------------
            DEFINE LINES FOR COUNTING
        ------------------------------------------
*****************************************************************
'''

def cumulative_object_counting_x_axis(input_video, detection_graph, category_index, is_color_recognition_enabled, roi, deviation):
        # input video
        cap = cv2.VideoCapture(input_video)

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('the_output.avi', fourcc, fps, (width, height))

        total_passed_vehicle = 0
        speed = "waiting..."
        direction = "waiting..."
        size = "waiting..."
        color = "waiting..."
        counting_mode = "..."
        width_heigh_taken = True
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # for all the frames that are extracted from input video
            while(cap.isOpened()):
                ret, frame = cap.read()

                if not  ret:
                    print("end of the video file...")
                    break

                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.
                counter, csv_line, counting_mode = vis_util.visualize_boxes_and_labels_on_image_array_x_axis(cap.get(1),
                                                                                                             input_frame,
                                                                                                             1,
                                                                                                             is_color_recognition_enabled,
                                                                                                             np.squeeze(boxes),
                                                                                                             np.squeeze(classes).astype(np.int32),
                                                                                                             np.squeeze(scores),
                                                                                                             category_index,
                                                                                                             x_reference = roi,
                                                                                                             deviation = deviation,
                                                                                                             use_normalized_coordinates=True,
                                                                                                             line_thickness=4)

                # when the vehicle passed over line and counted, make the color of ROI line green
                if counter == 1:
                  cv2.line(input_frame, (roi, 0), (roi, height), (0, 0xFF, 0), 5)
                else:
                  cv2.line(input_frame, (roi, 0), (roi, height), (0, 0, 0xFF), 5)

                total_passed_vehicle = total_passed_vehicle + counter

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(
                    input_frame,
                    '0',
                    (827, 948),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    )
                cv2.putText(
                    input_frame,
                    '0',
                    (864, 730),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (893, 556),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (917, 419),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (939, 316),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (1506, 932),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (1460, 730),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (1412, 550),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (1371, 422),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                cv2.putText(
                    input_frame,
                    '0',
                    (1337, 317),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                #output_movie.write(input_frame)
                print ("writing frame")
                #cv2.imshow('object counting',input_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

def vlCouting_parcel_passed_line(vlParcelCollection, input_video, detection_graph, category_index, is_color_recognition_enabled, roi, roi_chutes, deviation, isShowFrame, isWriteVideoOutput):
  # input video
  cap = cv2.VideoCapture(input_video + ".mp4")
  #cap = cv2.VideoCapture('rtsp://admin:cntt@123@192.168.0.111')
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2)
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
  fps = int(cap.get(cv2.CAP_PROP_FPS))

  fourcc = cv2.VideoWriter_fourcc(*'X264')
  if isWriteVideoOutput:
    output_movie = cv2.VideoWriter(input_video + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + '.mp4', fourcc, fps, (width, height))

  # Declare variables
  old_chutes_count  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  chutes_count      =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  total_parcel = 0
  speed = "waiting..."
  direction = "waiting..."
  size = "waiting..."
  color = "waiting..."
  counting_mode = "..."
  width_heigh_taken = True

  with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
      # Definite input and output Tensors for detection_graph
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

      # Each box represents a part of the image where a particular object was detected.
      detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
      detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # couting frame handle
      frame_handled_count = 0;
      # for all the frames that are extracted from input video
      while(cap.isOpened()):
        ret, frame = cap.read()
        #print('Start process frame: ' + str(cap.get(1)) + '...')
        if not  ret:
            print("End processing...")
            break

        input_frame = frame

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(input_frame, axis=0)

        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        # insert information text to video frame
        font = cv2.FONT_HERSHEY_SIMPLEX

       # Visualization of the results of a detection.

        arr_box_counting, chutes_count, counter, csv_line = vis_util.vlVisualize_boxes_and_count(cap.get(1),
                                                                               input_frame,
                                                                               2,
                                                                               is_color_recognition_enabled,
                                                                               np.squeeze(boxes),
                                                                               np.squeeze(classes).astype(np.int32),
                                                                               np.squeeze(scores),
                                                                               category_index,
                                                                               y_reference=roi,
                                                                               chute_references=roi_chutes,
                                                                               deviation=deviation,
                                                                               use_normalized_coordinates=True,
                                                                               line_thickness=1)

        # Database handle
        arr_chute_count = [chutes_count[i] - old_chutes_count[i] for i in range(len(old_chutes_count))]
        old_chutes_count = chutes_count
        #print("arr_chute_count: ")
        #print(arr_chute_count)
        # start insert here
        for c in arr_box_counting:
          c[2] = c[2] * 1280
          c[3] = c[3] * 720
          c[4] = c[4]* 1280
          c[5] = c[5]* 720
          print("Insert  " + str(c) + " to databases")
          ret = vlParcelCollection.insert_one({"chuteno":       c[0],
                                               "timesorted":    datetime.now(),
                                               "path_image":    c[1],
                                               "coordination": [c[2], c[3], c[4], c[5]]
                                               })
          print(ret)
        # when the vehicle passed over line and counted, make the color of ROI line green
        #print("==================> Count in frame: " + str(counter))

        '''
        ********************************************************************************************************
                    --------------------------------------------------------------
                        THIS INPUT THE NUMBER OF PARCELS WHICH HAS BEEN SORTED
                        # insert information text to video frame
                    --------------------------------------------------------------
        ********************************************************************************************************
        '''
        for i in range(len(roi_chutes)):
          cv2.putText(input_frame, str(chutes_count[i]), (roi_chutes[i][0], roi_chutes[i][1]), font, 1, (0, 0xFF, 0xFF), 2)
        for roi_chute in roi_chutes:
          cv2.line(input_frame, (roi_chute[0], roi_chute[1]), (roi_chute[0], roi_chute[2]), (0, 0, 0xFF), 2,8)
        # cv2.putText(input_frame,', '.join(map(str, chutes_count)),(50, 125),font,0.6,(0, 0xFF, 0xFF),2,cv2.FONT_HERSHEY_SIMPLEX,)
        total_parcel = total_parcel + counter
        cv2.putText(input_frame, 'Frame process: ' + str(frame_handled_count), (50, 100), font, 0.8, (0, 0xFF, 0xFF), 2, cv2.FONT_HERSHEY_SIMPLEX)
        #cv2.putText(input_frame, ', '.join(map(str, chutes_count)), (50, 125), font, 0.6, (0, 0xFF, 0xFF), 2, cv2.FONT_HERSHEY_SIMPLEX,)
        if counter > 0:
          cv2.line(input_frame, (680, roi), (900, roi), (0, 0xFF, 0), 3, 8)
        else:
            cv2.line(input_frame, (680, roi), (900, roi), (0, 0, 0xFF), 3, 8)
        # couting for each chute

        if isShowFrame:
          # Display the resulting frame
          cv2.imshow('Vtp-Tracking', frame)

        if isWriteVideoOutput:
          #write result
          output_movie.write(input_frame)
        #Write log
        #print(str(chutes_count))
        #print("------ End process frame: " + str(cap.get(1)))
        frame_handled_count = frame_handled_count + 1
        # Press Q on keyboard to  exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
  return total_parcel, chutes_count

def object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled):

        # input video
        cap = cv2.VideoCapture(input_video)

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('the_output.avi', fourcc, fps, (width, height))

        total_passed_vehicle = 0
        speed = "waiting..."
        direction = "waiting..."
        size = "waiting..."
        color = "waiting..."
        counting_mode = "..."
        width_heigh_taken = True
        height = 0
        width = 0
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # for all the frames that are extracted from input video
            while(cap.isOpened()):
                ret, frame = cap.read()

                if not  ret:
                    print("end of the video file...")
                    break

                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.
                counter, csv_line, counting_mode = vis_util.visualize_boxes_and_labels_on_image_array(cap.get(1),
                                                                                                      input_frame,
                                                                                                      1,
                                                                                                      is_color_recognition_enabled,
                                                                                                      np.squeeze(boxes),
                                                                                                      np.squeeze(classes).astype(np.int32),
                                                                                                      np.squeeze(scores),
                                                                                                      category_index,
                                                                                                      use_normalized_coordinates=True,
                                                                                                      line_thickness=4)
                if(len(counting_mode) == 0):
                    cv2.putText(input_frame, "...", (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)
                else:
                    cv2.putText(input_frame, counting_mode, (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)

                output_movie.write(input_frame)
                print ("writing frame")
                #cv2.imshow('object counting',input_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

def object_counting_webcam(detection_graph, category_index, is_color_recognition_enabled):

        total_passed_vehicle = 0
        speed = "waiting..."
        direction = "waiting..."
        size = "waiting..."
        color = "waiting..."
        counting_mode = "..."
        width_heigh_taken = True
        height = 0
        width = 0
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            cap = cv2.VideoCapture(0)
            (ret, frame) = cap.read()

            # for all the frames that are extracted from input video
            while True:
                # Capture frame-by-frame
                (ret, frame) = cap.read()

                if not  ret:
                    print("end of the video file...")
                    break

                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.
                counter, csv_line, counting_mode = vis_util.visualize_boxes_and_labels_on_image_array(cap.get(1),
                                                                                                      input_frame,
                                                                                                      1,
                                                                                                      is_color_recognition_enabled,
                                                                                                      np.squeeze(boxes),
                                                                                                      np.squeeze(classes).astype(np.int32),
                                                                                                      np.squeeze(scores),
                                                                                                      category_index,
                                                                                                      use_normalized_coordinates=True,
                                                                                                      line_thickness=4)
                if(len(counting_mode) == 0):
                    cv2.putText(input_frame, "...", (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)
                else:
                    cv2.putText(input_frame, counting_mode, (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)

                cv2.imshow('object counting',input_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

def targeted_object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled, targeted_object):

        # input video
        cap = cv2.VideoCapture(input_video)

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('the_output.avi', fourcc, fps, (width, height))

        total_passed_vehicle = 0
        speed = "waiting..."
        direction = "waiting..."
        size = "waiting..."
        color = "waiting..."
        the_result = "..."
        width_heigh_taken = True
        height = 0
        width = 0
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # for all the frames that are extracted from input video
            while(cap.isOpened()):
                ret, frame = cap.read()

                if not  ret:
                    print("end of the video file...")
                    break

                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.
                counter, csv_line, the_result = vis_util.visualize_boxes_and_labels_on_image_array(cap.get(1),
                                                                                                      input_frame,
                                                                                                      1,
                                                                                                      is_color_recognition_enabled,
                                                                                                      np.squeeze(boxes),
                                                                                                      np.squeeze(classes).astype(np.int32),
                                                                                                      np.squeeze(scores),
                                                                                                      category_index,
                                                                                                      targeted_objects=targeted_object,
                                                                                                      use_normalized_coordinates=True,
                                                                                                      line_thickness=4)
                if(len(the_result) == 0):
                    cv2.putText(input_frame, "...", (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)
                else:
                    cv2.putText(input_frame, the_result, (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)

                #cv2.imshow('object counting',input_frame)

                output_movie.write(input_frame)
                print ("writing frame")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

def single_image_object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled):
        total_passed_vehicle = 0
        speed = "waiting..."
        direction = "waiting..."
        size = "waiting..."
        color = "waiting..."
        counting_mode = "..."
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')



        input_frame = cv2.imread(input_video)

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(input_frame, axis=0)

        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        # insert information text to video frame
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Visualization of the results of a detection.
        counter, csv_line, counting_mode = vis_util.visualize_boxes_and_labels_on_image_array_y_axis(cap.get(1),
                                                                                                     input_frame,
                                                                                                     2,
                                                                                                     is_color_recognition_enabled,
                                                                                                     np.squeeze(boxes),
                                                                                                     np.squeeze(
                                                                                                         classes).astype(
                                                                                                         np.int32),
                                                                                                     np.squeeze(scores),
                                                                                                     category_index,
                                                                                                     y_reference=roi,
                                                                                                     deviation=deviation,
                                                                                                     use_normalized_coordinates=True,
                                                                                                     line_thickness=1)
        if(len(counting_mode) == 0):
            cv2.putText(input_frame, "...", (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)
        else:
            cv2.putText(input_frame, counting_mode, (10, 35), font, 0.8, (0,255,255),2,cv2.FONT_HERSHEY_SIMPLEX)

        cv2.imshow('tensorflow_object counting_api',input_frame)
        cv2.waitKey(0)

        return counting_mode
