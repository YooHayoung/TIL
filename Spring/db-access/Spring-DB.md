# 스프링 DB
[1. JDBC](#jdbc)

[2. 커넥션 풀](#커넥션-풀)

[3. DataSource](#datasource)

[4. 트랜잭션](#트랜잭션)

[5. 스프링의 트랜잭션](#스프링의-트랜잭션)

   - [5.1. 선언적 트랜잭션 관리](#선언적-트랜잭션-관리)
	
   - [5.2. 프로그래밍 방식 트랜잭션 관리](#프로그래밍-방식-트랜잭션-관리)
	
[6. 스프링의 SQLException 예외 처리](#스프링의-sqlexception-예외-처리)

[7. @Transactional 옵션](#transactional-옵션)

[8. 스프링 트랜잭션 전파](#스프링-트랜잭션-전파)


<br>

---
## JDBC
애플리케이션 서버에서 DB 데이터를 가져오거나 삽입할 때 일반적으로 다음 과정을 거친다.
	
1. 커넥션 연결 : 주로 TCP/IP를 사용하여 DB와 애플리케이션의 커넥션을 연결
2. SQL 전달 : 애플리케이션 서버는 DB가 이해할 수 있는 SQL을 연결된 커넥션을 통해 DB에 전달한다.
3. 결과 응답 : DB는 전달받은 SQL을 수행하고 그 결과를 응답한다. 애플리케이션 서버는 응답 결과를 활용한다.

애플리케이션에서 위 과정을 코드로 구현하면 DB에 작업을 수행할 수 있다. 
하지만 각각의 DB마다 사용 방법이 모두 다르다. 만약 `Oracle` DB를 사용하다가 `Mysql` DB를 사용하게 되면 DB를 사용하는 모든 코드를 변경해야 하며, DB마다 사용 방법을 모두 학습해야 한다는 문제가 있다.

JDBC는 이러한 문제점을 해결하기 위해 등장하였다. JDBC(Java Database Connectivity)는 표준 인터페이스로 자바에서 DB에 접속할 수 있도록하는 API이다. 이 JDBC 표준 인터페이스를 각각의 DB 벤더에서 해당 DB에 맞게 구현하여 제공하는 라이브러리를 JDBC 드라이버라고 한다. 이제 개발자는 JDBC 인터페이스의 사용법만 알면 되고, DB를 변경하게되면 구현체인 JDBC 드라이버만 DB에 맞게 교체해주면 된다.

JDBC를 통해 데이터베이스에 연결하기 위해서는 JDBC가 제공하는 `DriverManager.getConnection(URL, ID, PW)`를 사용하면 된다. `DriverManager`는 라이브러리에 등록된 DB 드라이버들을 관리하고 커넥션을 획득하는 기능을 제공한다. 


[처음으로](#스프링-db)


## 커넥션 풀
애플리케이션에서 DB에 접근하여 어떤 작업을 수행하려면 가장 먼저 DB 커넥션을 획득해야 한다. 커넥션을 생성하는 과정은 다음과 같다.

1. 애플리케이션의 DB 드라이버에서 DB와 TCP/IP 커넥션 연결을 시도한다. 이 때, TCP/IP 연결을 위한 `Three way handshacke` 등의 네트워크 동작이 발생한다.
2. DB 드라이버는 TCP/IP 커넥션이 연결되면 ID와 PW, 기타 부가정보를 DB에 전달한다.
3. DB는 전달받은 정보를 통해 내부 인증을 완료하고 내부에 DB 세션을 생성한다.
4. DB는 커넥션 생성이 완료됨을 DB 드라이버에게 응답으로 전달한다.
5. DB 드라이버는 전달받은 응답을 통해 커넥션 객체를 생성하여 클라이언트에 반환한다.

만약 애플리케이션에서 DB에 접근하여 작업을 해야할 때 마다 커넥션을 생성하고 작업을 마치면 커넥션을 종료한다면 위와 같은 커넥션 생성 과정을 매 요청마다 수행해야한다. 커넥션 생성 작업은 비용이 아주 비싼 작업이다. DB와 애플리케이션 서버는 커넥션을 새로 생성하기 위한 리소스를 매번 사용해야 하고, 커넥션을 생성하는 시간이 응답시간에 추가되기 때문에 사용자에게 좋지 않은 경험을 줄 수 있다는 문제가 있다.

이를 해결하기 위해 커넥션을 미리 생성해두고 필요할 때 이를 꺼내서 사용하고, 반환하는 커넥션 풀이라는 방법을 사용한다.

### 커넥션을 미리 만들어두는 커넥션 풀
애플리케이션 시작 시점에 커넥션을 필요한 수 만큼 미리 만들어두고 커넥션 풀에 보관한다. 커넥션 풀에 들어있는 커넥션은 TCP/IP로 DB와 커넥션이 연결되어 있는 상태이기 때문에 언제든지 즉시 SQL을 DB에 전달할 수 있다.

커넥션 풀을 사용하면 매 요청마다 커넥션을 새로 생성하지 않기 때문에 응답 속도가 빨라진다. 또한 커넥션 풀은 서버당 최대 커넥션 수를 제한할 수도 있다. 따라서 DB에 무한정 연결이 생성되는 것을 막아주기 때문에 DB를 보호하는 효과도 있다.

커넥션 풀을 사용할 때 주의할 점은 커넥션을 모두 사용하고 나면 커넥션을 종료하는 것이 아니라 다음에 다시 사용할 수 있도록 커넥션이 살아있는 상태로 커넥션 풀에 반환해야 한다는 것이다.

커넥션 풀은 개념적으로 단순하여 직접 구현할 수도 있으나 사용이 편리하고 성능도 뛰어난 오픈소스 커넥션 풀이 많기 때문에 오픈소스를 사용하는 것이 좋다. 대표적인 커넥션 풀 오픈소스는 `HikariCP`, `commons-dbcp2`, `tomcat-jdbc pool` 등이 있다. 스프링 부트 2.0 부터는 `HikariCP`를 기본 커넥션 풀로 제공한다.


[처음으로](#스프링-db)


## DataSource
`DataSource`는 커넥션을 획득하는 방법을 추상화한 인터페이스이다.
`DriverManager`처럼 커넥션을 직접 생성하여 사용하고 종료하도록 하다가 `HikariCP`와 같은 커넥션 풀을 사용하도록 변경하면 의존관계가 변경되기 때문에 커넥션을 획득하는 애플리케이션 코드도 함께 변경해야 한다. 이러한 문제를 해결하기 위해 자바에서 `DataSource` 인터페이스를 제공한다.

대부분의 커넥션 풀은 `DataSource` 인터페이스를 이미 구현해두었기 때문에 이를 사용만 하면 된다. 하지만 `DriverManager`는 `DataSource` 인터페이스를 사용하지 않기 때문에 직접 사용해야한다. 이를 해결하기 위해 스프링은 `DriverManagerDataSource`라는 `DataSource`를 구현한 클래스를 제공한다.

`DriverManager`와 `DataSource`의 커넥션 획득 방법에는 차이가 있다. `DriverManager`는 커넥션 획득 마다 `URL, ID, PW` 파라미터를 넘긴다. 반면 `DataSource`는 처음 객체 생성시에만 필요한 파라미터를 넘기고 커넥션을 획득할 때에는 파라미터를 넘길 필요가 없다. `DataSource`는 설정과 사용을 분리하게 한 것이다. 이렇게 설정과 사용을 분리하게 되면 변경에 좀 더 유연하게 대처할 수 있다.

### DataSource 자동 등록
스프링 부트는 `application.properties`의 다음 속성을 통해 `DataSource`를 생성하고 `dataSource`라는 이름으로 스프링 빈에 등록한다. 이 때, 스프링 부트는 기본으로 커넥션 풀을 제공하는 `HikariDataSource`를 생성한다. 직접 `DataSource`를 스프링 빈으로 등록하게 되면 자동 등록되지 않는다.

- `application.properties`
```properties
# url 속성이 없으면 내장 데이터베이스를 생성하려고 시도한다.
spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.username=sa
spring.datasource.password=
# 커넥션 풀 관련 설정도 할 수 있다.
```


[처음으로](#스프링-db)


## 트랜잭션
DB에서 트랜잭션은 어떠한 작업을 할 때, 데이터 삽입, 수정, 삭제, 조회 등의 기능을 묶어 하나의 작업처럼 안전하게 처리하도록 보장해주는 것을 말한다. 트랜잭션은 `ACID`를 보장해야 한다. `ACID`의 개념은 다음과 같다.

- **원자성 (Atomicity)** : 트랜잭션 내에서 실행한 작업들은 마치 하나의 작업인 것 처럼 모두 성공하거나 모두 실패해야 한다.
- **일관성 (Consistency)** : 모든 트랜잭션은 일관성 있는 데이터베이스 상태를 유지해야 한다. 예를 들어 데이터베이스에서 정한 무결성 제약조건을 항상 만족해야 한다.
- **격리성 (Isolation)** : 동시에 실행되는 트랜잭션들이 서로에게 영향을 미치지 않도록 격리한다. 격리성은 동시성과 관련된 성능 이슈로 인해 트랜잭션 격리 수준을 선택할 수 있다.
- **지속성 (Durability)** : 트랜잭션을 성공적으로 끝내면 그 결과가 항상 기록되어야 한다. 중간에 시스템에 문제가 발생해도 데이터베이스 로그 등을 사용하여 성공한 트랜잭션 내용을 복구해야 한다.

애플리케이션에서 DB 데이터를 통해 어떠한 로직을 수행할 때, 해당 로직은 트랜잭션 안에서 수행되어야 한다. 로직이 성공적으로 처리되면 DB에 반영(`commit`)하고, 로직 수행에 실패하면 로직이 처음부터 수행되지 않은 것 처럼 작업 수행 이전 상태로 되돌려야 한다(`rollback`).

보통 애플리케이션은 클라이언트로부터 요청을 받고 요청에 대한 작업을 위임하는 `Web` 계층, 비즈니스 로직을 담은 `Service` 계층, DB에 접근하는 `Repository`계층이 분리되어 있다. `Repository` 계층은 DB와 관련되어 데이터를 조회하여 객체로 변환하고, `Service` 계층에서는 조회한 데이터를 이용해 매핑된 객체들을 통해 비즈니스 로직을 수행한다. 비즈니스 로직을 성공적으로 수행하였으면 로직을 통해 변경된 데이터를 DB에 `commit`하여 반영하고, 실패하였으면 `rollback`하여 로직 수행 이전 상태로 되돌려야 한다. 
DB에서 데이터를 가져오는 작업은 `Repository`에서 하지만 가져온 데이터들을 통해 비즈니스 로직을 수행하여 가져온 데이터를 사용하는 것은 `Service` 계층에서 발생한다. 따라서 트랜잭션은 `Service` 계층에서 시작하고 종료하는 것이 맞다. `Service` 계층에서 트랜잭션을 시작하고 `Repository` 계층에서 트랜잭션을 이어받아 DB에 필요한 작업을 수행해야 하는 것이다.

애플리케이션에서 DB에 접근하여 작업을 수행할 때, DB 커넥션을 통해 작업을 수행한다. DB는 커넥션을 통해 내부에 세션을 생성한다. 세션은 커넥션마다 하나씩 생성되고 해당 세션에서 트랜잭션이 수행된다. 따라서 `Service` 계층에서 커넥션을 획득하고 해당 커넥션을 통해 트랜잭션을 시작, 트랜잭션이 시작된 커넥션을 파라미터를 통해 `Repository` 계층에 넘겨준다면 트랜잭션을 유지하여 사용할 수 있다.

하지만 이러한 방법으로 트랜잭션을 적용하면 서비스 계층이 트랜잭션 시작과 종료를 위한 `javax.sql.DataSource`, `java.sql.Connection`, `java.sql.SQLException` 등의 JDBC 기술에 의존하게 되고, 트랜잭션 적용을 위한 `try, catch, finally` 구문이 메서드마다 반복되는 문제가 있다.


[처음으로](#스프링-db)


## 스프링의 트랜잭션
[선언적 트랜잭션 관리](#선언적-트랜잭션-관리)
[프로그래밍 방식 트랜잭션 관리](#프로그래밍-방식-트랜잭션-관리)

### 선언적 트랜잭션 관리
스프링은 트랜잭션을 처리하기 위한 AOP 기능을 제공한다. 이를 이용하면 트랜잭션 적용을 위해 서비스 계층이 `javax.sql.DataSource`, `java.sql.Connection` 등의 JDBC 기술에 의존하게 되는 문제와 트랜잭션 적용을 위해 반복적으로 작성했던 `try, catch, finally` 구문을 해결할 수 있다. 트랜잭션과 관련된 로직을 더 이상 작성하지 않아도 되는 것이다.

트랜잭션 적용을 원하는 대상 클래스나 메서드에 `@Transactional` 애노테이션만 붙여주면 스프링 트랜잭션 AOP는 이를 인식하여 트랜잭션 프록시를 적용한다. 이를 선언적 트랜잭션 관리라고 한다. 트랜잭션 AOP가 `@Transactional` 애노테이션이 붙은 클래스를 바탕으로 프록시를 생성하고 프록시에서 트랜잭션 관련 작업을 수행하도록 해준다. 

- 트랜잭션 AOP 프록시 동작 과정
	0. 트랜잭션 AOP가 `@Transactional` 애노테이션을 인식하여 프록시를 적용한다.
	1. 프록시를 호출하면 프록시는 스프링 컨테이너를 통해 빈으로 등록된 트랜잭션 매니저를 획득하고 이를 통해 트랜잭션을 시작한다.
	2. 프록시는 실제 로직을 담은 대상 객체를 호출하여 로직을 수행한다.
	3. 로직에서는 데이터 접근 계층을 호출하여 작업을 수행한다.
	4. 트랜잭션이 모두 완료되면 프록시에서 트랜잭션을 종료한다.

- 트랜잭션 프록시의 예시
```java
// @Transactional // <- 일반적으로 클래스의 모든 public 메서드에 트랜잭션을 적용한다.
public class Service {
	
	@Transactional // 해당 메서드에 트랜잭션을 적용한다.
	public void transactionalMethod() {
		// 로직
	}

	// value, transactionManager 둘 중 하나에 트랜잭션 매니저의 스프링 빈 이름을 입력하면 특정 트랜잭션 매니저를 지정하여 사용할 수 있다. 입력하지 않으면 기본으로 등록된 트랜잭션 매니저를 사용한다.
	@Transactional("트랜잭션 매니저 이름") // 입력한 트랜잭션 매니저 이름을 스프링 빈에서 찾아서 사용한다.
	public void transactionalMethod2() {
		// 로직
	}
}

/*
// 트랜잭션 AOP는 다음과 같은 구조의 프록시를 생성한다.

public class Proxy {
	// 실제 대상 객체를 포함한다.
	private Service target;

	public void transactionalMethod() {
		//트랜잭션을 시작한다.
		TransactionStatus status = transactionManager.getTransaction(...);

		try {
			// 실제 타겟의 메서드를 호출한다.
			target.transactionalMethod();
			// 작업 수행에 성공하면 커밋하여 트랜잭션을 종료한다.
			transactionManager.commit(status);
		} catch (Exception e) {
			// 작업 수행에 실패하면 롤백하여 트랜잭션을 종료한다.
			transactionManager.rollback(status);
			throw new RuntimeException(e);
		}
	}
}
*/
```

프록시 내부에서는 트랜잭션 매니저를 사용하여 트랜잭션을 시작하고 종료한다. 트랜잭션 매니저는 트랜잭션을 추상화한 것으로 스프링이 제공하며, `PlatformTransactionManager`와 이를 구현한 구현체들을 말한다. 트랜잭션 매니저는 `javax.sql.DataSource`, `java.sql.Connection` 등의 JDBC 기술에 의존하지 않고 트랜잭션을 사용할 수 있게 해준다. 

또한 스프링은 서비스 계층에서 시작된 트랜잭션을 깔끔하게 데이터 접근 계층에서 동기화하여 사용할 수 있도록 트랜잭션 동기화 매니저인 `TransactionSynchronizationManager`를 제공한다. 트랜잭션 동기화 매니저는 쓰레드 로컬을 통해 커넥션을 동기화한다.

데이터 접근 계층에서 `Spring Data JPA`의 경우, `JpaRepository`를 상속받게 되는데 `JpaRepository`에는 기본적으로 `@Transactional`이 적용되어 있다. 이와 같이 선언적 트랜잭션이 적용된 서비스 계층에서 선언적 트랜잭션이 적용된 데이터 접근 계층을 호출하면 기본적으로는 서비스 계층의 [트랜잭션이 전파](#스프링-트랜잭션-전파)된다.

#### 트랜잭션 매니저 자동 등록
스프링 부트는 현재 등록된 라이브러리를 보고 적절한 트랜잭션 매니저를 `transactionManager`라는 이름으로 자동으로 스프링 빈에 등록한다. JDBC 기술을 사용하면 `DataSourceTransactionManager`를, JPA를 사용하면 `JpaTranactionManager`를 스프링 빈으로 등록한다. 둘 다 사용하는 경우에는 `JpaTranactionManager`가 `DataSourceTransactionManager`의 기능도 대부분 지원하기 때문에 `JpaTranactionManager`를 등록한다.


### 프로그래밍 방식 트랜잭션 관리
프로그래밍 방식 트랜잭션 관리는 트랜잭션 매니저 또는 트랜잭션 템플릿 등을 사용하여 트랜잭션 관련 코드를 직접 작성하는 것을 말한다. 선언적 트랜잭션 관리가 간편하고 실용적이기 때문에 대부분 선언적 방식을 사용하지만 테스트 시에 프로그래밍 방식 트랜잭션 관리를 사용하기도 한다.

서비스 계층에서 `DataSource`와 `Connection`을 통해 직접 트랜잭션을 시작하고 종료하면 서비스 계층에 해당 JDBC 기술에 대한 의존성이 생기기 때문에 데이터 접근 기술을 바꾸게 되면 변경이 발생한다. 데이터 접근 기술마다 트랜잭션 사용하는 방법이 다르기 때문이다. 또한 파라미터를 통해 서비스 계층에서 시작된 트랜잭션을 데이터 접근 계층으로 전달하려면 메서드를 중복으로 만드는 등의 문제가 있다.

스프링은 위와 같은 문제를 해결하기 위해서 트랜잭션을 추상화한 `PlatformTransactionManager` 인터페이스를 제공한다. 해당 인터페이스와 이를 구현한 구현체들을 트랜잭션 매니저라고 한다. 트랜잭션 매니저를 통해 데이터 접근 기술을 JDBC에서 JPA와 같은 다른 기술로 변경하여도 트랜잭션 관련 코드를 변경하지 않아도 된다. `PlatformTransactionManager`를 사용하는 곳에 `DataSourceTransactionManager`, `JpaTransactionManager`와 같은 구현체만 잘 맞추어 넣어주면 된다.

또한 스프링은 트랜잭션 리소스 동기화 매니저인 `TransactionSynchronizationManager`를 제공하여 쓰레드 로컬을 통해 커넥션을 동기화할 수 있도록 해준다. `PlatformTransactionManager`는 내부에서 트랜잭션 동기화 매니저를 사용하고 트랜잭션 동기화 매니저는 쓰레드 로컬을 사용하기 때문에 파라미터로 커넥션을 전달하지 않아도 커넥션을 동기화 할 수 있다. 

서비스 계층에서 트랜잭션 매니저를 통해 시작된 트랜잭션을 데이터 접근 계층에서 사용하려면 `DataSourceUtils`의 메서드를 사용하면 된다. `DataSourceUtils`는 `TransactionSynchronizationManager`를 편리하게 사용할 수 있게 하는 유틸리티 클래스로 보면 된다. 데이터 접근 기술을 JDBC로 사용하는 경우 이와 같이 코드를 직접 작성하여 사용하게 된다.

- `PlatformTransactionManager` 사용 예시
```java
@Configuration
public class BeanConfig {
	// 트랜잭션 매니저 수동 등록
	@Bean
	public PlatformTransactionManager transactionManager() {
		// JDBC를 사용하는 트랜잭션 매니저를 빈으로 등록하여 사용한다.
		return new DataSourceTransactionManager(dataSource());
		// JPA를 사용하는 트랜잭션 매니저를 빈으로 등록하여 사용한다.
		// return new JpaTransactionManager(dataSource());
	}

	// 데이터소스 수동 등록
	@Bean
	public DataSource dataSource() {
		// DriverManagerDataSource를 빈으로 등록하여 사용한다.
		return new DriverManagerDataSource(URL, ID, PW);
	}
}

public class Service {
	private final PlatformTransactionManager transactionManager;
	private final Repository repository;

	public Service(PlatformTransactionManager transactionManager, Repository repository) {
		// 트랜잭션 매니저를 주입받는다.
		this.transactionManager = transactionManager;
		this.repository = repository;
	}

	public void serviceExampleMethod() throws SQLException {
		// 트랜잭션 시작
		TransactionStatus status = transactionManager.getTransaction(new DefaultTransactionDefinition());

		try {
			// 비즈니스 로직;
			// 트랜잭션 수행 성공. 커밋한다.
			transactionManager.commit(status);
		} catch (Exception e) {
			// 트랜잭션 수행 실패. 롤백한다.

			transactionManager.rollback(status);
			throw new RuntimeException(e);
		}
	}
}

@RequiredArgsConstructor
public class Repository {
	private final DataSource datasource;

	public void repositoryExampleMethod() throws SQLException {
		Connection con = null;
		// ...
		try {
			// 트랜잭션 동기화 사용시 DataSourceUtils를 사용하여 쓰레드 로컬에서 커넥션을 가져오거나 생성할 수 있다.
			con = DataSourceUtils.getConnection(dataSource);
			// 기타 로직.
		} catch (SQLException e) {
			throw e;
		} finally {
			// 사용 리소스 닫기.
			// 트랜잭션 동기화 사용시 DataSourceUtils를 사용하여 커넥션을 반환하도록 한다.
			// 내부에서 con.close()를 호출하여 커넥션을 종료한다. 커넥션 풀의 경우 커넥션 풀에 반환된다.
			DataSourceUtils.releaseConnection(con, dataSource);
		}
	}
}
```
- 트랜잭션 매니저를 통해 서비스 계층에서 `DataSource`와 `Connection`에 대한 의존성을 제거된 것을 확인할 수 있다.


[처음으로](#스프링-db)


## 스프링의 `SQLException` 예외 처리
서비스 계층에서 `java.sql.SQLException`에 대한 의존을 제거하려면 데이터 접근 계층에서 체크 예외인 `SQLException`을 런타임 예외로 전환하여 던지면 된다. 예외를 변환할 때, 기존 예외를 포함하여 변환해야 한다. 기존 예외를 포함하지 않으면 장애 발생 원인이 남지 않아 심각한 문제가 발생할 수 있다.

`SQLException`에는 DB에서 제공하는 `errorCode`가 들어있다. `errorCode`는 어떤 상황에 DB 오류가 발생했는지에 대한 정보를 나타낸다. 이 `errorCode`를 통해 특정 상황에서는 예외를 복구하려고 시도할 수도 있다. `errorCode`에 대한 정보는 DB마다 다르다.

- `SQLException` -> `RuntimeException`
```java
// 런타임 예외를 상속받은 사용자 정의 예외
public class CustomException extends RuntimeException {
	public CustomException() {}

	public CustomException(String message) {
		super(message);
	}

	// Throwable cause를 통해 기존 예외를 받아 기존 예외 정보를 담는다.
	public CustomException(String message, Throwable cause) {
		super(message, cause);
	}

	// Throwable cause를 통해 기존 예외를 받아 기존 예외 정보를 담는다.
	public CustomException(Throwable cause) {
		super(cause);
	}
}

// 사용자 정의 예외를 상속받은 키 중복 예외
public class CustomKeyDuplicatedException extends CustomException {

	// ... 기타 예외 생성자 ...

	// Throwable cause를 통해 기존 예외를 받아 기존 예외 정보를 담는다.
	public CustomKeyDuplicatedException(Throwable cause) {
		super(cause);
	}
}

public class Repository {
	try {
		// ...
	} catch (SQLException e) {
		// h2의 23505 errorCode는 키 중복 오류이다.
		if (e.getErrorCode() == 23505) {
			// 키 중복 오류라면 CustomKeyDuplicatedException로 변환하여 예외를 던진다.
			throw new CustomKeyDuplicatedException(e);
		}
		// SQLException -> CustomException(RuntimeException) 변환
		// 기존 예외를 넘겨 예외의 원인을 담아야 한다.
		throw new CustomException(e);
	} finally {
		// ...
	}
}
```


### 스프링의 예외 처리
스프링은 데이터 접근 계층에 대한 많은 예외를 추상화하여 일관된 예외 계층을 제공한다. 각각의 예외는 특정 기술에 종속적이지 않게 설계되었다. 스프링은 데이터 접근 계층에서 어떤 기술을 사용하든 스프링이 제공하는 예외로 변환해 주는 역할도 제공한다. 따라서 서비스 계층에서도 스프링이 제공하는 예외를 사용하면 된다.

스프링은 DB 마다 다른 오류 코드를 해결하기 위해 `SQLExceptionTranslator`라는 예외 변환기를 제공한다. `SQLExceptionTranslator` 객체를 생성하고 해당 객체의 `translate("설명", SQL, SQLException)`을 호출하면 스프링 데이터 접근 계층의 예외로 변환해서 반환해준다. 예외 변환기는 `SQLException`의 `errorCode`를 `org.springframework.jdbc.support.sql-error-codes.xml`에 대입하여 어떤 스프링 데이터 접근 예외로 변환할지 찾아낸다. `sql-error-codes.xml` 파일에는 여러 DB의 `errorCode`에 대한 매핑 정보가 들어있다.

스프링의 추상화된 예외를 사용하여 서비스 계층에서 특정 기술에 종속적이지 않도록 순수한 서비스 계층을 작성할 수 있고, 스프링의 데이터 접근 계층 예외 변환기를 통해 데이터 접근 기술에 상관없이 `SQLException`을 추상화된 예외로 변환하여 추가 작업이 필요한 경우, 이를 처리할 수 있게 되었다.


[처음으로](#스프링-db)


## @Transactional 옵션
### 사용할 트랜잭션 매니저 지정
`@Transactional` 애노테이션의 `value`, `transactionManager` 중 하나의 옵션에 사용할 트랜잭션 매니저의 스프링 빈 이름을 기입한다. 해당 값을 생략하면 기본으로 등록된 트랜잭션 매니저를 사용한다.

```java
@Transactional("jpaTransactionManaer")

@Transactional("dataSourceTransactionManager")
```

### 특정 예외 롤백 지정, 제외
스프링의 트랜잭션은 기본적으로 언체크 예외인 `RuntimeException`, `Error`와 이들의 하위 예외가 발생하면 트랜잭션을 롤백한다. 하지만 체크 예외인 `Exception`과 그 하위 예외들은 커밋한다.
`@Transactional` 애노테이션의 `rollbackFor` 옵션을 사용하면 추가로 지정한 예외가 발생하면 트랜잭션을 롤백할지 지정할 수 있다.
반대로 `noRollbackFor` 옵션을 사용하면 추가로 지정한 예외가 발생하면 트랜잭션을 롤백하지 않고 커밋한다.

트랜잭션 수행 중에 발생한 비즈니스 예외 상황에 따라 트랜잭션을 커밋할 수도, 롤백할 수도 있다. 상황에 맞추어 해당 옵션을 사용하면 유연하게 처리할 수 있다. ex) 상품 결제 - 잔액 부족 예외 발생 -> 주문 상태 : 대기 처리

```java
// CustomRollbackException 예외가 발생하면 트랜잭션을 롤백한다.
@Transactional(rollbackFor = CustomRollbackException.class)

// CustomCommitException 예외가 발생해도 트랜잭션을 롤백하지 않고 커밋한다.
@Transactional(noRollbackFor = CustomCommitException.class)
```

### 읽기 전용 트랜잭션 설정
트랜잭션은 기본적으로 읽기, 쓰기 모두 가능한 트랜잭션이 생성된다. `@Transactional` 애노테이션의 `readOnly` 옵션을 사용하면 읽기 전용으로 트랜잭션을 생성한다. `readOnly` 옵션은 트랜잭션에 참여하는 경우에는 적용되지 않는다.
`readOnly` 옵션을 사용하면 `JdbcTemplate`의 경우, 읽기 전용 트랜잭션 안에서 변경 기능을 실행하면 예외를 던진다. JPA는 커밋 시점에 변경된 데이터의 내용을 영속성 컨텍스트에 적용하지 않는다.

```java
// 읽기 전용 트랜잭션으로 생성한다. readOnly 속성의 기본값은 false이다.
@Transactional(readOnly = true)
```

### 트랜잭션 전파 설정
[트랜잭션 전파 설명](#스프링-트랜잭션-전파)

`@Transactional` 애노테이션의 `propagation` 옵션을 통해 트랜잭션 전파를 설정할 수 있다. 사용할 수 있는 옵션은 다음과 같다.

- `REQUIRED` : 기존 트랜잭션이 있으면 기존 트랜잭션에 참여한다. 기존 트랜잭션이 없으면 새로 생성한다.
- `REQUIRES_NEW` : 기존 트랜잭션 유무에 상관없이 항상 새로운 트랜잭션을 생성한다.
- `SUPPORT` : 기존 트랜잭션이 있으면 참여하고, 기존 트랜잭션이 없으면 트랜잭션을 지원하지 않는다.
- `NOT_SUPPORT` : 트랜잭션을 지원하지 않는다. 참여도 하지 않는다.
- `MANDATORY` : 기존 트랜잭션에 참여한다. 반드시 기존 트랜잭션이 있어야 하며 기존 트랜잭션이 없으면 예외가 발생한다.
- `NEVER` : 트랜잭션을 허용하지 않는다. 기존 트랜잭션이 있으면 예외가 발생한다.
- `NESTED` : 기존 트랜잭션이 없으면 새로운 트랜잭션을 생성하고, 기존 트랜잭션이 없으면 중첩 트랜잭션을 만든다. 중첩 트랜잭션은 본인은 외부 트랜잭션의 영향을 받지만 외부에 영향을 주지 않는 트랜잭션이다. JPA에서는 중첩 트랜잭션을 사용할 수 없다.

```java
// 기존 트랜잭션에 참여하지 않고, 신규 트랜잭션을 생성한다. propagation의 기본값은 REQUIRED 이다.
@Transactional(propagation = Propagation.REQUIRES_NEW)
```

### 기타
- `isolation` : 트랜잭션 격리 수준을 지정한다. 기본값은 `DEFAULT`로 DB에 설정된 격리 수준을 따른다. 트랜잭션에 참여하는 경우에는 적용되지 않는다.
- `timeout` : 트랜잭션 수행 시간에 대한 타임아웃을 초 단위로 지정한다. 기본값은 트랜잭션 시스템의 타임아웃을 사용한다. 트랜잭션에 참여하는 경우에는 적용되지 않는다.
- `label` : 트랜잭션 에노테이션의 값을 직접 읽어서 특정한 동작을 하고 싶을 때 사용할 수 있다.


[처음으로](#스프링-db)


## 스프링 트랜잭션 전파
트랜잭션이 수행 중에 추가로 다른 트랜잭션을 수행할 때 어떻게 동작할지 결정하는 것을 트랜잭션 전파라고 한다. 트랜잭션 A가 수행중에 트랜잭션 B를 호출하여 수행하게 될 때, 동일한 트랜잭션에서 수행하게 할 지, 분리된 별도의 트랜잭션으로 동작하게 할 지 정하는 것이다.

`@Transactional` 애노테이션의 `propagation` 옵션을 통해 트랜잭션 전파를 설정할 수 있다. 사용할 수 있는 옵션은 다음과 같다.

- `REQUIRED` : 기존 트랜잭션이 있으면 기존 트랜잭션에 참여한다. 기존 트랜잭션이 없으면 새로 생성한다.
- `REQUIRES_NEW` : 기존 트랜잭션 유무에 상관없이 항상 새로운 트랜잭션을 생성한다.
- `SUPPORT` : 기존 트랜잭션이 있으면 참여하고, 기존 트랜잭션이 없으면 트랜잭션을 지원하지 않는다.
- `NOT_SUPPORT` : 트랜잭션을 지원하지 않는다. 참여도 하지 않는다.
- `MANDATORY` : 기존 트랜잭션에 참여한다. 반드시 기존 트랜잭션이 있어야 하며 기존 트랜잭션이 없으면 예외가 발생한다.
- `NEVER` : 트랜잭션을 허용하지 않는다. 기존 트랜잭션이 있으면 예외가 발생한다.
- `NESTED` : 기존 트랜잭션이 없으면 새로운 트랜잭션을 생성하고, 기존 트랜잭션이 없으면 중첩 트랜잭션을 만든다. 중첩 트랜잭션은 본인은 외부 트랜잭션의 영향을 받지만 외부에 영향을 주지 않는 트랜잭션이다. JPA에서는 중첩 트랜잭션을 사용할 수 없다.

```java
// 기존 트랜잭션에 참여하지 않고, 신규 트랜잭션을 생성한다. propagation의 기본값은 REQUIRED 이다.
@Transactional(propagation = Propagation.REQUIRES_NEW)
```

트랜잭션 전파는 크게 두가지로 분류할 수 있다. **(1) 기존 트랜잭션에 참여하는 방법**과 **(2) 기존 트랜잭션에 참여하지 않고 별도의 새로운 트랜잭션을 생성하는 방법**이다. 트랜잭션에 참여하지도, 새로운 트랜잭션을 생성하지도 않는 방법은 예외이다.

### (1) 기존 트랜잭션에 참여하는 방법
`propagation` 속성에 `REQUIRED` 옵션을 사용한다.
기존 트랜잭션에 참여하는 방법은 A 트랜잭션 수행 중에 B 트랜잭션을 추가로 수행할 때, A 트랜잭션의 범위가 B 트랜잭션까지 확장되어 B 트랜잭션이 A 트랜잭션을 그대로 이어받아 수행되는 것을 말한다. 
이 때, 확장된 A 트랜잭션의 범위를 물리 트랜잭션이라 하고, 기존의 트랜잭션 단위를 논리 트랜잭션이라 한다. 논리 트랜잭션은 각각의 작업 처리 결과에 따라 커밋 또는 롤백할 수 있다. 물리 트랜잭션은 각각의 논리 트랜잭션이 모두 커밋되면 커밋하고, 하나의 논리 트랜잭션이라도 롤백한다면 물리 트랜잭션 범위 내의 모든 트랜잭션을 롤백한다.

여기서 물리 트랜잭션의 커밋과 롤백을 결정하는 것은 트랜잭션이 처음 시작된 트랜잭션 A 이다. 각각의 논리 트랜잭션은 자신의 작업을 마치면 트랜잭션 매니저에 커밋 또는 롤백하게 된다. 트랜잭션 매니저는 `isNewTransaction()`를 통해 종료된 논리 트랜잭션이 신규 트랜잭션인지 기존 트랜잭션에 참여한 트랜잭션인지 판단하여 물리 트랜잭션을 관리한다. 
종료된 트랜잭션이 내부 논리 트랜잭션일 때, 해당 트랜잭션이 커밋하였다면 별도의 조치 없이 그 상위 트랜잭션으로 작업이 넘어간다. 하지만 롤백하였다면 트랜잭션 매니저는 물리 트랜잭션에 `rollback-only`를 표시하여 최초 트랜잭션이 종료되면 물리 트랜잭션을 전부 롤백한다.
종료된 트랜잭션이 신규 생성된 외부 트랜잭션일 때, 해당 트랜잭션이 커밋하면 트랜잭션 매니저는 물리 트랜잭션에 `rollback-only`가 마킹되었는지 확인한다. 해당 표시가 없다면 전체 논리 트랜잭션이 모두 커밋된 것으로 보고 물리 트랜잭션을 커밋한다. 신규 트랜잭션이 롤백한다면 물리 트랜잭션을 전부 롤백한다.

1. A 트랜잭션이 생성된다. 트랜잭션 매니저는 해당 트랜잭션을 신규 트랜잭션으로 생성한다.
2. B 트랜잭션이 `REQUIRED` 옵션을 통해 기존 트랜잭션에 참여한다. 트랜잭션 매니저는 B 트랜잭션은 신규 트랜잭션으로 생성하지 않는다.
3. B 트랜잭션이 수행을 종료한다. 트랜잭션 매니저는 B 트랜잭션이 신규 트랜잭션이 아님을 확인하고 다음 작업을 수행한다.
	- 작업을 성공적으로 마치고 `commit`한 경우 : 별도의 조치 없이 다음으로 작업이 넘어간다.
	- 작업에 실패하여 `rollback`한 경우 : 물리 트랜잭션에 `rollback-only`를 표시하고 다음 작업으로 넘어간다.
4. A 트랜잭션이 수행을 종료한다. 트랜잭션 매니저는 A 트랜잭션이 신규 트랜잭션임을 확인하고 물리 트랜잭션에 A 트랜잭션의 결과(`commit` 또는 `rollback`)를 수행한다.
	- A 트랜잭션이 `commit`한 경우 : 물리 트랜잭션을 커밋한다. 이 때, 물리 트랜잭션에 `rollback-only`가 표시되어 있는지 확인하고, 해당 표시가 있다면 `rollback`하고 `UnexpectedRollbackException` 예외를 던진다.
	- A 트랜잭션이 `rollback`한 경우 : 물리 트랜잭션을 `rollback` 한다.

### (2) 기존 트랜잭션에 참여하지 않고 별도의 새로운 트랜잭션을 생성하는 방법
`propagation` 속성에 `REQUIRES_NEW` 옵션을 사용한다.
외부 트랜잭션과 내부 트랜잭션을 완전히 분리하여 각각 별도의 물리 트랜잭션을 사용하는 방법을 말한다. 따라서 커밋과 롤백도 별도로 이루어진다.

트랜잭션 A가 수행중에 트랜잭션 B를 추가로 수행을 시작한다. 트랜잭션 B는 A에 참여하지 않고 새로운 트랜잭션을 생성한다. 이 경우, 각각의 트랜잭션은 별도의 물리 트랜잭션을 가지며 **DB 커넥션을 공유하지 않고 별도의 커넥션을 사용**하게 된다. 이렇게 되면 트랜잭션 A와 B는 서로의 수행 결과에 영향을 미치지 않는다.

`REQUIRES_NEW` 옵션은 HTTP 요청 하나에 2개의 커넥션을 사용하기 때문에 주의해야 한다. `REQUIRES_NEW`를 사용하지 않고 문제를 해결할 수 있다면 그 방법을 사용하는 것이 더 좋다.
예를 들어 트랜잭션 A에서 트랜잭션 B와 트랜잭션 C를 호출하지 않고 별도의 클래스 E를 두고 E -> A -> B, E -> C 와 같은 구조로 변경하여 동시에 여러 커넥션을 사용하지 않게 할 수도 있다.
상황에 따라 어떤 방법이 더 깔끔한지, 성능에 많은 영향을 미치는지 트레이드 오프를 따져보고 더 나은 방법을 사용하도록 한다.

1. A 트랜잭션이 생성된다. 트랜잭션 매니저는 해당 트랜잭션을 신규 트랜잭션으로 생성한다.
2. B 트랜잭션이 `REQUIRES_NEW` 옵션으로 생성된다. 트랜잭션 매니저는 해당 트랜잭션을 신규 트랜잭션으로 생성한다. A와 B는 별도의 물리 트랜잭션을 사용한다.
3. B 트랜잭션이 수행을 종료한다. 트랜잭션 매니저는 해당 트랜잭션이 신규 트랜잭션임을 확인하고 물리 트랜잭션에 B 트랜잭션의 결과(`commit` 또는 `rollback`)를 수행한다.
	- 작업을 성공적으로 마치고 `commit`한 경우 : B 물리 트랜잭션을 커밋한다.
	- 작업에 실패하여 `rollback`한 경우 : 물리 트랜잭션을 `rollback` 한다.
4. A 트랜잭션이 수행을 종료한다. 트랜잭션 매니저는 해당 트랜잭션이 신규 트랜잭션임을 확인하고 물리 트랜잭션에 A 트랜잭션의 결과(`commit` 또는 `rollback`)를 수행한다.
	- 작업을 성공적으로 마치고 `commit`한 경우 : A 물리 트랜잭션을 커밋한다.
	- 작업에 실패하여 `rollback`한 경우 : 물리 트랜잭션을 `rollback` 한다.

### 트랜잭션 전파가 필요한 이유
트랜잭션 A, B, C가 있고 A -> B, A -> C 와 같은 관계로 트랜잭션을 호출한다고 할 때, 특정 상황에서는 B, C를 각각 호출하고 또 다른 상황에서는 A, B, C를 한번에 모두 사용하는 등 여러 상황이 발생할 수 있다. 특정 상황마다 요구사항에 맞게 트랜잭션을 수행하려면 많은 수의 트랜잭션을 만들어야 할 것이다. 이렇게 되면 중복되는 코드가 다수 발생하고, 유지보수도 어려워진다. 이러한 문제를 해결하기 위해 트랜잭션 전파가 필요하다.
트랜잭션 전파를 활용하면 특정 상황에서는 단일 메서드만을 트랜잭션을 사용하여 수행할 수 있고, 또 다른 상황에서는 여러 트랜잭션을 하나의 트랜잭션처럼 묶어서 사용할 수도 있다.

.


[처음으로](#스프링-db)


