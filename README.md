# 그대의 걸음걸이 (AI융합경진 대회 _ Team.뜨아아)
### 걸음걸이 이미지를 활용한 신체 상태 분석 시스템
![blue_logo](https://user-images.githubusercontent.com/70639589/201914819-983013cc-2775-48ce-add4-c1fe3e7f4f14.png)

## 작품 소개
[경진대회 최종 결과 발표.pdf](https://github.com/tjddus0403/StepByStep/files/10017819/default.pdf)

## 설치 및 실행과정
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
## 데모영상
[YouTube 바로가기](https://www.youtube.com/watch?v=HqwVybZ8kz4)

## Development Environment
<p align="center">
 <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=TensorFlow&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/></a> 
</p>

*Language :* Python 3.7 & Python 3.8  
*Framework :* Django 3.2.16  
*Video Processing :* openCV & tensorflow-posenet
## Contributors
| Name | School & Major | Github |
|-|-|-|
| 👩🏻‍💻 SungYeon Kim | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/tjddus0403 |
| 👨🏻‍💻 JaeWon Ko | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/jaewon1778 |
| 👨🏻‍💻 DongHyun Kang | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/andantinow |
| 👨🏻‍💻 SeongYun Kim | 🎓 Soongsil Univ. 🤖 AI Convergence | https://github.com/kimseoungyun |

