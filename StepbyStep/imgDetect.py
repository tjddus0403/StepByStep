import tensorflow as tf
import numpy as np
import cv2
#import argparse
import os
import posenet

args = {"model":101, "scale_factor":1.0, "notxt":False}
#우리가 사용할 자세가 있는 이미지를 넣어서 좌표 기억을 시켜줘야 하는 듯?
#args = {"model":101, "scale_factor":1.0, "notxt":False, "image_dir":"./images", "output_dir":"./output"}

    