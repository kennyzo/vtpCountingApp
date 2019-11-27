from utils.image_utils import image_saver

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]

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
  is_parcel_passed = False
  distance = abs(((bottom + top) / 2) - roi_position)
  print("Distance of box center and roi line: " + str(distance))
  if distance < deviation:
    is_parcel_passed = True
    image_saver.save_image(crop_img)  # save detected object image
  print("box pass line: " + str(is_parcel_passed))
  return is_parcel_passed