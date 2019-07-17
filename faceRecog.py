from __future__ import print_function
import cv2 as cv
import argparse
import base64
import time
import redis
class FacRecog:
    def __init__(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        parser = argparse.ArgumentParser(description='Face Detector')
        parser.add_argument('--face_cascade', help='Path to face cascade.',
                            default='../../opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
        parser.add_argument(
            '--camera', help='Camera devide number.', type=int, default=0)
        args = parser.parse_args()

        face_cascade_name = args.face_cascade

        self.face_cascade = cv.CascadeClassifier()

        if not self.face_cascade.load(cv.samples.findFile(face_cascade_name)):
            print('--(!)Error loading face cascade')
            exit(0)
        cap = cv.VideoCapture(args.camera)
        if not cap.isOpened:
            print('--(!)Error opening video capture')
            exit(0)
        self.reulsts = []
        frameNum = 0
        t_end = time.time() + 60 * 1
        # while(True)
        while time.time() < t_end:
            # Althoug I added a sequence number for the frames 
            # the issue i am having is due to the nature of redis 
            # it does not maintain order
            # I need to modify this so it only returns wehn the frame has a face detected
            frame = self.detFace(cap)
            cv.imwrite("./capture.jpg", frame)
            with open('./capture.jpg', 'rb') as imag:
                encoded_string = base64.b64encode(imag.read())
            self.foundFrame = encoded_string
            toPass = self.getFoundFrame()
            if
            r.set(str(frameNum),toPass)
            self.reulsts.append(self.foundFrame)
            frameNum += 1
            time.sleep(.5)
    def getFoundFrame(self):
        stringS = str(self.foundFrame)
        stringS = stringS[2:]
        stringS = stringS[:-1]
        self.foundFrame = "data:image/jpeg;base64," + stringS
        return "data:image/jpeg;base64," + stringS
    def detFace(self, cap):
        while True:
            ret, frame = cap.read()
            if frame is None:
                print('--(!) No captured frame -- Break!')

            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame_gray = cv.equalizeHist(frame_gray)

            faces = self.face_cascade.detectMultiScale(frame_gray)
            cv.waitKey(1000000000)
            for (x, y, w, h) in faces:
                center = (x + w//2, y + h//2)
                frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            return frame