import cv2
import numpy as np
import time

import PoseModule as pm
from tkinter import *

workout_list = ['right_bicep_curl', 'left_bicep_curl', "squat"]


def openWorkoutCustomization():
    top = Tk(className='Customize your Workout!')
    top.config(bg="blue")
    top.title("Customize Your Workout!")
    top.geometry("900x600")

    variable = StringVar(top)
    variable.set(workout_list[0])

    w = OptionMenu(top, variable, *workout_list)
    w.pack()

    button = Button(top, text="Start", command=lambda: startWorkout(variable.get()))
    button.pack()

    top.mainloop()


def showBar(workout, angle, img, count):
    if workout == "right_bicep_curl":
        per_right = np.interp(angle, (200, 330), (0, 100))
        bar = np.interp(angle, (200, 330), (650, 100))
        # Draw bar
        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per_right)}', (1100, 75), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 0, 0), 4)

        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN,
                    15, (255, 0, 0), 25)
    if workout == "left_bicep_curl":
        per_left = np.interp(angle, (35, 170), (100, 0))
        bar = np.interp(angle, (35, 170), (100, 650))
        # Draw bar
        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per_left)}', (1100, 75), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 0, 0), 4)

        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN,
                    15, (255, 0, 0), 25)


def showMultiBar(workout, angle_right, angle_left, img, count):
    if workout == "squat":

        per_squat_right = np.interp(angle_right, (70, 170), (100, 0))
        per_squat_left = np.interp(angle_left, (190, 280), (0, 100))

        bar_right = np.interp(angle_right, (70, 170), (100, 650))
        bar_left = np.interp(angle_left, (190, 280), (650, 100))

        # Draw right bar
        cv2.rectangle(img, (1200, 100), (1275, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1200, int(bar_right)), (1275, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per_squat_right)}', (1200, 75), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 0, 0), 4)

        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar_left)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per_squat_left)}', (1100, 75), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 0, 0), 4)

        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN,
                    15, (255, 0, 0), 25)

def startWorkout(workoutType):
    print(workoutType)
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    count = 0
    dir = 0
    pTime = 0

    workout = workoutType

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:

            if workout == "right_bicep_curl":
                angle_right = detector.findAngle(img, 12, 14, 16)
                per_right = np.interp(angle_right, (200, 330), (0, 100))
                bar = np.interp(angle_right, (200, 330), (650, 100))
                if per_right == 100:
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per_right == 0:
                    if dir == 1:
                        count += 0.5
                        dir = 0
                showBar("right_bicep_curl", angle_right, img, count)
            elif workout == "left_bicep_curl":
                angle_left = detector.findAngle(img, 11, 13, 15)
                per_left = np.interp(angle_left, (35, 170), (100, 0))
                if per_left == 100:
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per_left == 0:
                    if dir == 1:
                        count += 0.5
                        dir = 0
                showBar("left_bicep_curl", angle_left, img, count)
            # Right Arm min=180 max=340 0, 0), 5)
            elif workout == "squat":
                angle_squat_right = detector.findAngle(img, 24, 26, 28)
                angle_squat_left = detector.findAngle(img, 23, 25, 27)

                per_squat_right = np.interp(angle_squat_right, (70, 170), (0, 100))
                per_squat_left = np.interp(angle_squat_left, (190, 280), (100, 0))

                print("Left: " + str(int(per_squat_left)) + " | Right: " + str(int(per_squat_right)))

                if per_squat_right and per_squat_left == 0:
                    if dir == 0:
                        count += 0.5
                        dir = 1
                    if dir == 1:
                        count += 0.5
                        dir = 0
                if per_squat_left and per_squat_right == 100:
                    if dir == 0:
                        count += 0.5
                        dir = 1
                    if dir == 1:
                        count += 0.5
                        dir = 0


                showMultiBar("squat", angle_squat_right, angle_squat_left, img, count)

                # print("Left: " + str(int(angle_squat_left)) + " | Right: " + str(int(angle_squat_right)))

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (50, 100),
                        cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # cv2.createButton("Customize", openWorkoutCustomization(), None, cv2.QT_PUSH_BUTTON, 1)
        cv2.imshow("AI Personal Trainer", img)
        cv2.waitKey(1)

openWorkoutCustomization()
