# NOTE: This script is based on this link: https://www.youtube.com/watch?v=jsoe1M2AjFk
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from speech import speech_recognition

# cascPath = "haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

detector = FaceMeshDetector(maxFaces=1)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()


    # NOTE: The focal length should be measured beforehand
    # measure the focal length
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if len(faces) != 1:
        continue
    face = faces[0]
    eyeLeft = face[145]
    eyeRight = face[374]
    # cv2.line(frame, eyeLeft, eyeRight, (0, 255, 0), 3)
    # cv2.circle(frame, eyeLeft, 5, (255, 0, 255), cv2.FILLED)
    # cv2.circle(frame, eyeRight, 5, (255, 0, 255), cv2.FILLED)

    # w is a distance in pixel
    w, _ = detector.findDistance(eyeLeft, eyeRight)

    # W is a distance between the left and right eye in cm
    # d is a distance between a camera and a face
    # f is the focal length
    W = 6.3
    # d = 30
    # f = (w * d) / W
    # print(f)

    # find the actual distance
    f = 630
    d = (W * f) / w
    print('*******this is the distance: *******')
    print(d)

    if d <= 30:
        print('You\'re in a range!! before speech_recognition')
        speech_recognition()
        print('You\'re in a range!! after speech_recognition')
    else:
        print('not in range')

    # TODO: make sure that we don't need to display the frame and get rid of the below
    # Display the resulting frame
    # cv2.imshow('Video', frame)
    # the below works only when imshow is executed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()