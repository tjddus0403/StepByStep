import tensorflow as tf
import cv2
import time
import argparse
import os
import numpy as np
import posenet

# parser = argparse.ArgumentParser()
# parser.add_argument('--model', type=int, default=101)
# parser.add_argument('--scale_factor', type=float, default=1.0)
# parser.add_argument('--notxt', action='store_true')
# parser.add_argument('--image_dir', type=str, default='./images')
# parser.add_argument('--output_dir', type=str, default='./output')
# args = parser.parse_args()

args = {"model": 101, "scale_factor": 1.0, "notxt": True, "image_dir": './images',
        "output_dir": './output'}
# model 번호를 입력해주어 posenet중 어떤 모델 쓸지 결정 
# scale_factor의 역할이 뭘까?

#평균내기 -> 이후에 척추 세분화에서 사용
def getAverage(pos, n):
    x, y = 0, 0

    for i in range(n):
        x += pos[i][0]
        y += pos[i][1]

    return [x/n, y/n]


def main(exerciseCode): # -> keypointList
    keypointList = []

    # Launch the graph in a session.
    # https://www.tensorflow.org/api_docs/python/tf/compat/v1/Session
    with tf.compat.v1.Session() as sess:
        # 딕셔너리 형태로 output_stride와 checkpoint_name을 반환해준다. (파일을 이쁘게 불러와서)
        model_cfg, model_outputs = posenet.load_model(args['model'], sess)
        #args는 위의 전역 배열 
        #sess는 뭐지 -> 위 주소로 가보쇼
        output_stride = model_cfg['output_stride']

        #출력주소 없을 때 발생오류처리
        if args['output_dir']:
            if not os.path.exists(args['output_dir']):
                os.makedirs(args['output_dir'])

        #원하는 형식의 파일이라면 image주소를 스캔해서 파일 주소로 
        #f.path를 통해 파일이름들을 모두 저장
        filenames = [
            f.path for f in os.scandir(args['image_dir']) if f.is_file() and f.path.endswith(('.png', '.jpg'))]

        #운동 종류별 인덱싱
        exercise = {1: 'squat', 2: 'press_up',
                    2.5: 'press_down', 3: 'raise_up', 3.5: 'raise_down'}
        
        #운동 종류별 해당 사진
        f = './images\\' + exercise[exerciseCode] + '.jpg'
        #시간 측정 시작
        start = time.time()

        # 스케일링 = 어떤 양을 늘리거나 줄이는 것
        input_image, draw_image, output_scale = posenet.read_imgfile(
            f, scale_factor=args['scale_factor'], output_stride=output_stride)

        #load_model에서 불러온 모듈과 위에서 불러온 사진을 feed로 지정해준 후
        #이를 이용하여 나온 결과를 출력.
        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
            model_outputs,
            feed_dict={'image:0': input_image}
        )

        #이 프로젝트에서는 여기서 single 대신 multiple이용.
        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
            #squeeze는 압축시키는 것.
            #max_pose_detections은 최대 검출 인원인듯(왜냐하면 multiple이니까)
            #min_pose_socore는 자세로 판단하는 최소 점수?인듯
            heatmaps_result.squeeze(axis=0), # == scores
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=output_stride,
            max_pose_detections=10,
            min_pose_score=0.25)
        #pose_scores 이해가 좀 어려움... 머리가 안돌아감.

        keypoint_coords *= output_scale

        #======================================================================================================
        spineTop = getAverage(
            [keypoint_coords[0][5], keypoint_coords[0][6]], 2)
        spineMiddle = getAverage(
            [keypoint_coords[0][5], keypoint_coords[0][6], keypoint_coords[0][11], keypoint_coords[0][12]], 4)
        spineBottom = getAverage(
            [keypoint_coords[0][11], keypoint_coords[0][12]], 2)

        spine_pos = [spineTop, spineMiddle, spineBottom]

        for i in range(3):
            tmp = np.array([[spine_pos[i]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[
                0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]]])
            keypoint_coords = np.concatenate(
                (keypoint_coords, tmp), axis=1)
            keypoint_scores = np.concatenate(
                (keypoint_scores, np.array([[1], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00]])), axis=1)
        #=====================================================================================================================================================================================================================

        if args['output_dir']:
            #스켈레톤 만들어서 그림에 저장
            draw_image = posenet.draw_skel_and_kp(
                draw_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.25, min_part_score=0.25)

            cv2.imwrite(os.path.join(args['output_dir'],
                        os.path.relpath(f, args['image_dir'])), draw_image)

        for pi in range(len(pose_scores)):
            #pose_scores의 의의가 겨우 이건가..?
            if pose_scores[pi] == 0.:
                break
            # (여러개의 리스트와 인덱스)의 요소를 얻고 싶을 때
            # ki = index, s= keypoint_scores[ki,:,:], c = keypoint_coords[ki,:,:]
            for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                keypointList.append(c)
            #결국 좌표 얻어감. 
        return keypointList


if __name__ == "__main__":
    main()
