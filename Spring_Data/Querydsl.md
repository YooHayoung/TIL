# Querydsl
[1. Querydsl 설명](#querydsl-설명)
[2. Querydsl 설정](#querydsl-설정)
[3. Q Type 파일 생성](#q-type-파일-생성)
[4. Querydsl 적용](#querydsl-적용)
[5. Querydsl 문법](#querydsl-문법)
[6. JPA와 QueryDSL](#jpa와-querydsl)

## Querydsl 설명
기존 JPQL이나 쿼리를 직접 작성하는 방식에서 쿼리는 문자이기 때문에 해당 쿼리가 실행되기 전 까지는 작동 여부를 확인할 수 없다. 쿼리에 바인딩되는 타입의 체크도 불가능하다. 이 방식은 오류를 런타임에 잡을 수 있는 것이다. 타입 체크가 불가능하기 때문에 동적 쿼리를 작성하기 어렵다는 단점이 있다. 이러한 문제를 해결하기위해 QueryDSL이 등장했다.

`DSL`은 `Domain(도메인) Specific(특화) Language(언어)`로 특정한 도메인에 초점을 맞춘 제한적인 표현력을 가진 컴퓨터 프로그래밍 언어로 정의된다. 
`QueryDSL`은 `Query` + `DSL`의 개념으로 쿼리에 특화된 프로그래밍 언어이다. 쿼리를 자바 언어로 작성하여 타입을 체크할 수 있도록 `type-safe`하게 개발할 수 있게 지원하는 프레임워크이다. QueryDSL을 사용하면 컴파일 타임에 쿼리의 오류를 잡을 수 있다. 자바 코드로 작성하여 컴파일 타임에 오류를 체크할 수 있기 때문에 복잡한 동적 쿼리를 작성하기에 편리하다. 주로 JPA 쿼리를 사용할 때 많이 사용한다.

`Type-safe`한 쿼리 타입을 만드려면 `QueryDSL`에서 제공하는 `APT(Annotation Processing Tool)`라는 코드 생성기를 통해 `QType`을 생성해야 한다. `APT`는 `@Entity`, `@QueryProjection` 애노테이션이 붙은 클래스를 보고 `QType` 파일을 생성해준다. 
프로젝트에 `QueryDSL`의 설정과 `APT` 컴파일을 통해 Q 타입 파일을 생성할 수 있다.



## Querydsl 설정
- `build.gradle` - Querydsl 관련 설정
```java
buildscript {
	dependencies {
		classpath("gradle.plugin.com.ewerk.gradle.plugins:querydsl-plugin:1.0.10")
	}
}

plugins {
   id "com.ewerk.gradle.plugins.querydsl" version "1.0.10"
}

apply plugin: "com.ewerk.gradle.plugins.querydsl"

configurations {
	compileOnly {
		extendsFrom annotationProcessor
	}
}

dependencies {
	implementation 'com.querydsl:querydsl-jpa'
	annotationProcessor 'com.querydsl:querydsl-apt'
}

def querydslDir = "$buildDir/generated/querydsl"

querydsl {
	library = "com.querydsl:querydsl-apt"
	jpa = true
	querydslSourcesDir = querydslDir
}

sourceSets {
	main {
		java {
			srcDirs = ['src/main/java', querydslDir]
		}
	}
}

compileQuerydsl{
	options.annotationProcessorPath = configurations.querydsl
}

configurations {
	querydsl.extendsFrom compileClasspath
}

// 자동 생성된 Q클래스를 gradle clean으로 제거한다.
// IntelliJ IDEA로 빌드하는 옵션을 선택하면 src/main/generated 아래에 파일이 생성되고 필요한 경우 Q 파일을 직접 삭제해야 한다. 아래 스크립트는 gradle clean 명령어를 실행하면 src/main/generated 아래에 있는 파일을 함께 삭제해준다.
clean {
	delete file('src/main/generated')
}
```

> **[참고]** 22.07.13 기준 Querydsl 최신 버전의 설정으로 버전마다 설정에 조금씩 차이가 있다. 매뉴얼과 검색을 통해 버전에 맞는 설정을 하도록한다.  



## Q Type 파일 생성
엔티티 또는 프로젝션 작성 후, `querydsl`을 컴파일하여 `APT`를 통해 엔티티와 프로젝션에 대한 `Qxxx` 파일을 생성해야 한다. Q 타입 파일을 생성하는 방법은 다음과 같다.

#### Gradle을 통해서 빌드할 때
	* Gradle -> Tasks -> build -> clean
	* Gradle -> Tasks -> other -> compileQuerydsl
	* Gradle 콘솔을 사용한다면 `./gradlew clean compileQuerydsl` 명령어를 통해 가능하다.
Gradle을 통해 빌드하게되면 `/build/generated/sources/annotationProcessor/java/main` 하위에 Q 타입 파일이 생성된다.

#### IntelliJ를 통해서 빌드할 때
`Build -> Build Project` 또는 `Rebuild`를 선택하거나 메인 메서드 실행, 테스트 실행을 하게되면 `src/main/generated` 하위에 Q 타입 파일이 생성된다.
생성된 Q 타입 파일을 삭제하려면 해당 파일을 직접 삭제하거나 `build.gradle`에 `clean { delete file('src/main/generated') }` 설정을 추가하여 `gradle clean` 명령어를 실행하면 된다.

### Q 타입 파일은 버전관리에 포함하지 않도록 한다.
Q타입 파일은 컴파일 시점에 자동으로 생성되기 때문에 버전관리에 포함하지 않는 것이 좋다. 대부분 `gradile build` 폴더를 git에 포함하지 않기 때문에 `gradle`로 빌드하는 경우는 문제가 없을 것이다. 하지만 IntelliJ로 빌드하는 경우 `src/main/generated` 하위에 Q 타입 파일이 생성되기 때문에 `.gitignore` 파일에 해당 위치를 버전관리에 포함하지 않도록 하는 것이 좋다.




## Querydsl 적용
### JPAQueryFactory
Querydsl은 `JPAQueryFactory`에 `EntityManager`를 주입받아서 사용한다. `JPAQueryFactory`는 JPA 쿼리인 JPQL을 만들기 때문에 `EntityManager`가 필요하다. `JPAQueryFactory`를 스프링 빈으로 등록해서 사용해도 무방하다.
스프링 프레임워크는 여러 쓰레드에서 동시에 같은 EntityManager에 접근해도 트랜잭션 마다 별도의 영속성 컨텍스트를 제공하기 때문에, 동시성 문제는 걱정하지 않아도 된다.

```java
@Repository
@Transactional
public class QuerydslTestClass {

	private final EntityManager em;
	private final JPAQueryFactory queryFactory;

	public QuerydslTestClass(EntityManager em) {
		this.em = em;
		this.queryFactory = new JPAQueryFactory(em);
	}

	QMember m = new QMember("m");
	Member findMember = queryFactory
		.select(m)
		.from(m)
		.where(m.username.eq("member1"))
		.fetchOne();
}
```



## Querydsl 문법
### Q 타입 인스턴스 사용
Q 타입의 인스턴스를 사용하는 방법은 2가지로 다음과 같다.
```java
QMember qMember = new QMember("m"); // 별칭 직접 지정
QMember qMember = QMember.member; // 기본 인스턴스 사용. static import 하여 사용 추천.
```


### 검색 조건 쿼리
`where()` 절에 조건을 넣고 이후 `.and()` 또는 `.or()`을 메서드 체인으로 연결하면 여러 검색 조건을 추가할 수 있다.
또한 `where()`절에 파라미터로 검색 조건을 추가하면 `AND` 조건을 추가한 것과 동일한 효과를 볼 수 있다. 이 때, 파라미터로 넘어온 값이 `null`이면 해당 조건은 무시되기 때문에 `where()`절에 파라미터로 `BooleanExpression`을 반환하는 여러 검색 조건 메서드를 넘기면 동적 쿼리 작성시 쿼리를 더 깔끔하게 만들 수 있다.

- `where` 절에 파라미터로 동적 쿼리
```java
Member findMember = queryFactory
      .select(member)
      .from(member) // .selectFrom(member) 동일
      .where(member.username.eq("member1")
            .and(member.age.eq(10)))
      // .where(member.username.eq("member1"), member.age.eq(10)) 동일
      .fetchOne();

// where절에 BooleanExpression 타입을 반환하는 메서드를 파라미터로 넘겨 동적 쿼리를 깔끔하게 작성할 수 있다.
List<Item> findItems = queryFactory
		.select(item)
		.from(item)
		.where(likeItemName(itemName), maxPrice(maxPrice))
		.fetch();

private BooleanExpression likeItemName(String itemName) {
	if (StringUtils.hasText(itemName)) {
		return item.itemName.contains(itemName);
	}
	return null;
}
private BooleanExpression maxPrice(Long maxPrice) {
	if (maxPrice != null) {
		return item.price.loe(maxPrice);
	}
	return null;
}
```

- `BooleanBuilder`를 통해 동적 쿼리를 처리할 수도 있다.
```java
public void test() {
	BooleanBuilder booleanBuilder = new BooleanBuilder();
	if (StringUtils.hasText(name)) {
		booleanBuilder.and(member.name.eq(name));
	}
	if (maxAge != null) {
		booleanBuilder.and(member.age.loe(maxAge));
	}
	List<Member> result = queryFactory
		.selectFrom(member)
		.where(booleanBuilder) // BooleanBuilder 사용
		.fetch();
}
```

#### JPQL이 제공하는 모든 검색 조건을 제공
	* `.eq("")` : =
	* `.ne("")` : !=
	* `.eq("").not()` : !=
	* `.isNotNull()` : is not null
	* `.in(-, -)` : in (-, -)
	* `.notIn(-, -)` : not in (-, -)
	* `.between(-, -)` : between -, -
	* `.goe(-)` : >=
	* `.gt(-)` : >
	* `.loe(-)` : <=
	* `.lt(-)` : <
	* `.like("김%")` : like
	* `.contains("수")` : like '%수%'
	* `.startsWith("김")` : like '김%'
	* 등등 더 있다.


### 정렬
`.orderBy()` 메서드 체인을 통해 검색 결과를 정렬할 수 있다.

	* `desc()` : 내림차순 정렬.
	* `asc()` : 오름차순 정렬.
	* `nullsLast()` : null 데이터를 마지막으로 정렬한다.
	* `nullsFirst()` : null 데이터를 처음에 정렬한다.

```java
.where(...)
.orderBy(member.age.desc(), member.username.asc().nullsLast())
```


### 결과 조회
QueryDsl에서 쿼리문의 결과를 조회하기 위한 메서드는 다음과 같다.

	* `fetch()` : 리스트를 조회한다. 데이터가 없으면 빈 리스트를 반환한다.
	* `fetchOne()` : 단건 조회시 사용한다. 결과가 없으면 `null`을 반환하고, 둘 이상이면 `NonUniqueResultException` 발생한다.
	* `fetchFirst()` : `limit(1).fetchOne()`과 같은 결과이다. 검색 결과의 처음 한 건을 결과로 반환한다.
	* `fetchResults()` : 페이징 정보를 포함한다. total count 쿼리가 추가 실행된다 <- 미지원
	* `fetchCount()` : count 쿼리로 변경해서 count 수를 조회한다. <- 미지원. `fetchOne()`을 통해 count 쿼리 실행할 수 있다.

> **fetchResult(), fetchCount() 미지원**. count 쿼리 별도로 작성하여 페이징 필요.  

`select` 절에 대상을 지정하는 것을 **프로젝션**이라고 한다.
결과 조회시 프로젝션 대상이 하나이면 타입을 명확히 지정할 수 있다. 반면 프로젝션 대상이 여러개이면 투플이나 DTO로 조회할 수 있다.

#### Tuple 반환
여기서 사용하는 `Tuple` 객체는 `com.querydsl.core.Tuple` 클래스이며 `select` 절의 조회 결과를 담고 있다. `Tuple` 객체에서 원하는 데이터를 꺼낼 때에는 `tuple.get(select절에 지정한 프로젝션)`과 같은 형식으로 꺼낼 수 있다. 아래는 `Tuple` 객체에서 데이터를 꺼내는 예시이다.

```java
List<Tuple> tuples = queryFactory
	.select(member.name, member.age)
	.from(member)
	.fetch();

for (Tuple tuple : tuples) {
	String name = tuple.get(member.name);
	Integer age = tuple.get(member.age);
}
```

#### DTO 반환
조회 결과를 DTO로 반환할 때 Querydsl 빈을 생성해서 반환한다. 이는 프로퍼티 접근, 필드 직접 접근, 생성자 사용 등 3가지 방법을 지원한다.

```java
// 프로퍼티 접근. 기본 생성자와 setter가 필요하다.
List<MemberDto> result = queryFactory
	.select(Projections.bean(MemberDto.class, member.name, member.age))
	.from(member)
	.fetch();

// 필드 직접 접근
queryFactory
	.select(Projections.fields(MemberDto.class, member.name, member.age))
	.from(member)
	.fetch();
	// 별칭이 다르면 as("Dto 필드의 이름")을 통해 해결하거나 ExpressionUtils.as(source, alias)를 통해 서브쿼리를 작성하고 이에 별칭을 적용하는 방법을 선택한다.

// 생성자 사용. 생성자의 타입과 맞아야 한다.
queryFactory
	.select(Projections.constructor(MemberDto.class, member.name, member.age))
	.from(member)
	.fetch();
```

#### `@QueryProjection`
Querydsl을 통해 DTO를 반환받고 싶을 때, DTO를 통해 Q 타입 파일을 생성하여 해당 타입으로 결과를 반환받을 수 있다. DTO 클래스에 생성자를 만들고 해당 생성자에 `@QueryProjection` 애노테이션을 붙이고 이를 빌드하면 해당 DTO의 Q 타입 파일이 생성된 것을 확인할 수 있다. 이제 해당 Q 타입의 DTO를 통해 결과를 받으면 된다.

```java
List<MemberDto> result = queryFactory
	.select(new QMemberDto(member.name, member.age))
	.from(member)
	.fetch();
```



### 페이징
`.offset()`과 `.limit()` 메서드 체인을 통해 페이징 조건을 추가할 수 있다.
`.offset()`은 시작 지점을 말하고,
`.limit()`는 페이지의 크기를 말한다.
따라서 `.offset()`에는 원하는 페이지의 번호가 아니라, `원하는 페이지의 번호 * 페이지 크기`가 들어가는 것이 맞다. 이 때, `offset` 범위는 0 부터 시작하는 것에 주의해야 한다.

```java
queryFactory
   .selectFrom(member)
   .orderBy(member.username.desc())
   .offset(1) // offset 범위는 0부터 시작한다.
   .limit(2) // 최대 조회 건수
   .fetch();
```

스프링 데이터 JPA의 `Page`와 `Pageable`을 활용할 수도 있다.

```java
public Page<Item> getItems(Pageable pageable) {
	List<Item> contents = queryFactory
		.selectFrom(item)
		.where(item.price.loe(20000))
		.offset(pageable.getOffset())
		.limit(pageable.getPageSize())
		.fetch();

	Long total = queryFactory
		.select(item.count())
		.from(item)
		.where(item.price.loe(20000))
		.fetchOne();

	return new PageImpl<>(content, pageable, total);

//	(미지원) 다음과 같이 작성하면 count 쿼리가 생략 가능한 경우 생략해서 처리하기 때문에 최적화 가능.
//	JPAQuery<Item> countQuery = queryFactory
//		.selectFrom(item)
//		.where(item.price.loe(20000));
	
//	return PageableExecutionUtils.getPage(content, pageable, countQuery::fetchOne);
}
```


### 집합
집합 함수와 `GrouBy` 절을 통해 `Tuple`을 반환받을 수 있다. Querydsl은 JPQL이 제공하는 모든 집합 함수를 제공한다. `.count()`, `.sum`, `.avg()`, `.max()`, `.min()`를 집합 함수로 제공한다.
`.groupBy` 절은 다음과 같이 사용할 수 있다.

```java
queryFactroy
   .select(team.name, member.age,avg())
   .from(member)
   .join(member.team, team)
   .groupBy(team.name) // team.name으로 Groupping
   .having(team.name.contains("부산")) // having절 가능
   .fetch();
```


### 조인
[조인 - 기본 조인](#조인---기본-조인)
[조인 - 세타 조인](#조인---세타-조인)
[조인 - ON 절](#조인---on-절)
[조인 - fetch 조인](#조인---fetch-조인)

#### 기본 조인
조인은 조인 메서드에 파라미터로 조인 대상과, 별칭으로 사용할 Q 타입을 지정하여 사용할 수 있다.
`join()`, `innerJoin()`, `leftJoin()`, `rightJoin()`, `fetch` 조인을 제공한다.
사용 방법은 다음과 같다.

```java
queryFactory
	.selectFrom(member)
	// 첫번째 파라미터로 조인 대상을 지정, 두번째 파라미터로 별칭으로 사용할 Q 타입을 지정한다.
	.join(member.team, QTeam.team) 
	.where(QTeam.team.name.eq(...))
	.fetch();
```

#### 세타 조인
from 절에 여러 엔티티를 선택하여 세타 조인을 할 수 있다. 세타 조인은 연관관계가 없는 필드로 조인하는 것이다. 세타 조인을 이용하면 외부 조인이 불가능하다. `.on()` 절을 활용하면 조인 대상이 필터링되고 연관관계가 없는 엔티티를 외부 조인할 수 있는 기능이 있어서 세타 조인시에도 외부 조인이 가능해진다.

#### ON 절
`.on()` 절은 조인 대상을 필터링할 수 있는 기능을 한다. 이 때, 외부조인이 아닌 내부조인을 사용하면 `where` 절에서 필터링 한 것과 기능이 동일하다. 내부조인 사용시에는 `where`절로 해결하고 외부조인시에 `on` 절의 필터링 기능이 필요하면 사용하는 것이 일관성있고 의도를 드러낼 수 있으므로 좋다.

```java
//member.team.name == "teamA" -> Join
//member.team.name != "teamA" -> null 인 tuple 반환
queryFactory
   .select(member, team)
   .from(member)
   .leftJoin(member.team, team).on(team.name.eq("teamA"))
   .fetch();
```

또한 `.on()` 절은 외부조인시 연관관계가 없는 엔티티를 조인하는 기능도 한다. 이 때, `.leftJoin()` 절에 일반 조인시와 다르게 파라미터가 하나만 들어간다. `on` 절을 활용할 때에는 `leftjoin`에 외부 조인할 대상 Q 타입을 지정하면 된다. 위 예시 코드와, 아래 예시 코드를 확인해보면 다른 점을 확인할 수 있다.

```java
// member.username == team.name
queryFactory
   .select(member, team)
   .from(member)
	 // 여기서 team은 QTeam.team 이다.
   .leftJoin(team).on(member.username.eq(team.name))
   .fetch();
```

#### fetch 조인
JPA의 페치 조인과 같은 기능으로 SQL 조인을 활용하여 연관된 엔티티를 SQL 한번에 조회하는 기능으로 지연 로딩으로 설정된 엔티티를 즉시 로딩으로 한번에 가져온다. 성능 최적화시 사용한다. 조인 뒤에 `.fetchJoin()`을 붙이면 조인 대상으로 지정된 엔티티를 페치 조인 한다.

```java
// member를 조회하면서 member와 연관된 team 엔티티도 함께 조회하여 담는다.
queryFactory
   .selectFrom(member)
   .join(member.team, team).fetchJoin()
   .where(member.username.eq("member1"))
   .fetchOne();
```


### 서브 쿼리
`com.querydsl.jpa.JPAExpressions`를 사용하여 서브쿼리를 사용할 수 있다. 상위 쿼리의 엔티티 명과 서브 쿼리의 엔티티 명이 겹치면 안되기 때문에 별도의 Q 타입 인스턴스를 생성하여 서브쿼리에서 사용하도록 한다. 

```java
// 서브 쿼리에서 사용할 QMember 인스턴스
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

일반적으로 `eq`, `goe`, `in` 절 등, 대부분의 절에서 서브 쿼리를 작성할 수 있으나 `select`, `from`절에서는 서브쿼리를 사용할 수 없다. 하이버네이트 구현체를 사용하면 `select` 절에서도 서브 쿼리를 사용할 수 있다.
Querydsl은 JPA의 JPQL을 생성한다. JPQL은 `select`, `from` 절의 서브쿼리를 지원하지 않는다. 때문에 Querydsl도 `select`, `from` 절에 서브 쿼리를 작성할 수 없다. JPA의 구현체인 하이버네이트는 `select` 절의 서브쿼리를 지원하기 때문에 해당 구현체를 사용하면 `select` 절에서 서브 쿼리를 사용할 수 있는 것이다.

`from` 절의 서브 쿼리가 필요한 상황이라면 다음과 같은 시도를 해보는 것이 좋다.
	1. 서브 쿼리를 join을 사용하도록 변경해본다.
	2. join을 통해 해결되지 않는 상황이라면 애플리케이션에서 쿼리를 2번 분리해서 실행한다.
	3. 또는 native sql을 사용하여 해결한다.

> 하지만 너무 서브쿼리에 집착하지 않는 것이 좋다. 화면에 맞춰서 쿼리를 짜다보면 복잡한 쿼리가 나오게 되고, 서브 쿼리를 사용하는 경우가 생긴다. 하지만 화면에 맞춘 코드는 재활용성이 떨어진다. 따라서 DB는 데이터만 필터링하고 그룹지어 가져오고, 화면을 위한 로직은 앱에서 해결하는 것이 좋다. 실시간 트래픽이 크게 중요하지 않다면 복잡한 쿼리는 분리하여 전송하는 것이 나은 선택일 수도 있다.  


### Case 문
Querydsl에서 `case` 문을 사용할 수 있다. `대상.when(조건1).then(결과1).otherwise(기타결과)` 를 통해 `case` 문을 작성할 수 있다. 복잡한 경우에는 `CaseBuilder`를 통해 `case` 문을 작성할 수 있다. `case` 기능이 꼭 필요한 경우에는 사용하고 가능하다면 애플리케이션 로직에서 처리하는 것이 좋다.


### 상수, 문자 더하기
상수가 필요하면 `Expressions.constant(상수)`를 사용할 수 있다. 또한 문자를 덧붙여 사용해야 하는 경우 `필드.concat(덧붙일 문자열)`을 통해 문자를 추가할 수 있다. 숫자 등 문자가 아닌 타입들은 `stringValue()`를 통해 문자로 변경해서 사용할 수 있다.


### 벌크 연산
쿼리 한번으로 대량 데이터를 수정, 삭제할 수 있다. JPQL 벌크 연산과 마찬가지로 영속성 컨텍스트에 있는 엔티티를 무시하고 실행된다. 배치 쿼리를 실행하고 나면 영속성 컨텍스트를 초기화하는 것이 안전하다.

```java
// 수정
queryFactory
	.update(item)
	.set(item.price, item.price.multiply(1.1))
	.execute();

// 삭제
queryFactory
	.delete(item)
	.where(item.name.contains("tmp"))
	.execute();
```


### SQL Function 호출
JPA와 같이 Dialect에 등록된 SQL 함수를 호출할 수 있다. 함수 SQL 함수 호출을 원하는 부분에 `Expressions.stringTemplate("function('lower', {0}, {1}, {2})", -, -, - )`
`lower` ansi 표준 함수들은 Querydsl이 상당부분 내장하고 있다.



## JPA와 QueryDSL
### 순수 JPA Repository
순수 JPA로 이루어진 Repository의 경우 `class`이기 때문에 Querydsl을 바로 사용할 수 있다.

### Spring Data JPA Repository
스프링 데이터 JPA의 경우, 인터페이스로 작성된다. 따라서 이 경우, Querydsl을 스프링 데이터 JPA Repository에서 바로 사용할 수 없다. 해결 방법으로는 사용자 정의 Repository를 작성해주고 스프링 데이터 JPA Repository에서 이를 상속받아 사용할 수 있다. 다음과 같이 스프링 데이터 JPA Repository에 사용자 정의 인터페이스를 상속받도록 하여 사용할 수 있다.

> `<interface> MemberRepository` -> (상속) -> `<interface> JpaRepository`  
> `<interface> MemberRepository` -> (상속) -> `<interface> MemberRepositoryCustom`  
> `MemberRepositoryImpl` -> (구현) -> `<interface> MemberRepositoryCustom`  

### API나 특정 화면에 특화된 복잡한 기능의 경우
화면에 특화된 복잡한 기능의 경우 특정 용도용으로 Repository를 생성하여 이를 주입받아 사용하도록 하는 방법이 있다. 이러한 기능들을 모두 한군데 몰아넣으면 재사용과 유지보수가 힘들다.
핵심 비즈니스 로직, 엔티티 검색, 재사용 가능한 기능들의 경우에는 Spring Data JPA Repository에 넣고, 공용성이 없고, 특정 API나 화면에 종속되어있는 기능들은 별도로 조회용 Repository를 만들어 사용하는 것도 좋은 방법이다.


### 스프링 데이터 JPA가 제공하는 Querydsl 기능
- QuerydslPredicateExecutor
	- https://docs.spring.io/spring-data/jpa/docs/2.2.3.RELEASE/reference/html/#core.extensions.querydsl

- Querydsl Web 지원
	- https://docs.spring.io/spring-data/jpa/docs/2.2.3.RELEASE/reference/html/#core.web.type-safe 

- QuerydslRepositorySupport
	- `QuerydslRepositorySupport`를 상속받아서 기능을 사용할 수 있다.
	- `getQuerydsl().applyPagination(pageable)`을 통해 페이징을 편리하게 변환 가능하다. Sort는 오류가 발생한다. QSort로 변환 필요.

#### Querydsl 지원 클래스를 직접 만들어 사용할 수 있다.
스프링 데이터가 제공하는 `QuerydslRepositorySupport`가 지닌 한계를 극복하기 위해  Querydsl 지원 클래스를 직접 만들어 사용할 수 있다. 이렇게 직접 만들어 사용하면 스프링 데이터가 제공하는 페이징을 편리하게 변환할 수 있고, 페이징과 카운트 쿼리를 분리할 수 있다. 또한 `QuerydslRepositorySupport`와 다르게 스프링 데이터 Sort를 지원하고 `select()`, `selectFrom()`으로 시작하게 할 수도 있다. `QuerydslRepositorySupport`에서 제공하지 않던 `QueryFactory`도 제공하게 할 수도 있다. `QuerydslRepositorySupport`의 단점을 보완하여 라이브러리를 확장하는 것이다.

