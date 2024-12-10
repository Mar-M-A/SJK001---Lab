import GUI
import HAL
import cv2
import utm



# Enter sequential code!

boat_x = 40 + 16/60 + 48.2/3600
boat_y = 3 + 49/60 + 3.5/3600

victim_x = 40 + 16/60 + 47.23/3600
victim_y = 3 + 49/60 + 1.78/3600

#UTM
boat_coord = utm.from_latlon(boat_x, boat_y)
victim_coord = utm.from_latlon(victim_x, victim_y)

HAL.takeoff(3)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_ims():
    front_im = HAL.get_frontal_image()
    vent_im = HAL.get_ventral_image()

    GUI.showImage(front_im)
    #GUI.showLeftImage(vent_im)

    return vent_im

def rotate(im, angle, center = None, scale = 1.0):
    (h, w) = im.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(im, M, (w, h))

    return rotated


b_v_diff_x = -(victim_coord[0] - boat_coord[0])
b_v_diff_y = victim_coord[1] - boat_coord[1] 

b_v_diff_x = 38
b_v_diff_y = -31

drone_position = HAL.get_position()

get_ims()

victim_position = []

while True:
    
    #if drone_position[0] != victim_coord[0] and drone_position[1] != victim_coord[1]:

    drone_position = HAL.get_position()
    drone_move = HAL.set_cmd_pos(b_v_diff_x, b_v_diff_y, 3, 0)
  
        # code

    print("position", drone_position)
    print(b_v_diff_x,b_v_diff_y)

    img = rotate(get_ims(),-30)

    gray_im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_im, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))
    #rotated_faces = rotate(gray_im, -30)
     
    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    if len(faces) > 0:
        victim_position.append(drone_position)

    print(len(faces))
    print(faces)
    GUI.showLeftImage(img)
 



#while True:
    # Enter iterative code!
    #control = HAL.set_cmd_pos(x, y, z, az)
    
    #if boat_coord != victim_coord


