from __future__ import print_function
import cv2 as cv
import argparse
import base64


def detFace(cap):
    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.equalizeHist(frame_gray)

        faces = face_cascade.detectMultiScale(frame_gray)
        cv.waitKey(1000000000)
        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            frame = cv.ellipse(frame, center, (w//2, h//2),
                               0, 0, 360, (255, 0, 255), 4)
        #cv.imshow('Capture - Face detection', frame)
        # cv.waitKey(10000)
        try:
            if ret:
                framesnumpy = frame.tostring()
                framesnumpy = base64.b64encode(framesnumpy)
            else:
                framesnumpy = "ignore"

            return framesnumpy

        except Exception as exc:
            print("Exception caught")
            raise exc

        # return frame

    #cv.imshow('Capture - Face detection', frame)
    # cv.waitKey(1000)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Face Detector')
    parser.add_argument('--face_cascade', help='Path to face cascade.',
                        default='../../opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
    parser.add_argument(
        '--camera', help='Camera devide number.', type=int, default=0)
    args = parser.parse_args()

    face_cascade_name = args.face_cascade

    face_cascade = cv.CascadeClassifier()

    if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(0)
    cap = cv.VideoCapture(args.camera)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)

    print(detFace(cap))
    #cv.imshow('Capture - Face detection', detFace(cap))
    # cv.waitKey(10000)
