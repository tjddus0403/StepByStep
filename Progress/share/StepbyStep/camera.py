import tensorflow as tf
import numpy as np
import cv2
import posenet
import time
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

args = {"model": 101, "scale_factor": 1.0, "notxt": True, "image_dir": './images',
        "output_dir": './output'}
position = ["코", "왼쪽눈", "오른쪽눈", "왼쪽귀", "오른쪽귀", "왼쪽어깨", "오른쪽어깨", "왼쪽팔꿈치", "오른쪽팔꿈치",
            "왼쪽손목", "오른쪽손목", "왼쪽골반부위", "오른쪽골반부위", "왼쪽무릎", "오른쪽무릎", "왼쪽발목", "오른쪽발목"]

class VideoCamera(object):
    def __init__(self):
        self.cap=cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

def gen(camera):
    with tf.compat.v1.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args['model'], sess)
        #모델에서 output_stride 가져오는 듯
        output_stride = model_cfg['output_stride']
        start=time.time()
        while True:
            input_img, display_img, output_scale = posenet.read_cap(
                camera.cap, scale_factor=args['scale_factor'], output_stride = output_stride)

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs, feed_dict={'image:0':input_img})

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10, 
                min_pose_score=0.15)
            
            overlay_img=posenet.draw_skel_and_kp(
                display_img, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            overlay_img=cv2.resize(overlay_img, dsize=(1240, 920), interpolation=cv2.INTER_AREA)

            overlay_img=cv2.flip(overlay_img,1)

            _, img= cv2.imencode('.jpg', overlay_img)
            frame=img.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')