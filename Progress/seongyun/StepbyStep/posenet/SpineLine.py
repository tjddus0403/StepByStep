import math


#키와 보폭의 비율 기준과의 차이점 파악
# 0:코, 1:왼쪽눈, 2:오른쪽눈, 3:왼쪽귀, 4:오른쪽귀", 5:왼쪽어깨, 6:오른쪽어깨
# 7:왼쪽팔꿈치, 8:오른쪽팔꿈치, 9:왼쪽손목, 10:오른쪽손목, 11:왼쪽골반부위, 12:오른쪽골반부위
# 13:왼쪽무릎, 14:오른쪽무릎, 15:왼쪽발목, 16:오른쪽발목
# 17:척추상 = 5/6평균, 18:척추중 = 5/6/11/12평균 19:척추하 = 11/12평균

def getDegree(key1, key2, key3):
    try:
        x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
            math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
        return abs(x*180/math.pi)
    except:
        getDegree(key1, key2, key3)

# 어깨와 골반이 일직선으로 연결되어 있는 정도를 퍼센트로 환산하여 반환하는 함수
# 배나오게 걷는 사람들 방지 혹은 오리 궁뎅이
def SpineLine(keypoint):
    spine_offset = abs(keypoint[17][1] - keypoint[19][1])
    #피타고라스를 통해서 어깨부터 골반까지의 길이를 구함.
    max_offset = ((keypoint[17][0] - keypoint[19][0])**2 + (keypoint[17][1] - keypoint[19][1])**2)**0.5

    result = ((max_offset - spine_offset)/max_offset)*100
    result = (result)

    return result

