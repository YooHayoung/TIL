# JPA란?

## JPA
* Java Persistence API
* 자바 진영의 ORM 기술 표준이다.

## ORM
* Object-relational mapping (객체 관계 매핑)
* 객체는 객체대로 설계하고 RDB는 RDB대로 설계한다.
* ORM 프레임워크가 중간에서 매핑해준다. (JPA)
	* 객체 - ORM(JPA) - RDB
	* 객체와 RDB의 패러다임 차이를 극복하도록 도와준다.

## JPA는 표준 명세
* `JPA`는 `인터페이스의 모음`이다.
* 이를 구현한 3가지 구현체로는 `Hibernate`, `EclipseLink`, `DataNucleus` 있다.

## JPA는 왜 써야하나?
* SQL 중심적인 개발에서 객체 중심으로 개발할 수 있다.
* 생산성 증가
* 유지보수 Good
* 패러다임 불일치 해결
* 높은 성능
* 데이터 접근 추상화와 벤더 독립성
	* 벤더는 생산회사를 말한다.
	* 각 DB마다 명령을 처리하는 방법이 다를 수 있음
	* 인터페이스인 JPA를 통해 기능을 구현하면 데이터베이스를 변경하여도 정상 동작한다. 이를 `벤더 독립성`이라고 한다.
* 표준이다.


## JPA 구동 방식
* `Persistence`에서 설정 정보 조회
* 이를 기반으로 `EntityManagerFactory` 생성
	* `EntityManagerFactory`는 1개만 생성하여 `애플리케이션이 공유`한다.
* EntityManagerFactory가 `EntityManager` 생성.  `EntityManager`는 Factory에서 `Session마다 생성`하여 **사용하고 버린다.** 
	* 쓰레드마다 공유 X
* JPA의 모든 데이터 변경은 트랜잭션 안에서 실행된다.

#JPA
#JPA/JPA란
#JPA/JPA구동방식
---

해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.