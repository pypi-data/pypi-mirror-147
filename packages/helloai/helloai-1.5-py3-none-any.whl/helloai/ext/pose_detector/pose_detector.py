#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

import cv2
import numpy as np
import mediapipe as mp
from collections import deque

from helloai.core.image import Image


__all__ = ['PoseDetector']

class PoseDetector:
    def __init__(self):
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_pose = mp.solutions.pose
        self.__pose = self.__mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.__landmarks = []
        self.load_model()
        
    def load_model(self):
        pass
    
    def process(self, image, draw=True):
        image = image.frame.copy()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.__pose.process(image) 
        
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            ret = []
            # ret = results.pose_landmarks

            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                ret.append([id, cx, cy, lm.z])

            self.__landmarks = ret
            if draw:
                self.__mp_drawing.draw_landmarks(image, 
                                             results.pose_landmarks, 
                                             self.__mp_pose.POSE_CONNECTIONS,
                                             self.__mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4), 
                                             self.__mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))
        else:
            ret = []
            self.__landmarks = ret
            
        return Image(image), self.__landmarks


    def calc_angle(self, image, p1, p2, p3, draw=True):
        image = image.frame.copy()
        
        x1, y1 = self.__landmarks[p1][1:3]
        x2, y2 = self.__landmarks[p2][1:3]
        x3, y3 = self.__landmarks[p3][1:3]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            image = cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 3)
            image = cv2.line(image, (x3, y3), (x2, y2), (255, 255, 255), 3)
            image = cv2.circle(image, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            image = cv2.circle(image, (x1, y1), 15, (0, 0, 255), 2)
            image = cv2.circle(image, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            image = cv2.circle(image, (x2, y2), 15, (0, 0, 255), 2)
            image = cv2.circle(image, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            image = cv2.circle(image, (x3, y3), 15, (0, 0, 255), 2)
            image = cv2.putText(image, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
    
    def distance(self, p1, p2, image, draw=True):
        image = image.frame.copy()
        r = 15
        t = 3
        x1, y1 = self.__landmarks[p1][1:3]
        x2, y2 = self.__landmarks[p2][1:3]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(image, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, image, [x1, y1, x2, y2, cx, cy]


    def __del__(self):
        if self.__pose:
            self.__pose.close()
