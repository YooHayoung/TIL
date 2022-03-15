# Spring Data JPA

## JPA와 Spring Data JPA

### 순수 JPA 기반 Repository

```java
@Repository
public class MemberJpaRepository {

   @PersistenceContext
   private EntityManager em;

   public Member save(Member member) {
      return em.persist(member);
   }

   public Optional<Member> findById(Long id) {
      return Optional.ofNullable(em.find(Member.class, id));
   }

   public List<Member> findAll() {
      return em.createQuery("select m from Member m", Member.class).getResultList();
   }

   .
   .
   .

}
```
- 순수 JPA 기반 리포지토리는 EntityManager 의존성을 주입해주고 기본적인 CRUD를 직접 작성한다.
  - JPA에서 U update는 DirtyChecking을 통해 이루어진다.
- Id pk 기반 검색, 전체 검색, 저장, 삭제 등등 기본적인 메서드를 직접 구현하였다.
- 하지만 Spring Data JPA는 그럴 필요가 없다. 다음을 보자

### Spring Data JPA Repository
```java
public interface MemberRepository extends JpaRepository<Member, Long>
```
- MemberRepository는 메서드가 없고 인터페이스다.
- 근데 위에서 작성한 순수 JPA 기반 Repository와 같이 동작한다.

## 어떻게??
- Spring이 JpaRepository를 상속받은 interface를 보고 구현체를 대신 생성하여 주입해준다.
- Spring이 생성하여 주입한 구현체에 기본적인 기능들이 들어있다. 얘네를 사용했기 때문에 동일하게 동작한다.
- `org.springframework.data.repository.Repository`를 구현한 클래스는 스캔 대상이 되어 스프링 빈에 등록된다.
  - JpaRepository를 상속하여도 위와 같다.
- `@Repository`를 붙이지 않아도 된다.
  - 컴포넌트 스캔을 스프링 데이터 JPA가 자동으로 처리한다.
  - JPA 예외를 스프링 예외로 변환하는 과정도 자동으로 처리한다.

<br>

# 공통 인터페이스 기능

## 공통 인터페이스 설정
```java
@Configuration
@EnableJpaRepositories(basePackages = "...")
public class AppConfig {}
```
- 스프링부트 사용시 생략 가능하다.

## 공통 인터페이스 분석
- JpaRepository -> PagindAndSortingRepository -> CrudRepository -> Repository 상속관계
- 각 인터페이스의 메서드들은 라이브러리를 들어가서 확인해보자
- 공통 인터페이스 덕분에 DB를 변경하여도 기본적인 기능들은 유사하게 제공한다.
- 주요 메서드
  - save(S) : 새로운 Entity는 저장하고 이미 존재하는 Entity는 병합
  - delete(T) : Entity 삭제. 내부에서 EntityManager.remove()
  - findById(ID) : 엔티티 하나 조회. 내부에서 EntityManager.find()
  - getOne(ID) : Entity를 프록시로 조회한다. 내부에서 EntityManager.getReference()
  - findAll() : 모든 Entity 조회. 정렬이나 페이징 조건을 파라미터로 제공할 수 있다.

<br>

---
# Spring Data JPA 기능들
Spring Data JPA는 위와 같이 기본적인 CRUD 기능들을 제공함과 동시에 다른 기능들도 제공한다.

## 쿼리 메소드 기능

- 쿼리 메소드 기능 3가지
  - 메소드 이름으로 쿼리 생성
  - 메소드 이름으로 JPA NamedQuery 호출
  - `@Query` 어노테이션을 사용하여 Repository Interface에 쿼리 직접 정의

<br>


### 메소드 이름으로 쿼리 생성
- 메소드 이름을 분석하여 JPQL 쿼리를 실행한다.
- 쿼리 메소드 필터 조건은 스프링 데이터 JPA 공식 문서를 참고하자.
- https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation
- find...By, read..., query..., get...By
- count...By : Count - long
- exists...By : Exists - boolean
- delete...By : Delete - long
- findDistinct, findMemberDistinctBy : Distinct
- findFirst3, findFirst, findTop, findTop3 : Limit
- 간단한 쿼리시 사용한다.
<br>

<b>해당 기능은 엔티티의 필드명이 변경되면 인터페이스에 정의한 메서드 이름도 꼭! 함께 변경해야 한다. 아니면 애플리케이션 시작 시점에 오류가 발생한다.<br>애플리케이션 로딩 시점에 오류를 인지할 수 있는 것이 스프링 데이터 JPA의 매우 큰 장점이다.</b>

<br>

### 메소드 이름으로 JPA NamedQuery 호출
- JPA의 NamedQuery를 호출할 수 있다.
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
- NamedQuery의 장점은 애플리케이션 로딩 시점에 오류를 잡을 수 있도록 제공한다.

<br>

### @Query 어노테이션을 사용하여 Repository Interface에 쿼리 직접 정의
- Repository의 메서드에 JPQL 쿼리 작성한다.
```java
public interface MemberRepository extends JpaRepository<Member, Long> {
   @Query("select m from Member m where m.username= :username and m.age = :age") // JPQL 쿼리 작성
   List<Member> findUser(@Param("username") String username, @Param("age") int age);
}
```
- 이 기능도 NamedQuery 처럼 애플리캐이션 로딩 시점에 오류를 잡을 수 있다.
- 메소드 이름으로 쿼리 생성 기능은 파라미터가 증가하면 메서드 이름이 지저분해진다. 따라서 해당 기능을 자주 사용하게 된다.

<br>

## @Query 어노테이션을 사용하여 값, DTO 조회하기
- 단순히 값 하나 조회
  ```java
  @Query("select m.username from Member m")
  List<String> findUsernameList();
  ```
- DTO 직접 조회
  ```java
  @Query("select new package.MemberDto(m.id, m.username, t.name from Member m join m.team t)")
  List<MemberDto> findMemberDto();
  ```
  - DTO로 조회하려면 JPA의 `new` 명령어를 사용해야 한다.
  - 생성자가 맞는 DTO도 필요하다.


<br>

## 파라미터 바인딩
- 이름 기반 파라미터 바인딩
```java
select m from Member m where m.username = ?0 // 위치기반 - 쓰지말자
select m from Member m where m.username = :name // 이름기반
select m from Member m where m.username in :names // 컬렉션 파라미터 바인딩

public interface MemberRepository extends JpaRepository<Member, Long> {
   @Query("select m from Member m where m.username= :username and m.age = :age") // JPQL 쿼리 작성
   List<Member> findUser(@Param("username") String username, @Param("age") int age);
}
```
- 코드 가독성과 유지보수를 위해 이름 기반 파라미터 바인딩을 사용하자

<br>

## 반환 타입
- Spring Data JPA는 유연한 반환 타입을 지원한다
  - 컬렉션
  - 단건
  - Optinal 단건
- 단건으로 지정한 메서드를 호출하면 Spring Data JPA는 내부에서 JPQL의 Query.getSingleResult() 메서드를 호출한다. 여기서 조회결과가 없으면 NoResultException 예외 발생. 그러나 Spring Data JPA는 단건 조회시 이 예외를 무시하고 null을 반환해준다.

<br>

## 페이징
### 순수 JPA 페이징
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
  - 위를 이용하여 페이지 계산 공식 적용해야 한다.

### Spring Data JPA 페이징
- `org.springframework.data.domain.Sort` : 정렬
- `org.springframework.data.domain.Pageable` : 페이징. 내부에 Sort 포함
- `org.springframework.data.domain.Page` : 추가 count 쿼리 결과를 포함하는 페이징
- `org.springframework.data.domain.Slice` : 추가 count 쿼리 없이 다음 페이지만 확인 가능. (내부적으로 limit + 1)

  ```java
  // count 쿼리 사용
  Page<Member> findByUsername(String name, Pageable pageable);
  // count 쿼리 사용 X
  Slice<Member> findByUsername(String name, Pageable pageable);
  // count 쿼리 사용 X
  List<Member> findByUsername(String name, Pageable pageable);
  List<Member> findByUsername(String name, Sort sort);
  ```

- 페이지 사용 예제
   ```java
   // Repository Method
   Page<Member> findByAge(int age, Pageable pageable);

   ...

   // use ex
   PageRequest pageRequest = PageRequest.of(0, 3, Sort.by(Sort.Direction.DESC, "username")); // 현재 페이지, 조회할 데이터 수, 정렬 정보 입력
   Page<Member> page = memberRepository.findByAge(10, pageRequest);

   List<Member> content = page.getContent(); //조회된 데이터
   assertThat(content.size()).isEqualTo(3); //조회된 데이터 수
   assertThat(page.getTotalElements()).isEqualTo(5); //전체 데이터 수
   assertThat(page.getNumber()).isEqualTo(0); //페이지 번호
   assertThat(page.getTotalPages()).isEqualTo(2); //전체 페이지 번호
   assertThat(page.isFirst()).isTrue(); //첫번째 항목인가?
   assertThat(page.hasNext()).isTrue(); //다음 페이지가 있는가?
   ```

- count Query를 분리할 수 있다.
  ```java
  @Query(value = "select m from Member m",
      countQuery "select count(m.username) from Member m")
  Page<Member> ...(Pageable pageable);
  ```
  - 데이터 개수가 많아지고 조인시 성능이 느려질 수 있다. count 쿼리를 분리하여 해결할 수 있다.

- 페이지를 유지하면서 엔티티를 DTO로 변환하기
   ```java
   Page<Member> page = memberRepository.findByAge(10, pageRequest);
   Page<MemberDto> dtoPage = page.map(m -> new MemberDto(m......));
   ```

## 벌크성 수정 쿼리
- JPA는 Dirty Checking 을 통해 update 한다.
- 하지만 여러 데이터를 한번에 수정해야 한다면?
- DB에 쿼리를 날리면 편하다.
   ```java
   @Modifying
   @Query("update Member m set m.age = m.age + 1 where m.age >= :age")
   int bulkAgePlus(@Param("age") int age);
   ```
  - 벌크성 수정, 삭제 쿼리는 `@Modifying` 어노테이션을 사용한다.
  - 사용하지 않으면 예외 발생한다.
  - 벌크성 쿼리를 실행하고 다시 조회해야 한다면 `clearAutomatically` 옵션을 `true`로 설정하여 영속성 컨텍스트를 초기화시켜주자.
  - 안그러면 영속성 컨텍스트에 과거 값이 남아서 문제가 될 수 있다.



## @EntityGraph
- 연관된 엔티티들을 SQL 한번에 조회하는 방법이다.
- JPQL의 fetchJoin을 잘 이해해야 한다.
- 연관된 엔티티를 한번에 조회하려면 fetchJoin이 필요하다.
   ```java
   // jpql fetchJoin
   @Query("select m from Member m left join fetch m.team")
   List<Member> findMemberFetchJoin();
   ```
- 스프링 데이터 JPA는 JPA가 제공하는 엔티티 그래프 기능을 편리하게 사용하도록 도와준다.
- 이를 사용하면 JPQL 없이 fetchJoin을 사용할 수 있다.

   ```java
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
   - fetchJoin의 간편 버전이다.
   - left outer join 사용한다.

## JPA Hint & Lock
- JPA Hint
  - JPA 쿼리 힌트.
  - SQL 힌트가 아니라 JPA 구현체에게 제공하는 힌트다.
  - readOnly 등을 힌트로 제공하여 조회시 영속성 컨텍스트에 보관되지 않도록, update 되지 않도록 (성능 최적화) 할 수 있다.
  - 성능 테스트 해보고 필요하다면 사용한다.
- Lock
  - 따로 공부해보자.

<br>

---
# 확장 기능

## 사용자 정의 리포지토리 구현

- 스프링 데이터 JPA Repository는 인터페이스만 정의하고 구현체는 스프링이 자동으로 생성한다.
- 스프링 데이터 JPA가 제공하는 인터페이스를 직접 구현한다면 구현해야하는 기능이 너무 많다...
- 여러 이유로 인터페이스의 메서드를 직접 구현하고 싶다면?
  - JPA 직접 사용 (EntityManager)
  - 스프링 JDBC Template 사용
  - MyBatis
  - DB Connection 직접 사용
  - Querydsl 등등

다음 방법을 통해 사용자 정의 리포지토리를 구현한다.

<br>

### 사용자 정의 인터페이스 생성
```java
public interface MemberRepositoryCustom {
  List<Member> findMemberCustom();
}
```

### 사용자 정의 인터페이스 구현 클래스
```java
@RequiredArgsConstructor
public class MemberRepositoryImpl implements MemberRepositoryCustom {

  private final EntityManager em;

  @Override
  public List<Member> findMemberCustom() { ... }
}
```

### 스프링 데이터 JPA 리포지토리에 사용자 정의 인터페이스 상속
```java
public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom { ... }
```
  - 이후 구현한 사용자 정의 메서드를 호출하여 사용한다.

### 사용자 정의 리포지토리 구현시 규칙이 있다.
- 사용자 정의 인터페이스는 상관이 없다.
- 위 인터페이스를 구현한 클래스의 이름은 Repository 인터페이스 이름 + `Impl` 이어야 한다.
  - `MemberRepository`라면 `MemberRepositoryImpl`로 지어야 한다.
- 그러면 스프링 데이터 JPA가 인식해서 스프링 빈으로 등록한다.

*스프링 데이터 2.x 부터는 사용자 정의 구현 클래스에 사용자 정의 인터페이스 명 + `Impl`방식도 지원한다*

## Auditing
- 엔티티를 생성, 변경할 때 변경한 사람과 시간을 추척하고 싶으면?
  - 등록일
  - 수정일
  - 등록자
  - 수정자 등을 Data로 관리한다.
- 스프링 데이터 JPA는 이러한 데이터를 자동으로 생성, 수정 하도록 도와준다.

### 순수 JPA 에서는
- 등록일, 수정일 등의 정보를 MappedSuperclass로 생성하고
- JPA 이벤트 어노테이션을 통해 해당 내용을 생성, 수정하여 저장하도록 한다.
  - JPA 주요 이벤트 어노테이션은 `@PrePersist`, `@PostPersist`, `@PreUpdate`, `@PostUpdate`가 있다.

### 스프링 데이터 JPA를 이용하면
- 스프링부트 설정 클래스에 `WEnableJpaAuditing`을 적용한다.
- 엔티티에 `@EntityListeners(AuditingEntityListener.class)`를 적용한다.
- 컬럼에 `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`, `@LastModifiedBy`를 사용한다.
- 등록자 수정자를 처리해주는 `AuditorAware`를 스프링 빈으로 등록한다.
  ```java
  @Bean
  public AuditorAware<String> auditorProvider() {
    return () -> Optional.of(세션정보 or 스프링 시큐리티 로그인 ID)
  }
  ```
  *대부분의 엔티티는 등록일, 수정일이 필요하지만, 등록자, 수정자는 필요없을 수도 있다. 그래서 Base Type을 분리하고 원하는 타입을 상속해서 사용하도록 한다.*

  *`@EntityListeners(AuditingEntityListener.class)`를 생략하고 스프링 데이터 JPA가 제공하는 이벤트를 엔티티 전체에 적용하려면 `orm.xml`에 등록한다. 필요하면 검색해서 찾아보자.*


## Web 확장 - 도메인 클래스 컨버터
- HTTP 파라미터로 넘어온 엔티티의 아이디로 엔티티 객체를 찾아서 바인딩한다.
- 도메인 클래스 컨버터 사용 전
  ```java
  //Controller에서
  @GetMapping("/members/{id}")
  public String findMember(@PathVariable("id") Long id) { //
    Member member = memberRepository.findById(id).get(); //
    return member.getUsername();
  }
  ```
- 도메인 클래스 컨버터 사용 후
  ```java
  //Controller에서
  @GetMapping("/members/{id}")
  public String findMember(@PathVariable("id") Member member) { //
    return member.getUsername();
  }
  ```
- Http 요청은 id를 받으나 도메인 클래스 컨버터가 중간에 동작해서 회원 엔티티 객체를 반환한다.
- 도메인 클래스 컨버터도 Repository를 사용하여 엔티티를 찾는다.
  
  *도메인 클래스 컨버터로 엔티티를 파라미터로 받으면, 이 엔티티는 단순 조회용으로 사용해야 한다. 트랜잭션이 없는 범위에서 엔티티를 조회했기 때문에 엔티티를 변경해도 DB에 반영되지 않는다.*

## Web 확장 - 페이징과 정렬
- 스프링 데이터가 제공하는 페이징과 정렬 기능을 스프링 MVC에서 편리하게 사용할 수 있다.
  ```java
  @GetMapping("/members")
  public Page<Member> list(Pageable pageable) {
    Page<Member> page = memberRepository.findAll(pageable);
    return page;
  }
  ```
- 파라미터로 `Pageable`을 받을 수 있다.
- `Pageable`은 인터페이스다. 실제로는 `org.springframework.data.domain.PageRequest` 객체를 생성한다.

### 요청 파라미터
ex) `/members?page=0&size=3&sort=id,desc&sort=username,desc`
- page : 현재 페이지, 0부터 시작
- size : 한 페이지에 노출할 데이터 건수
- sort : 정렬 조건 정의
  - 정렬 속성, 정렬 속성...(ASC|DESC), 정렬 방향을 변경하고 싶으면 sort 파라미터 추가한다.(asc는 기본값. 생략 가능)

### 기본값 설정
- 글로벌 설정 : Spring Boot
  ```spring
  spring.data.web.pageable.default-page-size=10 /# 기본 페이지 사이즈/
  spring.data.web.pageable.max-page-size=2000 /# 최대 페이지 사이즈/
  ```
- 개별 설정 : `@PageableDefault` 어노테이션 사용
  ```java
  @RequestMapping(value = "/members_page", method = RequestMethod.GET)
  public String list(@PageableDefault(size = 12, sort = "username", direction = Sort.Direction.DESC)) Pageable pageable { ... }
  ```

### 접두사
- 페이징 정보가 둘 이상이면 접두사로 구분한다.
- `@Qualifier`에 접두사명 추가 "{접두사명}_xxx"
- ex) `/members?member_page=0&order_page=1`
  ```java
  public String list(
    @Qualifier("member") Pageable memberPageable,
    @Qualifier("order") Pageable orderPageable, ...
  )
  ```

### Page 내용을 DTO로 변환하기
- 엔티티를 외부로 노출하면 여러 문제가 발생할 수 있다. (API spec 자체가 바뀌는 등)
- 꼭 엔티티를 DTO로 변환해서 반환해야 한다.
- Page는 `map()`을 지원해서 내부 데이터를 다른 것으로 변경할 수 있다.
  ```java
  @GetMapping("/members")
  public Page<MemberDto> list(Pageable pageable) {
    Page<Member> page = memberRepository.findAll(pageable);
    Page<MemberDto> pageDto = page.map(MemberDto::new);
    return pageDto;
  }
  ```

*DTO는 Entity로 봐도 괜찮다. Entity는 가급적이면 DTO로 보지않는게 좋다.* ...?

### 만약 Page를 1부터 시작하려면?
- 2가지 방법이 있다.
- Pageable, Page를 파라미터와 응답값으로 사용하지 않고 직접 클래스를 만들어서 처리한다.
  - 그 후, 직접 PageRequest(Pageable 구현체)를 생성해서 Repository에 넘긴다.
  - 물론 응답값도 Page 대신에 직접 만들어서 제공해야 한다.
- `wpring.data.web.pageable.one-indexed-parameters`를 `true`로 설정한다.
  - 하지만 이 방법은 web에서 `page`파라미터를 -1 처리 할 뿐이다.
  - 응답값인 `Page`에 모두 0 페이지 인덱스를 사용하는 한계가 있다.
  ```json
  // one-indexed-parameters : Page 1 요청 : /members?page=1
  {
    "content": [ ... ],
    "pageable": {
      "offset": 0,
      "pageSize": 10,
      "pageNumber": 0 // page 1 전송했으나 응답 페이지 인덱스 0
    },
    "number": 0, // page 1 전송했으나 응답 페이지 인덱스 0
    "empty": false
  }
  ```

# 스프링 데이터 JPA 분석

## 스프링 데이터 JPA 구현체
- 스프링 데이터 JPA가 제공하는 공통 인터페이스의 구현체
- `org.springframework.data.jpa.repository.support.SimpleJpaRepository`
- `@Repository`적용 : JPA 예외를 스프링이 추상화한 예외로 변환해서 반환한다.
- `@Transactional` 트랜잭션 적용
  - JPA의 모둔 변경은 트랜잭션 안에서 동작한다.
  - 스프링 데이터 JPA는 변경 메서드를 트랜잭션 처리한다.
  - 서비스 계층에서 트랜잭션을 시작하지 않으면 Repository 계층에서 트랜잭션을 시작.-
- `@Transactinal(readOnly = true)`
  - 데이터를 조회만 하는 트랜잭션에서 `readOnly = true`옵션을 사용하면 `flush`를 생략하여 약간의 성능 향상

## 새로운 엔티티인지 기존 엔티티인지 구별하는 방법
- JPA는 `save()`메서드를 통해 `insert`, `update` 둘 다 진행한다.
- 새로운 엔티티이면 `persist`
- 기존 엔티티이면 `merge`

### 새로운 엔티티를 판단하는 기본 전략
- 식별자가 객체일 때 `null`
- 식별자가 자바 기본 타입일 때 `0`
- `Persistable` 인터페이스를 구현하여 판단 로직 변경 가능

*등록시간(`@CreatedDate`)을 조합해서 사용하면 이 필드로 새로운 엔티티 여부를 편리하게 확인할 수 있다.( Override `getId()`, `isNew() `)*


# 나머지 기능들

## Specifications

## Query By Example

## Projections

## Native Query





<br><br><br><br>
---
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.