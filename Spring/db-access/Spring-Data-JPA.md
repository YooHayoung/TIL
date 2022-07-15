# Spring Data JPA
[1. Spring Data JPA 설명](#spring-data-jpa-설명)

[2. 쿼리 메서드 기능](#쿼리-메서드-기능)

[3. @Query 애노테이션을 사용하여 값, DTO 조회](#query-애노테이션을-사용하여-값-dto-조회)

[4. 파라미터 바인딩](#파라미터-바인딩)

[5. 유연한 반환 타입](#유연한-반환-타입)

[6. 페이징](#페이징)

[7. 벌크성 수정 쿼리](#벌크성-수정-쿼리)

[8. @EntityGraph](#entitygraph)

[9. 사용자 정의 기능 추가](#사용자-정의-기능-추가)

[10. Auditing](#auditing)

[11. Web 확장 - 도메인 클래스 컨버터](#web-확장---도메인-클래스-컨버터)
	
[12. Web 확장 - 페이징과 정렬](#web-확장---페이징과-정렬)



- - - -
## Spring Data JPA 설명
`Spring Data JPA`는 `JPA`를 편리하게 사용할 수 있도록 해주는 기술이다. 각 `repository` 클래스에서 공통적으로 생성되고 사용되는 기능들을 미리 구현하여 제공한다.

`Spring Data JPA`를 사용하지 않는 `JPA Repository`는 `Class`로 작성된다. `EntityManager`를 주입받고 `EntityManager`를 통해 저장, 조회 등의 기능을 조합하여 원하는 작업을 처리하는 메서드를 만들어 사용한다.
반면 `Spring Data JPA`는 `JpaRepository<T, ID>`를 상속받은 `Interface`로 작성된다. 이를 구현한 클래스는 `Component Scan` 대상이 되기 때문에 `@Repository`를 붙이지 않아도 스프링 빈에 등록이 된다. 실행 시점에 `Spring Data JPA`가 이를 구현한 구현 클래스를 프록시로 대신 생성해준다. 해당 인터페이스를 구현한 구현체 내부에는 `EntityManager`를 주입받아 공통으로 사용되는 기본적인 CRUD 기능을 대부분 제공한다. 추가 기능들이 필요하면 인터페이스에 특정 규칙에 맞추어 메서드를 작성하면 된다.

- `Spring Data JPA Repositody` 예시
```java
public interface MemberRepository extends JpaRepository<Member, Long>
```

`JpaRepository`에서 제공하는 기본적인 기능들은 다음과 같은 것들이 있다.

* `save(S)` : 새로운 엔티티는 저장하고 이미 존재하는 엔티티는 병합한다.
* `delete(T)` : 엔티티를 삭제한다. 내부에서 `EntityManager.remove()`가 발생한다.
* `findById(ID)` : 엔티티 하나를 조회한다. 내부에서 `EntityManager.find()`가 발생한다.
* `getOne(ID)` : 엔티티를 프록시로 조회한다. 내부에서 `EntityManager.getReference()`가 발생한다.
* `findAll()` : 모든 엔티티를 조회한다. 정렬이나 페이징 조건을 파라미터로 제공할 수 있다.

### `Spring Data JPA`의 구현체 `SimpleJpaRepository`
`Spring Data JPA`가 제공하는 공통 인터페이스의 구현체는 `org.springframework.data.jpa.repository.support.SimpleJpaRepository`이다. 
해당 구현체 내부에는 `@Repository` 애노테이션이 적용되어 JPA 예외를 스프링이 추상화한 예외로 변환해서 반환하도록 한다.
또한 `@Transactional`이 적용되어 변경 메서드를 트랜잭션 처리한다. JPA의 모든 변경은 트랜잭션 안에서 동작하게 되는데 서비스 계층에서 트랜잭션을 시작하면 해당 트랜잭션을 전파받아서 사용하고, 서비스 계층에서 트랜잭션을 시작하지 않으면 `Repository`에 적용된 `@Transactional` 애노테이션을 통해 트랜잭션을 시작하게 된다. 추가로 구현체인 `SimpleJpaRepository` 최상단에는 `@Transactional(readOnly=true)` 옵션이 있고, 내부의 변경 메서드에는 `readOnly=true` 옵션이 없다. `readOnly=true` 옵션은 데이터를 단순히 조회만 하고 변경하지 않는다는 것을 명시하여 `flush`를 생략하여 약간의 성능 향상을 얻을 수 있는 옵션이다. 변경 메서드에만 `readOnly` 옵션을 제거하여 트랜젝션에서 변경이 가능하도록 하여 성능  최적화를 한 것으로 볼 수 있다.

### `Spring Data JPA`의 `save()` 메서드
`Spring Data JPA`는 `save()` 메서드를 통해 저장과 병합을 모두 진행한다. `save()` 메서드를 통해 넘어온 엔티티가 새로운 엔티티이면 `persist`, 새로운 엔티티가 아니면 `merge`한다. 이 때, `Spring Data JPA`가 새로운 엔티티인지 판단하는 기준은 다음과 같다.

- 식별자가 객체일 때 `null` -> 새로운 엔티티로 본다.
- 식별자가 자바 기본 타입일 때 `0` -> 새로운 엔티티로 본다.

만약 새로운 엔티티를 저장하고자 할 때, 엔티티의 식별자 생성 전략이 `@GenerateValue`로 자동 생성이면 `save()` 호출 시점에 식별자가 없기 때문에 새로운 엔티티로 인식해서 `persist`한다. 하지만 `@Id`만을 사용하여 식별자 직접 할당이면 `save()` 호출 시점에 새로운 엔티티에 식별자 값이 있는 상태가 된다. 이 경우, `Spring Data JPA`는 엔티티에 식별자가 있기 때문에 `merge`하게 된다. `merge()`는 DB에 먼저 데이터가 있는지 확인하고, DB에 값이 없다면 새로운 엔티티로 인지하여 저장한다. 이는 검색 -> 삽입이 되기 때문에 비효율적이다.
이러한 경우, 엔티티에서 `Persistable` 인터페이스를 구현하여 새로운 엔티티 확인 여부를 판단하는 로직을 직접 구현해주면 된다. 아래는 `@CreatedDate`를 통한 등록시간 정보를 활용하여 새로운 엔티티인지 확인할 수 있는 로직을 작성한 예이다.

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
@NoArgConstructor(access = AccessLevel.PROTECTED)
public class Member implements Persistable<Long> {
	
	@Id
	private Long id;

	@CreatedDate
	private LocalDateTime createdDate;

	@Override
	public Long getId() { return id; }

	// @CreatedDate는 persist시에 이벤트가 동작하여 저장 시간을 입력한다.
	// 따라서 createdDate 필드가 null이면 새로운 엔티티로 볼 수 있다.
	@Override
	public boolean isNew() { return created == null; }
}
```


- - - -
`Spring Data JPA`는 기본 CRUD 기능을 제공함과 동시에 다른 기능들도 제공한다.
쿼리 메서드 기능, `@Query` 애노테이션을 사용하여 조회, 파라미터 바인딩, 반환 타입, 페이징, 벌크 연산, `@EntityGraph`, `JPA Hint&Lock` 등의 기능을 제공한다.

## 쿼리 메서드 기능
SQL 쿼리 전송을 위한 메서드를 작성하기 위해 다음과 같은 3가지 기능을 제공한다.

### 메서드 이름으로 쿼리 생성
인터페이스에 작성한 메서드의 이름을 분석하여 JPQL 쿼리를 실행하는 기능을 구현해준다. `findByUserName`, `findFirst3` 등과 같이 특정 규칙에 맞추어 메서드 이름을 작성하면 `Spring Data JPA`가 기능을 구현해준다. JPA 공식 문서를 참고하여 쿼리 메서드 필터 조건을 확인할 수 있다.

> https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation  

해당기능은 엔티티의 필드명이 변경되면 인터페이스에 정의한 메서드 이름도 함께 변경해야 한다. 변경하지 않으면 애플리케이션 시작 시점에 오류가 발생한다.


### 메서드 이름으로 JPA NamedQuery 호출
메서드 이름으로 JPA의 `NamedQuery`를 호출할 수 있다. 인터페이스에 메서드를 작성하면 해당 메서드 이름으로 대상 엔티티 클래스에서 `@NamedQuery`의 `name`과 매칭하여 쿼리를 사용할 수 있게 해준다. `NamedQuery`의 장점은 애플리케이션 로딩 시점에 오류를 잡을 수 있도록 제공하는 것이다.

```java
//Entity에 Named Query 정의
@Entity
@NamedQuery(
   name="Member.findByUsername",
   query="select m from Member m where m.username = :username"
)

.
.
.

//Repository에 사용
public interface MemberRepository extends JpaRepository<Member, Long> {
   // 위의 엔티티에서 먼저 찾는다.
   @Query(name = "Member.findByUsername") // 없어도 동작한다.
   List<Member> findByUsername(@Param("username") String username);
}
```


### `@Query` 애노테이션을 사용하여 Repository Interface에 쿼리를 직접 정의
메서드에 `@Query` 애노테이션을 통해 JPQL 쿼리를 작성하여 사용할 수 있게하는 기능이다. 사용 방법은 다음과 같다.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
   @Query("select m from Member m where m.username= :username and m.age = :age") // JPQL 쿼리 작성
   List<Member> findUser(@Param("username") String username, @Param("age") int age);
}
```

메서드 이름으로 쿼리를 생성하는 기능은 파라미터가 증가하면 메서드이름이 지저분해진다. 메서드 이름을 통한 생성 기능은 간단한 쿼리등에 사용하는 것이 좋고, 복잡한 쿼리는 해당 기능을 사용하는 것이 좋다.



## `@Query` 애노테이션을 사용하여 값, DTO 조회
`@Query` 애노테이션은 `Member` 등과 같은 객체를 결과로 받을 수 있고 자바 기본 값타입(`String`, `Long`)등과 같이 값을 조회할 수도, `DTO` 클래스 객체로도 받을 수 있다.

```java
// 값 조회.
@Query("select m.username from Member m")
List<String> findUsernameList();

// DTO로 조회. new 명령어를 사용해야 하고 조회 결과에 맞는 DTO의 생성자가 필요하다.
@Query("select new package.MemberDto(m.id, m.username, t.name from Member m join m.team t)")
List<MemberDto> findMemberDto();
```



## 파라미터 바인딩
```java
@Query("select m from Member m where m.username = ?0") // 위치기반
@Query("select m from Member m where m.username = :name") // 이름기반
@Query("select m from Member m where m.username in :names") // 이름기반 - 컬렉션
```



## 유연한 반환 타입
`Spring Data JPA`는 컬렉션, 단건, `Optional` 단건 등 유연한 반환 타입을 지원한다. 단건으로 지정한 메서드를 호출하면 `Spring Data JPA` 내부에서 `JPQL`의 `Query.getSingleResult()` 메서드를 호출한다. 여기서 조회 결과가 없으면 `NoResultException` 예외가 발생하지만 `Spring Data JPA`는 단건 조회시 이를 무시하고 `null`을 반환해준다.



## 페이징
`Spring Data JPA`는 페이징을 편리하게 이용할 수 있도록 API를 제공한다.

### 순수 JPA 페이징 쿼리
순수 JPA를 이용한 페이징은 페이징 쿼리를 통한 검색 결과와 전체 검색 결과의 수를 얻는 쿼리를 통해 페이지 계산 공식을 적용하여 페이징을 진행할 수 있다.

```java
// 페이징 쿼리
em.createQuery("select m from Member m where m.age = :age order by m.username desc")
    .setParameter("age", age)
    .setFirstResult(offset)
    .setMaxResult(limit)
    .getResultList();

// total count
em.createQuery("select count(m) from Member m where m.age = :age", Long.class)
    .setParameter("age", age)
    .getSingleResult();
``` 


### `Spring Data JPA` 페이징 API
반면 `Spring Data JPA`는 아래와 같은 페이징을 위한 API를 제공한다.
	
- `org.springframework.data.domain.Sort` : 정렬 조건
- `org.springframework.data.domain.Pageable` : 페이징 조건을 담는다. 내부에 Sort 포함
- `org.springframework.data.domain.Page` : 추가 count 쿼리 결과를 포함한 페이징 결과를 담는다.
- `org.springframework.data.domain.Slice` : 추가 count 쿼리 없이 다음 페이지만 확인 가능. (내부적으로 limit + 1)

`Pageable`은 인터페이스로 직접 페이징 조건을 전달하려면 구현체가 필요하다. 이 때, `PageRequest`를 이용하면 된다.
```java
// PageRequest.of(현재 페이지, 조회할 데이터 수, 정렬 정보)
PageRequest pageRequest = PageRequest.of(0, 3, Sort.by(Sort.Direction.DESC, "username"));

// Pageable을 구현한 PageRequest 사용 예
Page page = memberRepository.findByAge(10, pageRequest);
```

페이징을 할 때, 데이터 개수가 많아지거나 조인시에 전체 조회 결과의 개수를 포함한 쿼리를 사용하면 성능이 느려질 수 있다. 이는 `count` 쿼리를 분리하여 해결할 수 있다.
```java
@Query(value = "select m from Member m",
   countQuery = "select count(m.username) from Member m")
Page<Member> ...(Pageable pageable);
```

페이징 결과를 유지한 채로 엔티티를 DTO로 변환하려면 다음과 같이 람다를 이용하여 변환할 수 있다.
```java
Page<Member> page = memberRepository.findByAge(10, pageRequest);
Page<MemberDto> dtoPage = page.map(m -> new MemberDto(m......));
```



## 벌크성 수정 쿼리
`JPA`는 `Dirty Checking`을 통해 데이터를 수정한다. 기본적으로 단건으로 수정 쿼리가 전송되어 N개의 엔티티를 수정하면 N번의 `update` 쿼리가 발생한다. `Spring Data JPA`는 JPA의 `executeUpdate()`의 기능을 하는 `@Modifying` 애노테이션을 제공한다.

```java
@Modifying
@Query("update Member m set m.age = m.age + 1 where m.age >= :age")
int bulkAgePlus(@Param("age") int age);
```

`@Modifying` 애노테이션이 붙은 쿼리는 `Dirty Checking`을 통한 수정이 아니라 DB에 직접 수정 쿼리를 전송한다. 따라서 영속성 컨텍스트에는 수정 결과가 반영되어있지 않다. 벌크 연산 수행 후에는 영속성 컨텍스트를 초기화 해줘야 한다. `clearAutomatically` 옵션을 `true`로 설정하여 영속성 컨텍스트를 초기화 할 수 있다.



## `@EntityGraph`
`@EntityGraph` 기능은 `Fetch Join`의 간편 버전으로 연관된 엔티티들을 SQL 한번에 같이 조회하는 기능을 한다. 다음은 JPQL의 페치 조인을 사용한 예와 `@EntityGraph`를 사용한 예이다.

```java
// jpql fetchJoin
@Query("select m from Member m left join fetch m.team")
List<Member> findMemberFetchJoin();

// 공통 메서드
@Override
@EntityGraph(attributePaths = {"team"})
List<Member> findAll();

// JPQL + EntityGraph
@EntityGraph(attributePaths = {"team"})
@Query("select m from Member m")
List<Member> findMemberEntityGraph();

// 메서드 이름으로 쿼리
@EntityGraph(attributePaths = {"team"})
List<Member> findByUsername(String username);
```



## 사용자 정의 기능 추가
특정한 이유로 JPA의 `EntityManager`를 직접 사용하거나 `JdbcTemplate`, `QueryDsl` 등을 사용하여 `Repository`의 메서드를 직접 구현해야 할 수도 있다. 이 때, `JpaRepository` 인터페이스를 직접 구현해야 한다면 구현해야 할 기능이 너무 많다. `Spring Data JPA`는 이를 위해 다음과 같은 방법을 제공한다.

1. 사용자 정의 인터페이스를 생성한다. ex) `MemberRepositoryCustom`
2. 사용자 정의 인터페이스를 구현한 클래스를 작성한다. ex) `MemberRepositoryCustomImpl`
3. `JpaRepository`와 사용자 정의 인터페이스를 상속받은 `Repository` 인터페이스를 작성한다. ex) `MemberRepository`
	- 이 때, 사용자 정의 인터페이스를 구현한 클래스의 이름이 `사용자 정의 인터페이스 이름 + Impl` 또는 `Repository 이름 + Impl` 이라면, `Spring Data JPA`가 이를 인식하여 스프링 빈으로 등록한다.

1. 사용자 정의 인터페이스 생성
```java
public interface MemberRepositoryCustom {
  List<Member> findMemberCustom();
}
```

2. 사용자 정의 인터페이스 구현 클래스
```java
@RequiredArgsConstructor
public class MemberRepositoryCustomImpl implements MemberRepositoryCustom {

  private final EntityManager em;

  @Override
  public List<Member> findMemberCustom() { ... }
}
```

3. 스프링 데이터 JPA 리포지토리에 사용자 정의 인터페이스 상속
```java
public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom { 
	... 
}
```

위와 같은 방법으로 확장하지 않고 별도로 `Repository` 클래스를 만든 다음 별도로 `Bean`으로 등록하여 사용할 수도 있다. 이 경우에는 `Spring Data JPA`와는 관계없이 별도로 동작한다.


## Auditing
`Spring Data JPA`는 엔티티 생성일, 생성자, 수정일, 수정자 등을 추적할 수 있도록 자동화 하는 기능을 제공한다.

순수 JPA에서는 등록, 수정일 등의 공통 정보를 `MappedSuperclass`로 생성하고, `@PrePersist`, `@PostPersist`, `@PreUpdate`, `@PostUpdate`와 같은 JPA 이벤트 어노테이션을 통해 해당 내용을 생성, 수정하여 저장할 수 있다.

`Spring Data JPA`는 위 과정을 좀 더 편리하게 작성할 수 있는 방법을 제공한다.

- 스프링부트 설정 클래스에 `@EnableJpaAuditing` 애노테이션을 붙여 `Auditing` 기능을 활성화 한다.
- 엔티티의 원하는 컬럼에 `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`, `@LastModifiedBy` 애노테이션을 사용하여 어떤 이벤트에 어떤 컬럼을 수정할 것인지 지정한다.
- `Auditing`을 적용할 엔티티 클래스에 `@EntityListeners(AuditingEntityListener.class)` 애노테이션을 사용하여 이벤트를 적용할 수 있도록 한다.
- 등록자, 수정자의 경우 이를 처리해주는 `AuditorAware`를 스프링 빈으로 등록해야 한다.

```java
@Bean
public AuditorAware<String> auditorProvider() {
  return () -> Optional.of(세션정보 or 스프링 시큐리티 로그인 정보의 ID)
}
```

- 공통 정보를 별도 클래스에 작성하고 `@MappedSuperclass` 애노테이션을 통해 필요한 엔티티에 적용할 수도 있다. 등록일, 수정일은 모든 엔티티에 적용해야 하고 등록자, 수정자 정보는 특정 엔티티들만 필요하다면 다음과 같이 분리해서 필요한 엔티티에 필요한 정보만을 적용할 수도 있다.
```java
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public class BaseTimeEntity {
// 등록일, 수정일 정보

    @CreatedDate
    @Column(updateable = false)
    private LocalDateTime createdDate;

    @LastModifiedDate
    private LocalDateTime lastModifiedDate;
}


@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public class BaseEntity extends BaseTimeEntity {
// 등록자, 수정자 정보 - 등록일, 수정일 상속받음

    @CreatedBy
    @Column(updateable = false)
    private String createdBy;

    @LastModifiedDate
    private String lastModifiedBy;
}


@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Post extends BaseTimeEntity {
// BaseTimeEntity를 상속받아 등록일, 수정일 Auditing 적용.

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "post_id")
    private Long id;
}
```

> `@EntityListeners(AuditingEntityListener.class)`를 생략하고 스프링 데이터 JPA가 제공하는 이벤트를 엔티티 전체에 적용하려면 `orm.xml`에 특정 내용을 등록하면 된다. 필요하면 검색해보자.  



## Web 확장 - 도메인 클래스 컨버터
HTTP 파라미터로 넘어온 엔티티의 `id`값을 통해 엔티티 객체를 찾아서 바인딩할 수 있다.

```java
//Controller에서
@GetMapping("/members/{id}")
public String findMember(@PathVariable("id") Long id) {
	// 파라미터로 id 값을 받아서 repository에서 직접 검색한다.
  Member member = memberRepository.findById(id).get();
  return member.getUsername();
}

@GetMapping("/members/{id}")
public String convertorFindMember(@PathVariable("id") Member member) {
	// 파라미터로 id 값을 받았으나 도메인 클래스 컨버터가 동작하여 repository에서 엔티티를 찾아 바인딩 해준다.
  return member.getUsername();
}
```

도메인 클래스 컨버터로 파라미터를 받으면 해당 엔티티는 트랜잭션이 없는 범위에서 엔티티를 조회했기 때문에 엔티티를 변경해도 DB에 반영되지 않는다. 단순 조회용으로만 사용해야 한다. 수정이 필요한 경우, 도메인 클래스 컨버터를 이용하지 않고 직접 `Repository`에서 조회하여 트랜잭션 안에서 수정해야 한다. 모든 데이터 변경은 트랜잭션 내부에서 이루어져야 DB에 수정 쿼리가 전송되고 수정 내용이 적용될 수 있다.



## Web 확장 - 페이징과 정렬
`Spring Data JPA`는 페이징과 정렬 기능을 스프링 MVC에서 편리하게 사용할 수 있도록 해준다. `Pageable` 인터페이스를 파라미터로 받을 수 있다. `Pageable`은 인터페이스이기 때문에 실제로는 `org.springframework.data.domain.PageRequest` 객체를 생성한다.
HTTP 요청 파라미터에 `page`, `size`, `sort` 정보를 입력하면 `Pageable` 파라미터로 해당 정보를 전달받을 수 있다. 다음은 HTTP 요청 파라미터로 `Pageable`을 전달받는 예시이다.

```java
// http 요청 : /members?page=0&size=3&sort=id,desc&sort=username,desc
@GetMapping("/members")
public Page<Member> list(Pageable pageable) {
	// pageable 파라미터에 page=0, size=3, sort=id 기준 내림차순, username 기준 내림차순이 적용된 구현체 PageRequest 객체를 바인딩한다. sort는 asc가 기본값이다.
  Page<Member> page = memberRepository.findAll(pageable);
  return page;
}
```

페이지 크기의 경우 HTTP 요청 파라미터에 `page` 파라미터가 없으면 기본값을 적용한다. `application.properties`에서 `page` 크기를 글로벌 설정을 할 수도 있고, 각 메서드마다 `@PageableDefault`를 통해 Pageable의 기본값을 설정할 수도 있다.

- 글로벌 설정
```properties
#기본 페이지 크기
spring.data.web.pageable.default-page-size=10
#최대 페이지 크기
spring.data.web.pageable.max-page-size=2000
```
- 개별 설정
```java
@RequestMapping(value = "/members_page", method = RequestMethod.GET)
public String list(@PageableDefault(size = 12, sort = "username", direction = Sort.Direction.DESC) Pageable pageable) { ... }
```

만약 페이징 정보가 둘 이상이면 접두사로 구분할 수 있다. `@Qualifier`을 통해 접두사를 입력하면 HTTP 요청 파라미터에서 `접두사_page`와 같은 페이징 정보를 해당 `Pageable` 파라미터에 바인딩해준다.
```java
// HTTP 요청 : /members?member_page=0&order_page=1
@GetMapping("/members")
public String list(
  @Qualifier("member") Pageable memberPageable, // member_page 등과 같은 정보 바인딩
  @Qualifier("order") Pageable orderPageable // order_page 등과 같은 정보 바인딩
)
```


## 기타
기타 다음과 같은 기능들도 제공한다.
- Specifications(명세)
- Query By Example
- Projections
- Native Query

### Projections
`Projections` 기능은 엔티티 대신에 DTO를 편리하게 조회할 때 사용한다. 만약 전체 엔티티가 아니라 엔티티의 특정 필드만 조회하고 싶다면 조회할 엔티티의 필드를 `getter` 형식으로 지정하면 해당 필드만 선택해서 조회할 수 있다. 이를 `Projection` 이라고 한다.

```java
// 프로젝션의 반환값을 위한 interface. getter 형식으로 필드를 지정한다.
// 프로퍼티 형식(getter)의 인터페이스를 제공하면 구현체는 스프링 데이터 JPA가 제공한다.
public interface UsernameOnly {
	String getUsername();
}


public interface MemberRepository extends JpaRepository<Member, Long> {
	// 메서드 이름은 상관이 없다. 반환 타입으로 프로젝션을 인식한다.
	List<UsernameOnly> findProjectionsByUsername(String username);
}

// 위 메서드를 수행하면 select m.username from member m where m.username='m1'; 과 같은 쿼리가 수행되어 username만을 select 절로 조회한다.
```

#### 인터페이스 기반의 프로젝션
프로젝션을 위해 프로퍼티 형식(getter)의 인터페이스를 제공하면 구현체는 스프링 데이터 JPA가 제공한다. 또한 아래와 같이 스프링의 SpEL 문법도 지원한다. 하지만 SpEL 문법을 사용하면 DB에서 엔티티 필드를 다 조회해온 다음에 계산한다. JPQL select 절의 최적화가 안된다.
```java
public interface UsernameOnly {
	@Value("#{target.username + ' ' + target.age + ' ' + target.team.name}")
	String getUsername();
}
```

#### 클래스 기반 프로젝션
인터페이스가 아니라 클래스 기반의 구체적인 DTO 형식도 가능하다. 해당 방식은 생성자의 파라미터 이름으로 매칭된다.
```java
public class UsernameOnlyDto {
	private final String username;

	public UsernameOnlyDto(String username) { this.username = username; }

	public String getUsername() { return username; }
}
```

#### 동적 Projections
프로젝션에 제네릭 타입을 주면 동적으로 프로젝션 데이터를 변경할 수 있다.
```java
<T> List<T> findProjectionsByUsername(String username, Class<T> type);
```

#### 프로젝션 중첩
프로젝션에 프로젝션을 두어 중첩으로 구조를 처리할 수 있다.
```java
public interface NestedClosedProjection {
	String getUsername();
	TeamInfo getTeam();
	
	interface TeamInfo { String getName(); }
}
// 위 프로젝션을 이용하면 아래와 같은 SQL을 수행한다.
/*
select
      m.username as col_0_0_,
      t.teamid as col_1_0_,
      t.teamid as teamid1_2_,
      t.name as name2_2_
from 
member m 
  left outer join
      team t
          on m.teamid=t.teamid
where 
      m.username=?
*/
```

프로젝션은 대상이 루트 엔티티면 JPQL SELECT 절을 최적화 할 수 있다. 이 경우는 유용하게 사용가능하다. 하지만 루트 엔티티를 넘어가게 되면 `left outer join` 처리되기 때문에 모든 필드를 SELECT해서 엔티티로 조회한 다음 계산한다. 따라서 JPQL SELECT 최적화가 불가능하다. 때문에 단순할 때에만 프로젝션을 사용하고, 복잡해지면 QueryDSL을 사용하는 것이 좋다.


### 네이티브 쿼리
DB SQL 쿼리를 직접 작성하여 DB에 해당 쿼리를 직접 전송할 수 있도록 한다. 네이티브 쿼리는 재사용이 거의 불가능하기 때문에, 특정 DB에 의존적이기 때문에 가능하면 사용하지 않는 것이 좋다.

`Spring Data JPA` 기반 네이티브 쿼리는 페이징을 지원하고, `Object[]`, `Tuple`, `DTO` 등의 반환 타입을 지원한다. 하지만 `Sort` 파라미터를 통한 정렬이 정상 동작하지 않을 수도 있고, 쿼리의 문법을 애플리케이션 로딩 시점에 확인할 수 없으며, 동적 쿼리가 불가능하다.

네이티브 쿼리를 작성하는 방법은 `@Query` 애노테이션에 `nativeQuery = true` 속성을 전달하면 된다. 해당 애노테이션에 전달된 쿼리는 네이티브 SQL로 동작한다. JPQL과의 차이로는, JPQL은 위치 기반 파라미터를 1부터 시작하지만 네이티브 쿼리는 0부터 시작한다.

네이티브 SQL의 결과를 엔티티가 아닌 DTO로 변환하려면 DTO 대신 JPA TUPLE을 사용하여 조회하는 방법, MAP을 사용하는 방법, `@SqlResultSetMapping` 애노테이션을 사용하는 방법, `Hibernate ResultTransformer`를 사용하는 방법, `JdbcTemplate`, `MyBatis`를 사용하는 방법 등이 있다.
네이티브 SQL을 DTO로 조회할 때에는 `JdbcTemplate`, `MyBatis`를 사용하는 방법을 가장 권장한다.

조회 쿼리는 네이티브 쿼리를 통해 작성하고, 조회 결과를 프로젝션을 통해 받으면 프로젝션과 네이티브 쿼리를 활용할 수 있다.

동적 네이티브 쿼리를 작성하려면 하이버네이트를 직접 활용하거나, 스프링 JdbcTemplate, myBatis 등을 활용하는 방법이 있다. 아래는 하이버네이트의 기능을 사용하여 네이티브 쿼리로 동적 쿼리를 작성한 예이다.

```java
String sql = "select m.username as username from member m";
  List<MemberDto> result = em.createNativeQuery(sql)
          .setFirstResult(0)
          .setMaxResults(10)
          .unwrap(NativeQuery.class)
          .addScalar("username")
          .setResultTransformer(Transformers.aliasToBean(MemberDto.class))
          .getResultList();
```
