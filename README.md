# 그대의 걸음걸이 (AI융합경진 대회 _ Team.뜨아아)
### 걸음걸이 이미지를 활용한 신체 상태 분석 시스템
![blue_logo](https://user-images.githubusercontent.com/70639589/201914819-983013cc-2775-48ce-add4-c1fe3e7f4f14.png)

#### 작품 소개


#### 설치 및 실행과정
- Git clone
```
$ git clone https://github.com/tjddus0403/StepByStep.git
```
- ngrok Installation
```
$ ngrok http 8000 --authtoken={사용자의 authtoken}
# main/templates/main/qr.html의 url로의 이동 주소에 autotoken 넣어줌
```
- Django Virtual Environment
```
$ cd StepByStep/StepbyStep
# python 3.7.2 & 3.8.2 
# Django 가상환경에서 실행
(django_env) $ pip install -r requirements.txt
(django_env) $ python manage.py migrate
(django_env) $ python manage.py createsupersuer
(django_env) $ pytho manage.py runserver
```
#### 데모영상
[YouTube 바로가기](https://google.com)

#### Contributors

| Name | School & Major | Github |
|-|-|-|
| 👩🏻‍💻 SungYeon Kim | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/tjddus0403 |
| 👨🏻‍💻 JaeWon Ko | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/jaewon1778 |
| 👨🏻‍💻 DongHyun Kang | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/tjddus0403 |
| 👨🏻‍💻 SeongYun Kim | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/tjddus0403 |
#### Contributors
- Kim Sungyeon
- Ko Jaewon
- Kang Donghyun
- Kim Seongyun
