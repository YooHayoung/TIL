# JPA와 Querydls

해당 내용은 김영한님의 *실전! Querydsl*을 수강하고 정리한 내용입니다.

---

## 순수 JPA Repository
- Querydsl 메서드 작성 가능

## 스프링 데이터 JPA Repository
- Querydsl 등을 사용하기 위해서는
- 사용자 정의 Repository 사용

### API나 특정 화면에 특화된 복잡한 기능이라면?
- Spring Data JPA나 사용자 정의 Spring Data JPA처럼 만들지 않고 특정 용도용 Repository 생성, 정의
- 이렇게 만든 Repository를 주입받아 사용하도록 하는 방법도 있다.
- 너무 커스텀에 억압되어서 모든것을 커스텀에 Repository에서 해결하려는 것도 좋은 설계는 아니다.
- 핵심 비즈니스로직, 재사용 가능성이 있는 것들, 엔티티를 검색하는 등의 경우에는 Spring Data Repository에 넣고, 공용성이 없고 특정 API, 화면에 종속되어있다면 별도로 조회용 Repository를 만들어 사용하는것도 좋은 방법이다.
- 기본은 스프링 데이터 JPA를 커스텀하여 쓰는게 맞고, 아키텍처 적으로 유연하게 가져가고 싶으면 분리하는 것도 좋은 방법이다.


## CountQuery 최적화
- 전체 카운트 조회 방법을 최적화 할 수 있으면 분리해서 따로 쿼리 날린다.
- 스프링 데이터 JPA는 count 쿼리가 생략 가능하면 생략할 수 있다.
  - 페이지 시작이면서 조회 사이즈가 페이지 사이즈보다 작을 때
  - 마지막 페이지(offset + contents size로 전체 사이즈 구한다.)
- 스프링 데이터 라이브러리가 제공하는 `PageableExecutionUtils.getPage()`를 이용.
  - `JPAQuery<T> countQuery = queryFactory.select() ... ;`
  - count 쿼리를 정의하고
  - `PageableExecutionUtils.getPage(content, pageable, countQuery::fetchCount)`

## 정렬
- 조건이 조금만 복잡해져도 Pageable의 Sort 기능을 사용하기 어려움
- 루트 엔티티 범위를 넘어가는 동적 정렬이 필요하면 파라미터를 받아서 직접 처리하는 것을 권장

## 스프링 데이터 JPA가 제공하는 Querydsl 기능
- 