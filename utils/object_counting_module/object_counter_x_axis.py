from utils.image_utils import image_saver

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]
# M02
roi_chutes = [[0, 515, 528, 710], [1, 545, 393, 535], [2, 571, 292, 400],
              [3, 591, 218, 298], [4, 608, 160, 222], [5, 620, 115, 161],
              [6, 1045, 515, 700], [7, 1007, 389, 530], [8, 970, 292, 397],
              [9, 939, 218, 299], [10,911, 160, 222], [11,888, 115, 164]]
# M16
# roi_chutes = [[0, 315, 563, 720], [1, 335, 428, 574], [2, 370, 338, 436],
#               [3, 399, 268, 340], [4, 420, 216, 271], [5, 436, 175, 218],
#               [6, 936, 518, 720], [7, 869, 393, 538], [8, 813, 308, 410],
#               [9, 772, 243, 315], [10,743, 195, 240], [11,720, 156, 200]]
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