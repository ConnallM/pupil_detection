import cv2
import math
cam = cv2.VideoCapture(0)
if not cam.isOpened():
 print("Cannot open camera")
 exit()

def detectPupil():
    result, image_colour = cam.read()
    raw_image = cv2.cvtColor(image_colour, cv2.COLOR_BGR2GRAY)

    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    ret,thresh = cv2.threshold(bilateral_filtered_image,32,255,cv2.THRESH_BINARY)
    ret, thresh_high = cv2.threshold(bilateral_filtered_image, 64, 255, cv2.THRESH_BINARY)
    #cv2.imshow("Threshed", thresh_high)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, hierarchy = cv2.findContours(thresh_high, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(raw_image, contours,  -1, (0,255,0), 2)
    #cv2.drawContours(raw_image, contours2, -1, (0, 255, 0), 2)
    #cv2.imshow('Objects Detected',raw_image)

    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) and (len(approx) < 23) and (area > 50) and (area < 10000)):
            (x_axis, y_axis), radius = cv2.minEnclosingCircle(contour)
            area_ratio = math.pi * radius**2 / cv2.contourArea(contour)
            if (area_ratio < 1.5 and area_ratio > 1):
                for contour2 in contours2:
                    approx2 = cv2.approxPolyDP(contour2, 0.01 * cv2.arcLength(contour2, True), True)
                    area2 = cv2.contourArea(contour2)
                    if ((len(approx2) > 8) and (len(approx2) < 23) and (area2 > 100) and (area2 < 10000)):
                        (x_axis2, y_axis2), radius2 = cv2.minEnclosingCircle(contour2)
                        area_ratio2 = math.pi * radius2 ** 2 / cv2.contourArea(contour2)
                        if (area_ratio2 < 2 and area_ratio2 > 1):
                            if (x_axis < x_axis2 + radius/2 and x_axis > x_axis2 - radius/2) and (y_axis < y_axis2 + radius and y_axis > y_axis2 - radius):
                                contour_list.append(contour)
                                contour_list.append(contour2)
                                cv2.circle(image_colour, (int(x_axis), int(y_axis)), int(radius), (0, 255, 0), 2)
                                #cv2.circle(image_colour, (int(x_axis2), int(y_axis2)), int(radius2), (255, 0, 0), 2)

    cv2.imshow('Pupil Detected', image_colour)

def main():
    while(cam.isOpened()):
        detectPupil()
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
main()
