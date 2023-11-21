# NOTE: This script is based on this link: https://www.youtube.com/watch?v=jsoe1M2AjFk
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.FaceDetectionModule import FaceDetector

class WebCamera:
    def __init__(self) -> None:
        self.video_capture = cv2.VideoCapture(1)
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

        return width, frame


    def __del__(self) -> None:
        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()