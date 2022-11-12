#사람의 길이가 원하는 만큼 되도록함.
def isReady(keypoint):
    # keypoint[15][0]: 왼쪽 발목 y좌표, keypoint[1][0]: 왼쪽 눈 y좌표
    height = keypoint[15][0] - keypoint[1][0]
    MAX_LIMIT = 320
    MIN_LIMIT = 250

    if MIN_LIMIT <= height <= MAX_LIMIT:
        print("준비상태가 되었습니다.")
        return True
    elif height > MAX_LIMIT:
        print("뒤로 가주세요")
        return False
    elif height < MIN_LIMIT:
        print("앞으로 가주세요")
        return False


def isSide(keypoint):
    # keypoint[11][1]: 왼쪽 골반 x좌표, keypoint[12][1]: 오른쪽 골반 x좌표
    pelvis = abs(keypoint[11][1] - keypoint[12][1])
    limit = 20

    if pelvis <= limit:
        print("측면입니다.")
        return True
    else:
        print("측면으로 서주세요.")
        return False


def isFront(keypoint):
    # keypoint[11][1]: 왼쪽 골반 x좌표, keypoint[12][1]: 오른쪽 골반 x좌표
    pelvis = abs(keypoint[11][1] - keypoint[12][1])
    limit = 30

    if pelvis <= limit:
        print("정면으로 서주세요.")
        return False
    else:
        print("정면입니다.")
        return True
