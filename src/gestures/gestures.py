#Set to True to show differences between frames instead
#of frames themselves

SHOW_DIFF = False
SHOW_OPTICAL_FLOW = False
SHOW_MOTION_DIRECTION = True
WIN_NAME = 'Gestures'

#Check to see if we have opencv installed
import sys

try:
    import cv2
except ImportError:
    print 'FATAL: Failed to find opencv'
    sys.exit(1)

import cv2.cv as cv

from algorithm import absdiff, create_flow, update_mhi
from webcam import Webcam

class Gestures():
    def __init__(self):
        #initialize the webcam
        #self.camera = Webcam()
        self.motion = 0
        self.capture = 0

        if len(sys.argv)==1:
            self.capture = cv.CreateCameraCapture(0)
        elif len(sys.argv)==2 and sys.argv[1].isdigit():
            self.capture = cv.CreateCameraCapture(int(sys.argv[1]))
        elif len(sys.argv)==2:
            self.capture = cv.CreateFileCapture(sys.argv[1]) 

        if not self.capture:
            print "Could not initialize capturing..."
            sys.exit(-1)
        
        #initialize the video window
        cv2.namedWindow(WIN_NAME, cv2.CV_WINDOW_AUTOSIZE)
    
    def start(self):
        #Get 3 successive frames for difference calculation
        #frame0 = self.camera.get_frame_gray()
        #frame1 = self.camera.get_frame_gray()
        #frame2 = self.camera.get_frame_gray()

        while True:
            if SHOW_MOTION_DIRECTION:
                image = cv.QueryFrame(self.capture)
                if(image):
                    if(not self.motion):
                            self.motion = cv.CreateImage((image.width, image.height), 8, 3)
                            cv.Zero(self.motion)
                update_mhi(image, self.motion, 30)
            elif SHOW_OPTICAL_FLOW: #Show optical flow field
                #this single method does the magic of computing the optical flow
                flow = cv2.calcOpticalFlowFarneback(frame0, frame1, 0.5, 3, 15, 3, 5, 1.2, 0)
                image = create_flow(frame1, flow, 10) #create the flow overlay for display
                frame0 = frame1
                frame1 = self.camera.get_frame_gray()
            elif SHOW_DIFF: #Show image difference feed
                image = absdiff(frame0, frame1, frame2)
                frame0 = frame1
                frame1 = frame2
                frame2 = self.camera.get_frame_gray()
            else: #Just show regular webcam feed
                image = frame0
                frame0 = self.camera.get_frame()
            
            #self.show_image(image)
            cv.ShowImage("Motion", self.motion)

            #Quit if the user presses ESC
            key = cv2.waitKey(4)
            if key == 27:
                self.stop_gui()
                break
    

    #Show a GUI with the webcam feed for debugging purposes
    def show_image(self,img):
        cv2.imshow(WIN_NAME, img)
    
    #Stop the webcam
    def stop_gui(self):
        cv2.destroyWindow(WIN_NAME)
    