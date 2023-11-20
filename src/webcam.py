# NOTE: This script is based on this link: https://www.youtube.com/watch?v=jsoe1M2AjFk
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.FaceDetectionModule import FaceDetector
# from speech import speech_recognition

# cascPath = "haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascPath)
class WebCamera:
    def __init__(self) -> None:
        self.video_capture = cv2.VideoCapture(1)
##        self.detector = FaceMeshDetector(maxFaces=1)
        self.detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)
        self.focalLength = 630
        self.distBtwEyes = 6.3
        self.threshold = 350 # (in px) it should be either input or global variable

    # TODO:
    # I should make a function to calculateFocalLength
    def calculateFocalLength(self) -> None:
        print(f"Focal Length is set to {self.focalLength}!")

    # TODO:
    # I should make a setter for distBtwEyes
    
    # TODO:
    # I should specify the return value
    def calculateDistance(self):
        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

##        frame, faces = self.detector.findFaceMesh(frame, draw=True)
        img, bboxs = self.detector.findFaces(frame, draw=False)

        width = -1

        if bboxs:
            bbox = bboxs[0]
            x, y, w, h = bbox['bbox']
            center = bbox['center']

            color = (0, 0, 255)

            if w >= self.threshold:
                color = (0, 255, 0)

            cv2.rectangle(img, (x, y, w, h), color, 5)
            width = w

##        if len(faces) != 1:
##            return None, frame
##        face = faces[0]
##        eyeLeft = face[145]
##        eyeRight = face[374]
##        # cv2.line(frame, eyeLeft, eyeRight, (0, 255, 0), 3)
        # cv2.circle(frame, eyeLeft, 5, (255, 0, 255), cv2.FILLED)
        # cv2.circle(frame, eyeRight, 5, (255, 0, 255), cv2.FILLED)

        # w is a distance in pixel
##        w, _ = self.detector.findDistance(eyeLeft, eyeRight)

        # W is a distance between the left and right eye in cm
        # d is a distance between a camera and a face
        # f is the focal length
        # W = 6.3
        # d = 30
        # f = (w * d) / W
        # print(f)

        # find the actual distance
##        # f = 630
##        d = (self.distBtwEyes * self.focalLength) / w
##
##        print('*******this is the distance: *******')
##        print(width)

        return width, frame
        # if d <= 30:
        #     print('You\'re in a range!! before speech_recognition')
        #     if speech_recognition():
        #         print("The door is open")
        #         # call a function that opens the door
        #     else:
        #         if speech_recognition():
        #             print("The door is open this time")
        #         else:
        #             print("Come back later")
        #     print('You\'re in a range!! after speech_recognition')
        # else:
        #     print('not in range')

    # TODO: make sure that we don't need to display the frame and get rid of the below
    # Display the resulting frame
    # cv2.imshow('Video', frame)
    # the below works only when imshow is executed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    def __del__(self) -> None:
        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

""""
if __name__ == '__main__':
    webCamera = WebCamera()
    
    while True:
        d = webCamera.calculateDistance()
        if d <= 30.0:
            print('You\'re in a range!! before speech_recognition')
            if speech_recognition():
                print("The door is open")
                # call a function that opens the door
            else:
                if speech_recognition():
                    print("The door is open this time")
                else:
                    print("Come back later")
            print('You\'re in a range!! after speech_recognition')
            continue
        else:
            print('not in range')
"""
