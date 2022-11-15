import tensorflow as tf
import numpy as np
import cv2
from posenet import *
from posenet import DegreeOfSpinalCurve
from posenet import SpineLine
from posenet import DegreeOfArm
from posenet import FootStepSize
import time
np.set_printoptions(threshold=np.inf, linewidth=np.inf)
import json
import math

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

args = {"model": 101, "scale_factor": 1.0, "notxt": True, "image_dir": './images',
        "output_dir": './output'}
position = ["코", "왼쪽눈", "오른쪽눈", "왼쪽귀", "오른쪽귀", "왼쪽어깨", "오른쪽어깨", "왼쪽팔꿈치", "오른쪽팔꿈치",
            "왼쪽손목", "오른쪽손목", "왼쪽골반부위", "오른쪽골반부위", "왼쪽무릎", "오른쪽무릎", "왼쪽발목", "오른쪽발목"]
spine_position = ["척추상", "척추중", "척추하", "머리중심"]

def getAverage(pos, n):
    x, y = 0, 0
    for i in range(n):
        x += pos[i][0]
        y += pos[i][1]
    return [x/n, y/n]

class VideoCamera(object):
    def __init__(self):
        self.cap=cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

def gen(camera):
    file_path="./info.json"
    data={}
    data['post']=[]
    with tf.compat.v1.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args['model'], sess)
        output_stride = model_cfg['output_stride']
        # 걸음걸이 측정 시간 10초 타이머 시작
        start=time.time()
        while True:
            result1 = []
            result2 = []
            result3 = []
            result4 = []

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

            # 척추상, 척추중, 척추하, 목뼈시작 point 추가하기
            spineTop = getAverage(
                [keypoint_coords[0][5], keypoint_coords[0][6]], 2)
            spineMiddle = getAverage(
                [keypoint_coords[0][5], keypoint_coords[0][6], keypoint_coords[0][11], keypoint_coords[0][12]], 4)
            spineBottom = getAverage(
                [keypoint_coords[0][11], keypoint_coords[0][12]], 2)
            centerhead = getAverage(
                [keypoint_coords[0][3], keypoint_coords[0][4]], 2)
            spine_pos = [spineTop, spineMiddle, spineBottom, centerhead]

            for i in range(4):
                tmp = np.array([[spine_pos[i]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[
                    0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]]])
                keypoint_coords = np.concatenate(
                    (keypoint_coords, tmp), axis=1)
                keypoint_scores = np.concatenate(
                    (keypoint_scores, np.array([[1], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00]])), axis=1)                    
            position.extend(spine_position)
            keypoint_coords *= output_scale
            
            #목숙임, 허리숙임, 팔흔들림, 보폭크기 정도를 측정하여 info.json에 들어갈 result로 저장해둠
            result1.append(posenet.DegreeOfSpinalCurve.SpineCurve(keypoint_coords[0]))
            result2.append(posenet.SpineLine.SpineLine(keypoint_coords[0]))
            result3.append(posenet.DegreeOfArm.diagnose_Arm(keypoint_coords[0]))
            result4.append(posenet.FootStepSize.diagnose_footsize(keypoint_coords[0]))
            
            if(time.time()-start>10):
                break
            #정확도가 어느정도 충족되는 결과만 캠 화면에 점으로 나타나게 함 (우리가 보는 점들은 어느정도 정확도가 있는 것임)
            overlay_img=posenet.utils.draw_skel_and_kp(
                display_img, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            overlay_img=cv2.resize(overlay_img, dsize=(1240, 920), interpolation=cv2.INTER_AREA)

            overlay_img=cv2.flip(overlay_img,1)

            _, img= cv2.imencode('.jpg', overlay_img)
            frame=img.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            #info.json에 들어갈 데이터 형식대로 저장
            data['post'].append({'result1': result1,
                                'result2' : result2,
                                'result3' : result3,
                                'result4' : result4})
            #info.json에 json 형식으로 데이터 저장
            with tf.gfile.GFile(file_path,'w')as outfile:
                json.dump(data,outfile, indent=4)
        #info.json에 저장된 전체 데이터를 불러옴
        with tf.gfile.GFile(file_path,'r') as datafile:
            json_data=json.load(datafile)

        #여기서부터 전체 데이터를 최종 결과로 가공하여 result.json에 저장하는 부분 
        new_r1=[]
        new_r2=[]
        new_r3=[[],[]]
        new_r4=[]

        #옆모습으로 측정하기때문에 점들이 겹칠 때, 튀는 값이 발생할 수 있음 -> 이 값을 각 함수에서 NaN으로 예외처리 해줬을 것 /
        #NaN값을 제외한 측정값만 사용하여 최종 결과 가공 
        for i in json_data['post']:
            if(np.isnan(i['result1'][0])==False):
                new_r1.append(i['result1'][0])
            if(np.isnan(i['result2'][0])==False):
                new_r2.append(i['result2'][0])
            if((np.isnan(i['result3'][0][0]))==False)and((np.isnan(i['result3'][0][1]))==False):
                new_r3[0].append(i['result3'][0][0])
                new_r3[1].append(i['result3'][0][1])
            if(np.isnan(i['result4'][0])==False):
                new_r4.append(i['result4'][0])

        #result4 : 보폭크기 정도 결과 가공
        l = [0, 0, 0, 0, 0]
        v4=0
        for i in range(len(new_r4)):
            if new_r4[i] > 75:
                l[4] += 1
            elif new_r4[i] > 65:
                l[3] += 1
            elif new_r4[i] > 55:
                l[2] += 1
            elif new_r4[i] > 45:
                l[1] += 1
            elif new_r4[i] > 35:
                l[0] += 1

        if l[4] != 0:
            v4 = 50
        elif l[3] != 0:
            v4 = 25
        elif l[2] != 0:
            v4 = 0
        elif l[1] != 0:
            v4 = -25
        elif l[0] != 0:
            v4 = -50

        #result3 : 팔흔들림 정도 결과 가공
        v3 = 0

        l3m = []
        l3M = []
        r3m = []
        r3M = []

        new_r3[0].sort()
        new_r3[1].sort()

        for i in range(int(len(new_r3[0]) * 0.3)):
            l3m.append(new_r3[0][i])
        for j in range(int(len(new_r3[1]) * 0.3)):
            r3m.append(new_r3[1][j])
        for k in range(int(len(new_r3[0])), int(len(new_r3[0]) * 0.7), -1):
            l3M.append(new_r3[0][k-1])
        for l in range(int(len(new_r3[1])), int(len(new_r3[1]) * 0.7), -1):
            r3M.append(new_r3[1][l-1])

        lres = int(sum(l3M)/len(l3M)) - int(sum(l3m)/len(l3m))

        rres = int(sum(r3M)/len(r3M)) - int(sum(r3m)/len(r3m))

        if (lres > rres):
            v3 = -50 * ((lres - rres) / lres)
        elif (lres < rres):
            v3 = 50 * ((rres - lres) / rres)  
        
        #result.json에 최종 가공 데이터 넣고 저장
        result={}
        result['post']=[]
        result['post'].append({'result1': int(sum(new_r1)/len(new_r1)),
                            'result2':int(sum(new_r2)/len(new_r2)),
                            'result3':int(v3),
                            'result4':v4})
        with open('result.json','w')as f:
            json.dump(result,f,indent=4)