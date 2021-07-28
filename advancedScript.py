import cv2
import mediapipe as mp
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume.iid, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

vol = volume.GetVolumeRange()
print(vol)
minVolume = vol[0]
maxVolume = vol[1]

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    multiLandMarks = results.multi_hand_landmarks
    if multiLandMarks:
        # bad main add karna hai ye chunk
        indexPoint = ()
        thumbPoint = ()
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                print(id, lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)
                if id == 4:
                    thumbPoint = (cx,cy)
                if id == 8:
                    indexPoint = (cx,cy)
        print(indexPoint,thumbPoint)
        cv2.circle(img,indexPoint, 15, (255,255,0 ), cv2.FILLED)
        cv2.circle(img,thumbPoint, 15, (255,255,0 ), cv2.FILLED)
        cv2.line(img, indexPoint, thumbPoint, (255,255,0 ), 3)

        distance = math.sqrt(((indexPoint[0] - thumbPoint[0]) * 2) + ((indexPoint[1] - thumbPoint[1]) * 2))
        print(distance)
        if distance < 50:
            cv2.circle(img, indexPoint, 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, thumbPoint, 15, (0, 0, 255), cv2.FILLED)
        if distance > 260:
            cv2.circle(img, indexPoint, 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, thumbPoint, 15, (0, 255, 0), cv2.FILLED)

        vol = np.interp(distance, [50,260], [minVolume, maxVolume])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
    cv2.imshow("Img", img)
    cv2.waitKey(1)