import math
# from posenet import imageDetect

# 0:코, 1:왼쪽눈, 2:오른쪽눈, 3:왼쪽귀, 4:오른쪽귀", 5:왼쪽어깨, 6:오른쪽어깨
# 7:왼쪽팔꿈치, 8:오른쪽팔꿈치, 9:왼쪽손목, 10:오른쪽손목, 11:왼쪽골반부위, 12:오른쪽골반부위
# 13:왼쪽무릎, 14:오른쪽무릎, 15:왼쪽발목, 16:오른쪽발목
# 17:척추상 = 5/6평균, 18:척추중 = 5/6/11/12평균 19:척추하 = 11/12평균
# 20:목뼈 시작 = 3/4평균


def getDegree(key1, key2, key3):
    try:
        x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
            math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
        return abs(x*180/math.pi)
    except:
        getDegree(key1, key2, key3)

# 귀랑 골반이랑 연결해서 오차를 결정
# 거북목 방지
def SpineCurve(keypoint):
    curve_angle = getDegree(keypoint[20], keypoint[17], keypoint[19])

    result = ((180 - curve_angle)/180)*100
    result = (result)

    return result

    
