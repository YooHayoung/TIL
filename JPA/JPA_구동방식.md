# JPA 구동 방식
- Persistence 에서 설정 정보 조회
- 이를 기반으로 EntityManagerFactory 생성 <br> EntityManagerFactory는 1개만 생성하여 애플리케이션이 공유한다.
- EntityManagerFactory가 EntityManager 생성. <br> EntityManager는 Factory에서 Session마다 생성하여 사용하고 버린다. 쓰레드마다 공유 X
- JPA의 모든 데이터 변경은 트랜잭션 안에서 실행된다.


<br><br><br><br>

---

해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.