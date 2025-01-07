import GUI
import HAL
import cv2
import utm



# Enter sequential code!
# GPS coordinates of the safety boat and victim
boat_x = 40 + 16/60 + 48.2/3600
boat_y = -(3 + 49 / 60 + 3.5 / 3600)  # Negative because west

victim_x = 40 + 16/60 + 47.23/3600
victim_y = -(3 + 49 / 60 + 1.78 / 3600)  # Negative because west

#GPS to UTM
boat_coord = utm.from_latlon(boat_x, boat_y)
victim_coord = utm.from_latlon(victim_x, victim_y)

# We now have to calculate the initial difference in coordinates
b_v_diff_x = victim_coord[0] - boat_coord[0]
b_v_diff_y = victim_coord[1] - boat_coord[1]

# Takeoff to a height of 5 meters (This distance allows the drone to detect
  #the victims as well as their faces, if the height is higher it cannot detect
  #faces)
HAL.takeoff(5)

# Now we load Haar Cascade for face detection in the drone's camera image
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Creating functions
# To get and display drone images
def get_ims():
    front_im = HAL.get_frontal_image()

    GUI.showImage(front_im)
    #GUI.showLeftImage(vent_im)

    return front_im

def rotate(im, angle, center = None, scale = 1.0):
    (h, w) = im.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(im, M, (w, h))

    return rotated


# To calculate the yaw angle to face the target direction
def calculate_yaw(target_x, target_y):
    drone_position = HAL.get_position()
    diff_x = target_x - drone_position[0]
    diff_y = target_y - drone_position[1]
    yaw = math.atan2(diff_y, diff_x)  # Calculate yaw angle in radians
    return yaw

# List for saving the victim's positions
victim_positions = []

# Main loop: for navigation and face detection

while True:

    #if drone_position[0] != victim_coord[0] and drone_position[1] != victim_coord[1]:

    drone_position = HAL.get_position()
    # Calculate yaw so the drone faces the victim's location
    yaw_angle = calculate_yaw(b_v_diff_x, b_v_diff_y)

    # Command the drone to move towards the victim's location
    HAL.set_cmd_pos(b_v_diff_x, b_v_diff_y, 5, yaw_angle)

  
        # code

    print("position", drone_position)
    print(b_v_diff_x,b_v_diff_y)

    # Capture frontal image from the drone
    img = get_ims()

    # Convert the image to grayscale for face detection
    gray_im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_im, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))
    #rotated_faces = rotate(gray_im, -30)
     
    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # If faces are detected, save the drone's current position
    if len(faces) > 0:
        victim_position.append(drone_position)
        print(f"Victim detected at: {drone_position}")

    # Display the image with detected faces
    GUI.showLeftImage(img)

    # Check if the drone is close to the victim's coordinates
    distance_to_victim = math.sqrt((drone_position[0] - b_v_diff_x)**2 + (drone_position[1] - b_v_diff_y)**2)
    if distance_to_victim < 1.0:  # Stop when close to the victim
        print("Reached victim's location")
        break

# Command the drone to return to the initial position (boat coordinates), once all
  # victims are detected
print("Returning to boat...")
yaw_angle_to_boat = calculate_yaw(boat_coord[0], boat_coord[1])
HAL.set_cmd_pos(boat_coord[0], boat_coord[1], 5, yaw_angle_to_boat)

# Wait until the drone is back to the initial position
while True:
    drone_position = HAL.get_position()
    distance_to_boat = math.sqrt((drone_position[0] - boat_coord[0])**2 + (drone_position[1] - boat_coord[1])**2)
    if distance_to_boat < 1.0:
        break

# Land after returning to the initial position
HAL.land()

# Print all saved victim positions
print("Victim positions:")
for pos in victim_positions:
    print(pos)



#while True:
    # Enter iterative code!
    #control = HAL.set_cmd_pos(x, y, z, az)
    
    #if boat_coord != victim_coord


