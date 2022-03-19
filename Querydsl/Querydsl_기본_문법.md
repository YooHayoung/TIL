# Querydsl 기본 문법

해당 내용은 김영한님의 *실전! Querydsl*을 수강하고 정리한 내용입니다.

---

## JPAQueryFactory
- querydsl은 JPAQueryFactory에 EntityManager를 주입받아서 사용한다.
   ```java
   JPAQueryFactory queryFactory = new JPAQueryFactory(em);
   QMember m = new QMember("m");

   Member findMember = queryFactory
         .select(m)
         .from(m)
         .where(m.username.eq("member1"))
         .fetchOne();
   ```


### JPAQueryFactory 필드 제공시 동시성 문제
- EntityManager에 달려있음.
- 스프링 프레임워크는 여러 쓰레드에서 동시에 같은 EntityManager에 접근해도 트랜잭션 마다 별도의 영속성 컨텍스트를 제공하기 때문에, 동시성 문제는 걱정하지 않아도 됨.


>querydsl은 컴파일 타임에 오류를 잡아준다. *매우 좋음!!*<br>
jpql는 런타임에 잡는다. 


## 기본 Q-Type
### Q클래스 인스턴스 사용 2가지 방법
```java
QMember qMember = new QMember("m"); // 별칭 직접 지정
QMember qMember = QMember.member; // 기본 인스턴스 사용
```
> 기본 인스턴스를 static import 하여 사용하면 깔끔하다.
> <br>같은 테이블을 조인해야 하는 경우가 아니면 기본 인스턴스 사용을 권장.

> 다음 설정을 추가하면 실행되는 JPQL을 볼 수 있다.
```properties
spring.jpa.properties.hibernate.use_sql_comments: true
```

## 검색 조건 쿼리
### 기본 검색 쿼리
```java
Member findMember = queryFactory
      .select(member)
      .from(member) // .selectFrom(member) 동일
      .where(member.username.eq("member1")
            .and(member.age.eq(10)))
      // .where(member.username.eq("member1"), member.age.eq(10)) 동일
      .fetchOne();
```
- `where()`절에 파라미터로 검색 조건을 추가하면 `AND` 조건이 추가 된다.
- 이때, `null`값은 무시되어 메서드 추출을 활용하여 동적 쿼리를 깔끔하게 만들 수 있다.

### JPQL이 제공하는 모든 검색 조건을 제공한다
- `.eq("")` : =
- `.ne("")` : !=
- `.eq("").not()` : !=
- `.isNotNull()` : is not null
- `.in(-, -)` : in (-, -)
- `.notIn(-, -)` : not in (-, -)
- `.between(-, -)` : between -, -
- `.goe(-)` : >=
- `.gt(-)` : >
- `.loe(-)` : <=
- `.lt(-)` : <
- `.like("김%")` : like
- `.contains("수")` : like '%수%'
- `.startsWith("김")` : like '김%'
- 등등 더 있다.


## 결과 조회
- `fetch()` : 리스트 조회. 데이터 없으면 빈 리스트 반환
- `fetchOne()` : 단건 조회. 결과 없으면 `null`, 둘 이상이면 `NonUniqueResultException`
- `fetchFirst()` : `limit(1).fetchOne()`
- `fetchResults()` : 페이징 정보 포함, total count 쿼리 추가 실행
  - 복잡하고 성능이 중요한 페이징 쿼리는 얘를 쓰지 말고, 쿼리 두 개를 따로 날려야 한다.
- `fetchCount()` : count쿼리로 변경해서 count 수 조회

## 정렬
- `desc()` : 내림차순
- `asc()` : 오름차순
- `nullsLast()` : null 데이터 마지막
- `nullsFirst()` : null 데이터 처음
   ```java
   .orderBy(member.age.desc(), member.username.asc().nullsLast())
   ```

## 페이징
```java
// 전체 조회 수가 필요하면
// QueryResults<T> 로 받고
// 아니면
// List<T> 로 받자
queryFactory
   .selectFrom(member)
   .orderBy(member.username.desc())
   .offset(1) // 0부터 시작
   .limit(2) // 최대 조회 건수
   .fetch();
```
> count 쿼리에 조인이 필요없는 성능 최적화가 필요하면 count 전용 쿼리를 별도로 작성하자.

## 집합
### 집합 함수
- JPQL이 제공하는 모든 집합 함수를 제공
- `.count()`
- `.sum`
- `.avg()`
- `.max()`
- `.min()`

### GroupBy
```java
queryFactroy
   .select(team.name, member.age,avg())
   .from(member)
   .join(member.team, team)
   .groupBy(team.name) // team.name으로 Groupping
   //.having() : having절 가능
   .fetch();
```

## 조인
### 기본 조인
```java
// join(조인 대상, 별칭으로 사용할 QType)
.join(member.team, team)
```
- `join()`,`innerJoin()` : 내부 조인
- `leftJoin()` : left outer join
- `rightJoin()` : right outer join
- `fetch` 조인 제공
  - JPQL의 `on`과 성능 최적화

### 세타 조인
- 연관관계가 없는 필드로 조인
- `from` 절에 여러 엔티티 입력 : `.from(member, team)`
- 외부 조인 불가능
  - 조인 on을 사용하면 가능

### ON 절
- 조인 대상 필터링
   ```java
   //member.team.name == "teamA" -> Join
   //member.team.name != "teamA" -> null 인 tuple 반환
   queryFactory
      .select(member, team)
      .from(member)
      .leftJoin(member.team, team).on(team.name.eq("teamA"))
      .fetch();
   ```

- 연관관계 없는 엔티티 외부 조인
   ```java
   // member.username == team.name
   queryFactory
      .select(member, team)
      .from(member)
      .leftJoin(team).on(member.username.eq(team.name))
      .fetch();
   ```
   > <b>!문법 주의!</b><br>
   `leftJoin()` 부분에 일반 조인과 다르게 엔티티 하나만 입력함

### fetch 조인
- SQL 조인을 활용하여 연관된 엔티티를 SQL 한번에 조회하는 기능
- 주로 성능 최적화에 사용
- 조인 뒤에 `.fetchJoin()` 추가하면 됨
```java
queryFactory
   .selectFrom(member)
   .join(member.team, team).fetchJoin()
   .where(member.username.eq("member1"))
   .fetchOne();
```

## 서브 쿼리
- `com.querydsl.jpa.JPAExpressions` 사용
- `JPAExpressions`의 엔티티와 엘리어스가 겹치면 안된다.
- QType을 직접 생성해줘서 별칭을 다르게 해서 사용하자.
   ```java
   // sub query member
   QMember memberSub = new QMember("memberSub");

   queryFactory
      .selectFrom(member)
      .where(member.age.eq(
         JPAExpressions
            .select(memberSub.age.max())
            .from(memberSub)
      ))
      .fetch();
   ```
- `eq`, `goe`, `in`, `select`절에 subQuery 등등 가능하다.
- `JPAExpressions`를 static import 하여 사용 가능하다

### JPA : from 절의 서브쿼리(인라인 뷰) 한계
- 원래 JPA는 select 절도 지원하지 않으나 구현체인 하이버네이트가 select 절의 서브쿼리를 지원해서 가능한 것.

### 해결방안
- 서브쿼리를 join으로 변경
- 애플리케이션에서 쿼리를 2번 분리해서 실행
- nativeSQL 사용

> 서브쿼리에 집착하지 말자. 화면에 맞춰서 쿼리를 짜지 말자. 재활용성이 떨어진다. DB는 데이터만 필터링, 그루핑해서 가져오고, 로직은 앱에서. 실시간 트래픽이 중요하지 않다면 복잡한 애들은 쿼리를 나눠서 가져오는게 나을 수도 있다. *SQL AntiPatterns*

## Case 문
- select, where, order by에서 when().then() 사용 가능
- 복잡한 조건은 new CaseBuilder().when().then()
- 꼭 필요하다면 사용하고 가능하면 App 로직에서 처리하자.
- 필요하면 찾아보고 사용하자

## 상수, 문자 더하기
### 상수
- `Expressions.constant(-)`

### 문자 더하기
- `concat("")`
- 숫자 등의 타입은 `.stringValue()`를 통해 문자로 변경해서 사용
  - ENUM Type등을 처리할 때도 자주 사용함

