# Querydls 중급 문법

해당 내용은 김영한님의 *실전! Querydsl*을 수강하고 정리한 내용입니다.

---

## 프로젝션 결과 반환
- 프로젝션이란
  - select 대상 지정
- 프로젝션 대상이 둘 이상이면 튜플이나 DTO로 조회한다.
  - `List<Tuple>` ... `select(member.username, member.age)`
- DTO를 권장한다.

## 프로젝션 - DTO
- Querydsl Bean 생성
- 프로퍼티 접근
  - Default Constructor 필요
  - setter 필요
   ```java
   List<MemberDto> result = queryFactory
      .select(Projections.bean(MemberDto.class,
         member.username,
         member.age))
      .from(member)
      .fetch();
   ```
- 필드 직접 접근
  - `Projections.fields(...)`
  - setter 필요 없음
- 생성자 사용
  - `Projections.constructor(...)`
  - 생성자의 타입과 맞아야 한다.

### 별칭이 같아야 한다.
- 별칭이 다르면 값을 넣어주지 않는다..
- `.as("")`를 통해 해결
  - 필드에 별칭 적용한다.
- `ExpressionUtils.as(source, alias)`
  - `JPAExpressions`를 통해 서브쿼리를 작성하고 이에 별칭을 적용.


## 프로젝션 - @QueryProjection
- 생성자에 `@QueryProjection` 붙여준다.
  - `./gradlew compileQuerydsl` - QType 생성
- complie time에 오류를 잡아준다. (장점)
- DTO에 Querydsl 어노테이션을 유지해야 하고-의존성을 가지게 됨, DTO까지 Q파일을 생성(단점)
```java
List<MemberDto> result = queryFactory
   .select(new QMemberDto(member.username, member.age))
   .from(member)
   .fetch();
```

## 동적 쿼리

### BooleanBuilder
- `BooleanBuilder` 생성
  - 생성자에 초기값을 넣어줄 수도 있다.
- 조건문을 통해 `BooleanBuilder`에 `.and`, `.or`등으로 추가시킨다.

### Where 다중 파라미터
- 이 방식이 훨씬 깔끔하다.
- 파라미터 `null`체크를 하는 메서드를 만들어 `where`절에서 사용한다.
  - `BooleanExpression` 타입 반환
  - 파라미터가 `null`이면 `null`반환, 아니면 정상조건(`member.username.eq(param)`)반환
  - `where`조건에 `null`은 무시된다.
- 재사용성 높아짐

## 벌크 연산
- `update`, `delete` ... `.excute();`
- 영속성 컨텍스트에 있는 엔티티를 무시하고 실행.
- 배치 쿼리를 실행하고 나면 영속성 컨텍스트를 초기화하는 것이 안전하다.

## SQL Function 호출
- Dialect에 등록된 내용만 호출가능.
- `Expressions.stringTemplate("function('replace', {0}, {1}, {2})", -, -, - )`
- ansi 표준 함수들은 Querydsl이 상당부분 내장.

