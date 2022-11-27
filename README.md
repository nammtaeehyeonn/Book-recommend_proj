# **챗봇 만들기** 

* 처음 배우는 딥러닝 챗봇(한빛미디어. 조경래 지음. 2020년 11월) 실습

1. 실습 목적
   - 딥러닝 분석 중 자연어 처리에 관한 내용을 습득하고, 챗봇 구현을 위한 전반적인 내용을 익히기 위해
   - 책의 챗봇 구현 내용을 바탕으로 좀 더 발전된 챗봇 모델을 구현하고 싶었음

2. 진행 내용
   - 책의 chapter 중 8장 까지는 여러 시행 착오를 거치면서 진도가 나갔지만, 그 이후 진도가 나가기 위해서 더 많은 시간이 필요함
   
3. 문제점
   - 책의 내용이 약 2년 전 내용인데 책의 내용대로 구현하려고 할 때 막히는 부분들이 꽤 있음
   - 특히, 함수나 클래스로 .py 파일로 모듈을 만들어서 다른 프로젝트 관리 디렉터리에 저장하고 불러오는 부분은 결국 해결하지 못함
     > 임시방안: 진행 파일은 가장 상위 디렉터리에 두고 모듈 파일들은 하위 디렉터리에만 저장해서 import
     > 만일 진행 파일이 모듈이 저장 된 디렉터리의 상위 - 다시 하위 등의 위치에 있으면 경로 불러오기가 너무너무 힘듦.


4. 실습으로 구현되는 챗봇 타입
   - 토이 챗봇 형식으로, 간단하게 주문을 하고 싶다는 입력문에 대해 답변을 해주는 챗봇 방식
   - 좀 더 다양한 대화나 더 넓은 주제의 챗봇 구현 안됨
