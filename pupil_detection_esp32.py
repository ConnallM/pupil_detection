import cv2
import math
import urllib.request
import urllib.parse
import numpy as np
import requests

url = 'http://192.168.2.220/cam-hi.jpg'
cam = cv2.VideoCapture(url)
if not cam.isOpened():
 print("Cannot open camera")
 exit()

#def captureFrames():

def detectPupil():
    parse_url = urllib.parse.urlparse(url)
    #print(parse_url)
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    # ret, frame = cap.read()
    image_colour = cv2.imdecode(imgnp, -1)

    raw_image = cv2.cvtColor(image_colour, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('Original Image', image_colour)
    #cv2.waitKey(0)
    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    ret,thresh = cv2.threshold(bilateral_filtered_image,32,255,cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(raw_image, contours,  -1, (255,0,0), 2)
    cv2.imshow('Objects Detected',raw_image)

    contour_list = []
    radii = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01 *cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) and (len(approx) < 23) and (area > 50) and (area < 10000)):
            (x_axis, y_axis), radius = cv2.minEnclosingCircle(contour)
            area_ratio = math.pi * radius**2 / cv2.contourArea(contour)
            if (area_ratio < 1.5 and area_ratio > 1):
                contour_list.append(contour)
                radii.append(radius)
                cv2.circle(image_colour, (int(x_axis), int(y_axis)), int(radius), (0, 255, 0), 2)
                #cv2.imshow('Pupil Detected', image_colour)

    cv2.imshow('Pupil Detected', image_colour)

    #cv2.drawContours(raw_image, contour_list,  -1, (255,0,0), 2)

    #cv2.imshow('Objects Detected',raw_image)
    #cv2.waitKey(0)
    if len(radii) > 0:
        return sum(radii)/len(radii)
    else:
        return 0

def main():
    while(cam.isOpened()):
        detectPupil()
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
main()
