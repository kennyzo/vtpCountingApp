from utils.image_utils import image_saver

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]
roi_chutes = [[0, 132, 450, 619], [1, 156, 316, 452], [2, 174, 214, 318],
              [3, 188, 138, 215], [4, 200, 79, 140],  [5, 210, 030, 80],
              [6, 557, 444, 612], [7, 523, 313, 440], [8, 495, 214, 312],
              [9, 470, 137, 211], [10,450, 80, 134],  [11,432, 31,  76]]
''' [chute no, x_line, ymin, ymax]'''
def count_objects_x_axis(top, bottom, right, left, crop_img, roi_position, y_min, y_max, deviation):
        direction = "n.a." # means not available, it is just initialization
        isInROI = True # is the object that is inside Region Of Interest
        update_csv = False

        if (abs(((right+left)/2)-roi_position) < deviation):
          is_vehicle_detected.insert(0,1)
          update_csv = True
          image_saver.save_image(crop_img) # save detected object image

        if(bottom > bottom_position_of_detected_vehicle[0]):
                direction = "down"
        else:
                direction = "up"

        bottom_position_of_detected_vehicle.insert(0,(bottom))

        return direction, is_vehicle_detected, update_csv


def vlCount_objects_x_axis(top, bottom, right, left, crop_img, roi_position, deviation):
  is_parcel_passed = False
  distance = abs((right + left) / 2) - roi_position
  print("Distance of box center and roi line: " + str(distance))
  if distance < deviation:
    is_parcel_passed = True
    image_saver.save_image(crop_img)  # save detected object image
  print("box pass line: " + str(is_parcel_passed))
  return is_parcel_passed

def vlCount_objects_y_axis(top, bottom, right, left, crop_img, roi_position, deviation):
  is_parcel_passed_total_line = False
  y_coordinate = (bottom + top) / 2
  x_coordinate = (left + right) / 2
  #print("Distance of box center and roi line: " + str(distance))
  if (bottom < roi_position) and (roi_position - bottom) < deviation:
    is_parcel_passed_total_line = True
    image_saver.save_image(crop_img)  # save detected object image
  for i in range(len(roi_chutes)):
    if i < 6:
      if (right < roi_chutes[i][1]) and (roi_chutes[i][1] - right) < deviation and top > roi_chutes[i][2] and bottom < roi_chutes[i][3]:
        #if abs(x_coordinate - chute[1]) < deviation:
        return is_parcel_passed_total_line,roi_chutes[i][0]
    else:
      if (left > roi_chutes[i][1]) and (left - roi_chutes[i][1]) < deviation and top > roi_chutes[i][2] and bottom < roi_chutes[i][3]:
        #if abs(x_coordinate - chute[1]) < deviation:
        return is_parcel_passed_total_line,roi_chutes[i][0]

  return is_parcel_passed_total_line, -1
