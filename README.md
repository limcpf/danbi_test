# ROUTINE API 서버

## 개발 프레임워크
---
- 언어 : Python(3.11.1)
- 프레임워크 : Django(4.1.6), DRF(3.14.0)
- 그 외에 사용한 프레임워크, 라이브러리는 root 경로 내 requirements.txt 에 기록해놓았습니다.

## 테이블 설계
---
![테이블](https://user-images.githubusercontent.com/52344604/216826322-9f31a1ba-8548-43f1-870d-6594bffc02bb.png)

### ROUTINE 테이블
- 루틴 마스터 테이블
	- PK : ROUTINE_ID 로 Auto_increment를 설정하여 사용하였습니다.
	- FK : USER_USER.id(유저테이블) 값 으로 랜덤한 uuid 36자리를 ACCOUNT_ID가 들어가는 컬럼입니다.
	- TITLE, GOAL : 제목, 목표에 대한 컬럼입니다.
	- CATEGORY : 정의한 대로 "H"(HOMEWORK), "M"(MIRACLE) 두 값이 들어가는 컬럼입니다.
	- IS_ALARM : 알람 여부 입니다. 해당 값이 삽입시에 들어오지 않아도 default 값으로 false 값이 들어오게 설정된 컬럼입니다.
	- IS_DELETED : 삭제 여부 입니다. soft delete 전략을 사용하기 위한 컬럼으로 해당 값은 데이터 생성 시 false 값이 삽입 될 수 있게 설정된 컬럼입니다.

### ROUTINE_RESULT 테이블
- 루틴 결과 테이블
	- PK : ROUTINE_RESULT_ID 로 Auto_increment를 설정하여 사용하였습니다.
	- FK :  ROUTINE_ROUTINE.ROUTINE_ID 값을 설정하였습니다.
	- RESULT : 정의한 대로 "N"(NOT), "T"(TRY), "D"(DONE) 세 값이 들어가는 컬럼입니다.
	- IS_DELETED : 삭제 여부 입니다. soft delete 전략을 사용하기 위한 컬럼으로 해당 값은 데이터 생성 시 false 값이 삽입 될 수 있게 설정된 컬럼입니다.
### ROUTINE_DAY 테이블
- 루틴 요일 테이블
	- PK : ROUTINE_DAY_ID 로 Auto_increment를 설정하여 사용하였습니다.
	- FK :  ROUTINE_ROUTINE.ROUTINE_ID 값을 설정하였습니다.
	- DAY : FK값과 해당 DAY 컬럼 값을 이용하여 복합 PK 제약을 구성하였습니다.

### 공통 컬럼
- CREATED_AT, MODIFIED_AT : 각각 생성일시, 수정일시와 관련된 컬럼이며 각 테이블마다 자동으로 생성될 수 있게 설정하였습니다.