import GUI
import HAL
import cv2

# temps: 161.99s
i = 0
# Enter sequential code!
while True:
    im = HAL.getImage()
    
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv,
                            (0, 125, 125),
                            (30, 255, 255))
    contours, hierarchy = cv2.findContours(red_mask,
                                          cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])
    
    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
    else:
        cX, cY = 0, 0
    
    if cX > 0:
        err = 320 - cX
        HAL.setV(4.3)
        HAL.setW(0.01 * err)
    GUI.showImage(red_mask)
    i += 1
    print('%d cX: %.2f cY: %.2f' % (i, cX, cY))  
    # Enter iterative code!
