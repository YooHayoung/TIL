# JPA 공부
> 모든 출력은 가급적 로거를 통해 남긴다.
> `show_sql` 옵션은 `System.out`에 하이버네이트 실행 SQL을 남긴다.
> `org.hibernate.SQL` 옵션은 `logger`를 통해 하이버네이트 실행 SQL을 남긴다.
```yaml
spring:
	jpa:
		properties:
			hibernate:
#				show_sql: true  <- System.out
logging.level:
	org.hibernate.SQL: debug  # <- logger

```

- Setter를 막 열어두면 안되는 이유
	- Setter를 호출하면 데이터가 변하게 된다. 이를 막 열어두면 엔티티가 변경되는 것을 추적하기 힘들어질 수 있다.
	- Setter 대신에 변경지점이 명확하도록 변경을 위한 비즈니스 메서드를 만들어 사용하도록 한다.


## JPA 어노테이션 정리
- `@Entity` : 클래스를 엔티티로 선언
- `@Table` : 테이블명과 매핑
- `@Id` : PK
- `@GeneratedValue` : PK값 자동 증가
- `@Column` : 해당 속성을 컬럼명과 매핑
- `@ManyToMany` : 다대다 관계
- `@ManyToOne(fetch = FetchType.LAZY)` : 다대일 관계
- `@OneToMany(mappedBy = "매핑할Entity")` : 일대다 관계
- `@OneToOne` : 일대일 관계
	- `-ToOne` 관계는 `fetch`타입 지정 <- 기본이 즉시로딩이기 때문에 바꿔준다.
	- `-ToMany` 관계는 `mappedBy` 속성 지정
- `@JoinColumn(name = "targetEntity의 기본키")`
	- `-ToOne` 관계와 함께 붙여 외래키 지정
- `@Inheritance(strategy = InheritanceType.XXX)`
	- 상속관계 전략. 조상 class에 붙인다.
- `@DiscriminatorColumn(name = “xxx”)`
	- 상속관계 - 매핑할 컬럼 지정. 조상 class에 붙인다.
- `@DiscriminatorValue("XXX")`
	- 상속관계 - 컬럼에 입력될 값. 자손 class에 붙인다.
- `@Enumerated(EnumType.STRING) ` : EnumType
- `@Embedded` : 값타입 사용
- `@Embeddable` : 값타입 지정



## 테스트 케이스 작성시
- 테스트 케이스는 격리된 환경에서 실행하고, 끝나면 데이터를 초기화하는 것이 좋다. -> 메모리 DB 사용.
- 테스트 케이스를 위한 스프링 환경과, 애플리케이션을 실행하는 환경은 보통 다르므로 설정 파일을 다르게 사용 -> 테스트용 설정 파일 추가
- `test/resources/application.yml`
```yaml
spring:
logging.leverl:
	org.hibernate.SQL: debug
```
	- 스프링 부트는 `datasource` 설정이 없으면 기본적으로 Memory DB를 사용, `driver-class`도 현재 등록된 라이브러리를 보고 찾아줌. `ddl-auto`도 `create-drop` 모드로 동작


## 변경감지와 병합
- 준영속 엔티티 : 영속성 컨텍스트가 더이상 관리하지 않는 엔티티
- 수정 방법에는 2가지가 있음
	- 변경 감지(Dirty checking) : 영속성 컨텍스트에서 엔티티를 조회 후, 데이터 수정 -> 트랜잭션 내에서 조회, 변경 -> 트랜잭션 커밋 시점에 변경 감지 동작 후, DB에 UPDATE 실행
	- 병합(merge) : 준영속 엔티티를 영속 상태로 변경. 1차 캐시에서 엔티티 조회 -> 없으면 DB에서 엔티티 조회 후 1차 캐시에 저장 -> 조회한 영속 상태 엔티티의 모든 필드의 값을 merge 하려는 엔티티의 값으로 변경(값이 없으면  null)로 업데이트.
- 웬만하면 트랜잭션이 있는 서비스 계층에서 엔티티를 생성하고 변경 감지를 이용하여 변경하도록 한다. -> 예기지 못한 오류 발생 방지



## 페이징 + 컬렉션 엔티티 조회
- `-ToOne` 관계를 모두 페치조인.
- 컬렉션은 지연로딩으로 조회
- 지연로딩 성능 최적화를 위해 `hibernate.default_batch_fetch_size`, `@BatchSize` 적용
	- `hibernate.default_batch_fetch_size` : 글로벌 설정
	- `@BatchSize` : 개별 최적화 <- 컬렉션은 컬렉션 필드, 엔티티는 엔티티 클래스에 적용
	- 이를 이용하면 컬렉션이나 프록시 객체를 한꺼번에 설정한 size 만큼 IN 쿼리로 조회
```yaml
spring: 
	jpa: 
		properties:
			hibernate:
				default_batch_fetch_size: 1000
# DB or App이 견딜 수 있는 순간부하에 따라 설정하도록 한다.
# 100 ~ 1000 권장.
```

### 권장 순서
1. Entity 조회 방식
	1. `fetch join`을 통해 Query 수 최적화 
	2. 컬렉션 최적화 
		1. 페이징 필요시 : `default_batch_fetch_size`, `@BatchSize` 사용
		2. 페이징 필요X : `fetch join` 사용
2. 엔티티 조회 방식으로 해결 X -> DTO 조회 방식 사용
3. DTO 조회 방식으로 해결 X -> `NativeSQL` or `스프링 JdbcTemplate`

> 성능 최적화와 코드 복잡도를 고려하여 적절한 방식을 통해 성능 최적화를 하자. 유지보수를 위해서 단순한 코드가 좋지만 성능 최적화는 보통 복잡한 코드를 동반한다. 상황에 따라 효율적인 방법을 이용.


## OSIV
- Open Session In View <- Hibernate
- Open EntityManager In View <- JPA (관례상 OSIV라고 함)
```yaml
spring.jpa.open-in-view: true # or false (default: true)
```

- **OSIV on** : 최초 DB Connection 시점부터 API 응답 종료시까지 영속성 컨텍스트와 DB Conn을 유지함 -> Controller에서 지연로딩 가능
	- DB Connection Resource를 너무 오래 사용하기 때문에 connection이 부족할 수 있음
- **OSIV off** : 트랜잭션 종료 시 영속성 컨텍스트 off, DB conn 반환
	- 지연로딩을 트랜잭션 안에서 처리해야 한다 -> Contorller로 끌고갈 수 없음.
	- OSIV off 상태에서 복잡성을 관리하는 방법 : Command & Query 분리
	- [[[Command–query separation - Wikipedia](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation)]]
	- **관심사를 분리 하자**
		- OrderService : 핵심 비즈니스 로직
		- OrderQueryService : View용



#JPA/OSIV
#JPA/컬렉션 조회#
#JPA/default_batch_fetch_size 
#JPA/기타
---
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.