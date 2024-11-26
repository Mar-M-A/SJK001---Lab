import GUI
import HAL
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

def get_ims():
    front_im = HAL.get_frontal_image()
    vent_im = HAL.get_ventral_image()

    GUI.showImage(front_im)
    GUI.showLeftImage(vent_im)

b_v_diff_x = -(victim_coord[0] - boat_coord[0])
b_v_diff_y = victim_coord[1] - boat_coord[1] 

drone_position = HAL.get_position()

get_ims()

while True:
    
    #if drone_position[0] != victim_coord[0] and drone_position[1] != victim_coord[1]:

    drone_position = HAL.get_position()
    drone_move = HAL.set_cmd_pos(b_v_diff_x, b_v_diff_y, 3, 0)
  
        # code

    print("position", drone_position)
    print(b_v_diff_x,b_v_diff_y)

    get_ims()



#while True:
    # Enter iterative code!
    #control = HAL.set_cmd_pos(x, y, z, az)
    
    #if boat_coord != victim_coord
