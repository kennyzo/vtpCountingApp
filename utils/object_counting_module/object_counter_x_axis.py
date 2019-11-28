from utils.image_utils import image_saver

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]
roi_chutes = [[0, 536, 563, 716], [1, 565, 432, 546], [2, 588, 316, 415], [3, 605, 238, 318], [4, 615, 176, 241], [5, 630, 131, 181],
              [6, 1023, 534, 711], [7, 992, 412, 550], [8, 958, 312, 419], [9, 930, 242, 320], [10, 904, 180, 244], [11, 882, 125, 184]]
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
  if abs(y_coordinate - roi_position) < deviation:
    is_parcel_passed_total_line = True
    image_saver.save_image(crop_img)  # save detected object image
  for chute in roi_chutes:
    if abs(x_coordinate - chute[1]) < deviation and bottom > chute[2] and top < chute[3]:
    #if abs(x_coordinate - chute[1]) < deviation:
      return is_parcel_passed_total_line,chute[0]

  return is_parcel_passed_total_line, -1