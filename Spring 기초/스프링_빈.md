# 스프링 빈
스프링을 통해 객체를 생성하고 관리하면서 의존관계를 연결해주기 위해 스프링 컨테이너를 이용한다. 스프링 컨테이너에 객체를 스프링 빈으로 등록하고 이를 꺼내어 사용하는 것이다. 스프링 컨테이너는 기본적으로 싱글톤 방식으로 동작한다. 스프링 컨테이너에 스프링 빈을 등록하는 방법은 다음과 같은 방법들이 있다.

## 스프링 빈 등록 방법
### 스프링 설정 정보 클래스 작성
```java
@Configuration // 설정 정보 구성.
public class AppConfig {
	@Bean // 스프링 컨테이너에 스프링 빈으로 등록.
	public MemberServie memberServie() {
		return new MemberServiceImpl(memberRepository());
	}

	@Bean 
	public MemberRepository memberRepositry() {
		return new MemberRepositoryImpl();
	}

	@Bean
	public MemberController memberController() {
		return new MemberController(memberService());
	}

	...
}
```

	- 수동으로 직접 스프링 빈으로 등록해주는 방법이다.
	- 등록해야 할 스프링 빈이 많아지면 설정 정보가 커지고, 누락되는 문제가 발생할 수 있다.


### 컴포넌트 스캔 - 자동으로 스프링 빈을 등록
```java
@Configuration
@ComponentScan // @Component 애노테이션이 붙은 클래스를 스캔해서 자동으로 스프링 빈으로 등록.
public class AutoAppConfig {
}

@Component // 컴포넌트 스캔의 대상이 된다.
public class MemberRepositoryImpl implements MemberRepository {}

@Component // 컴포넌트 스캔의 대상이 된다.
public class MemberServiceImpl implements MemberService {
	private final MemberRepository memberRepository;

	@Autowired // 의존관계를 자동으로 주입.
	public MemberServiceImpl(MemberRepository memberRepository) {
		this.memberRepository = memberRepository;
	}
}

@Component // 컴포넌트 스캔의 대상이 된다.
public class MemberController {
	private final MemberService memberService;

	@Autowired // 의존관계를 자동으로 주입.
	public MemberController(MemberService memberService) {
		this.memberService = memberService;
	}
}
```
	- `@ComponentScan` : `@Component` 애노테이션이 붙은 모든 클래스를 스프링 빈으로 등록한다. 스프링 빈의 기본 이름은 클래스명을 사용하는데 맨 앞글자만 소문자로 변형하여 사용한다.
	- `@Component` : 컴포넌트 스캔의 대상으로 지정한다.
	- `@Autowired` : 스프링 컨테이너가 자동으로 해당 스프링 빈을 찾아서 주입한다. 기본 조회 전략은 타입이 같은 빈을 찾아서 주입한다.

	- `@ComponentScan`은 해당 클래스가 위치한 패키지를 포함하여 모든 하위 패키지를 스캔한다. 
		- `@ComponentScan(basePackages="패키지경로")`를 통하여 탐색 시작 위치를 지정할 수도 있다.
	- 스프링 부트를 사용하면 스프링 부트의 대표 시작 정보인`@SpringBootApplication`을 프로젝트 시작 위치에 두는 것이 관례인데, 이 안에 `@ComponentScan`이 들어있다.

#### 컴포넌트 스캔 필터
- `@ComponentScan(includeFilters = @Filter(type = FilterType.ANNOTATION, classes = 포함할 클래스명.class), excludeFilters = @Filter(type = FilterType.ANNOTATION, classes = 제외할 클래스명.class))`
	- 이 처럼 사용하여 특정 애노테이션이 붙으면 스프링 빈으로 등록하거나 등록하지 않도록 설정할 수 있다.


---
## 의존관계 자동 주입
의존관계 주입 방법은 크게 4가지 방법이 있다.

- 생성자 주입
- 수정자 주입(setter)
- 필드 주입
- 일반 메서드 주입

### 생성자 주입 
생성자를 통하여 의존 관계를 주입받는 방법으로 생성자 호출 시점에 딱 1번만 호출되는 것을 보장한다. **불변, 필수** 의존 관계에 사용한다.
```java
@Component
public class ExampleServiceImpl implements ExampleServie {
	private final ExampleRepository exampleRepository;

	// @Autowired // 생성자가 1개면 생략해도 자동 주입 가능. 스프링 빈에만 해당한다.
	public ExampleServiceImpl(ExampleRepository exampleRepository) {
		this.exampleRepository = exampleRepository;
	}
}
```


### 수정자 주입
필드값을 변경하는 수정자를 통하여 의존 관계를 주입한다. **선택, 변경** 가능성이 있는 의존 관계에 사용하면 된다.
```java
@Component
public class ExampleServiceImpl implements ExampleServie {
	private ExampleRepository exampleRepository;

	@Autowired // 주입할 대상이 없으면 기본적으로 오류가 발생한다. 주입할 대상이 없어도 동작하게 하려면 (required = false)로 지정해야 한다.
	public void setExampleRepository(ExampleRepository exampleRepository) {
		this.exampleRepository = exampleRepository;
	}
}
```


### 필드 주입
생성자 없이 필드에 바로 `@Autowired` 애노테이션을 붙인다. 코드가 간결하지만 외부 변경이 불가능하여 테스트하기 힘들다는 단점이 있으며 DI 프레임워크가 없으면 아무것도 할 수 없는 문제가 있다. 테스트 코드 등에는 사용해도 무방하나 App의 실제 코드에는 사용하지 않아야 한다.

### 일반 메서드 주입
일반 메서드를 통하여 주입받는다. 잘 사용하지 않아서 따로 설명하지 않는다.



### 스프링 빈 옵션 처리
자동 주입 대상을 옵션으로 처리하는 방법은 3가지가 있다.
```java
@Autowired(required = false)
public void setXXX(ExamClass examClass) {
	// 자동으로 주입할 대상이 없으면 호출하지 않는다.
}

@Autowired
public void setXXX(@Nullable ExamClass examClass) {
	// 대상이 없으면 Null을 입력한다.
}

@Autowired
public void setXXX(Optional<ExamClass> examClass) {
	// 대상이 없으면 Optional.empty를 입력한다.
}
```



### 의존관계 자동 주입시, 조회된 빈이 2개 이상일 때
3가지 해결 방법이 있다.
- `@Autowired` 필드명 매칭
	- `@Autowired private ExampleService exampleServiceImpl`
	- 기본으로 타입 매칭을 시도하고, 결과가 2개 이상이면 필드명, 파라미터명으로 빈 이름 매칭한다.
- `@Qualifier` 애노테이션 사용하여 추가 구분자를 붙여 매칭
	- 등록시 `@Qualifier("구분할 이름")`
	- 주입시 `@Autowired public 생성자(@Qualifier("사용할 구분 이름") ExampleService exampleService)`
	- 못찾으면 해당 구분 이름으로 등록된 스프링 빈을 찾는다.
- `@Primary` 애노테이션 사용
	- `@Component @Primary`
	- 여러 빈이 매칭되면 `@Primary` 애노테이션이 붙은 빈이 우선권을 가진다.


### 조회한 빈이 모두 필요할 때
`Map`과 `List`를 이용하면 된다.
- `private final Map<String, 주입받을 객체 타입> exampleMap;`
- `private final List<주입받을 객체 타입> exampleList;`
- 이를 이용하면 모든 `Map` 또는 `List` 형태로 `주입받을 객체 타입` 객체들을 주입받을 수 있다.
- 해당하는 타입의 스프링 빈이 없으면 빈 컬렉션이나 Map을 주입한다.



## 스프링 빈 등록 및 의존관계 주입 정리
애플리케이션 로직은 크게 2가지로 나눌 수 있다.
- 업무 로직 : 일반적으로 비즈니스 요구사항을 개발할 때 추가되거나 변경되는 빈들로 구성된다. 컨트롤러, 서비스, 리포지토리 등.
	- 업무 로직은 숫자도 많고 어느정도 유사한 패턴이 있다. 보통 문제가 발생해도 어떤 곳에서 문제가 발생했는지 파악하기 쉽기 때문에 자동 기능을 사용하는 것이 좋다.
- 기술 지원 로직 : 기술적인 문제나 공통 관심사(AOP)를 처리할 때 주로 사용된다. DB Connection, 공통 Log 처리 등 업무 로직을 지원하기 위한 하부 기술이나 공통 기술들을 말한다.
	- 기술 지원 로직은 업무 로직과 비교하여 수가 매우 적다. 또한 App 전반에 걸쳐 광범위하게 영향을 미친다. 기술 지원 로직은 문제가 발생하면 명확한 위치를 찾기 힘든 경우가 많다. 따라서 기술 지원 로직들은 가급적 수동 빈 등록을 사용하여 명확하게 드러내는 것이 유지보수에 좋다.

또한 비즈니스 로직 중 다형성을 활용할 때, 조회한 빈이 모두 필요할 때에 **한눈에 파악하기 쉽도록** 별도 설정 정보를 만든 후 수동으로 빈을 등록하거나, 특정 패키지에 묶어서 자동 빈 등록을 사용하는 것이 좋다.


- 기본적으로 자동 기능을 사용.
- 업무 로직에 해당하는 객체는 자동등록 사용.
- 기술 지원 객체는 수동 등록 사용.
- 다형성을 활용하는 비즈니스 로직은 수동 등록 or 특정 패키지에 묶기.


---
## 빈 생명주기 콜백
스프링 빈의 이벤트 라이프 사이클은 다음과 같다.
스프링 컨테이너 생성 -> 스프링 빈 생성 -> 의존관계 주입 -> 초기화 콜백 -> 사용 -> 소멸 전 콜백 -> 스프링 종료

초기화 콜백은 빈이 생성되고, 빈의 의존관계 주입이 완료된 후 호출된다. 소멸 전 콜백은 빈이 소멸되기 직전에 호출된다. 

스프링은 크게 3가지 방법으로 빈 생명주기 콜백을 지원한다.
- 인터페이스(initializingBean, DisposableBean) 구현
	- 스프링 전용 인터페이스.
	- 코드를 고칠 수 없은 외부 라이브러리에 적용할 수 없다.
	- 거의 사용하지 않음.
- `@Bean(initMethod = "초기화메서드이름", destroyMethod = "종료메서드지정")`
	- 설정 정보에 초기화 메서드, 종료 메서드 지정
	- 스프링 빈이 스프링 코드에 의존하지 않는다.
	- 설정 정보를 사용하기 때문에 외부 라이브러리에도 적용 가능.
	- `close`, `shutdown` <- 추론 기능을 이용하여 종료시에 해당 이름의 메서드를 지동으로 추론하여 호출해준다.
- `@PostConstruct`, `@PreDestroy` 애노테이션
	- 초기화, 종료 메서드에 각각 애노테이션을 붙여주면 된다.
	- JSR-250이라는 자바 표준 기술이다. 다른 컨테이너에서도 동작한다.
	- 외부 라이브러리에는 적용할 수 없다. 기본적으로 이를 사용하고 필요시 `@Bean`의 기능을 사용.


## 빈 스코프
스코프는 빈이 존재할 수 있는 범위를 말한다. 스프링은 다음과 같은 다양한 스코프를 지원한다.
- 싱글톤 : 기본 스코프로 스프링 컨테이너의 시작과 종료까지 유지된다.
- 프로토타입 : 스프링 컨테이너는 빈의 생성과 의존관계 주입까지만 관여하고 더는 관리하지 않는다.
- 웹 관련
	- request : 웹 요청이 들어오고 나갈 때 까지 유지된다.
	- session : 웹 세션이 생성되고 종료될 때 까지 유지된다.
	- application : 웹의 서블릿 컨텍스트와 같은 범위로 유지된다.

### 싱글톤

### 프로토타입
프로토타입 스코프를 스프링 컨테이너에 조회하면 스프링 컨테이너는 **항상 새로운 인스턴스를 생성해서 반환**한다. 스프링 컨테이너는 빈 요청 시점에 빈을 생성하고 필요한 의존관계를 주입한다. 이후 생성한 프로토타입 빈을 클라이언트에 반환하고 더 이상 관리하지 않는다. **스프링 컨테이너는 빈을 생성하고, 의존관계를 주입, 초기화까지만 처리하고 이 후, 종료 등은 처리하지 않는다.** 프로토타입 빈을 관리할 책임은 이를 반환받은 클라이언트에 있는 것이다. 클라이언트가 직접 종료 메서드에 대한 호출을 해야한다.

### 프로토타입 빈 요청시 주의
**매번 사용할 때 마다 의존관계 주입이 완료된 새로운 객체가 필요할 때 프로토타입 빈을 사용한다.**
이 때, 프로토타입 빈을 스프링 컨테이너에 직접요청하는 것은 문제가 되지 않는다. 스프링 컨테이너가 요청마다 프로토타입 빈을 새로 생성해서 반환하기 때문이다.

하지만 싱글톤 빈이 의존관계 주입을 통해 프로토타입 빈을 주입받아 사용하는 경우에는 주의해야 한다. 
싱글톤 빈 생성시 의존관계 주입을 통하여 프로토타입 빈을 주입받고 싱글톤 빈은 내부 필드로 프로토타입 빈을 보관한다. 싱글톤 빈에서 프로토타입 빈을 꺼내어 사용하면 요청마다 새로운 프로토타입 빈을 생성하는 것이 아니라 이미 생성된 프로토타입 빈을 사용하는 것이다. 프로토타입 빈이 싱글톤 빈과 함께 계속 유지되는 것이다.

싱글톤 빈과 함께 프로토타입 빈을 사용할 때, 항상 새로운 프로토타입 빈을 생성하는 방법은 다음과 같은 방법이 있다.
- 싱글톤 빈에서 프로토타입 빈 사용시 마다 스프링 컨테이너에 새로 요청한다.
```java
public class SingletonBean {
	@Autowired
	private ApplicationContext ac;
	
	public PrototypeBean testMethod() {
		PrototypeBean prototypeBean = ac.getBean(PrototypeBean.class);
	
		// ...	
	
		return prototypeBean;
	}
}
```

- 의존관계 주입(DL)이 아닌 의존관계 조회(DL : Dependency Lookup)를 통해 지정한 프로토타입 빈을 컨테이너에서 대신 찾아주도록 한다.
	- `ObjectFactory`
	- `ObjectProvider` <- `ObjectFactory`에 편의 기능 추가
	- `ObjectProvider`의 `getObject()`를 호출하면 내부에서 스프링 컨테이너를 통해 해당 빈을 찾아서 반환한다.
```java
public class SingletonBean {
	@Autowired
	private ObjectProvider<PrototypeBean> prototypeBeanProvider;
	
	public PrototypeBean testMethod() {
		PrototypeBean prototypeBean = prototypeBeanProvider.getObject();
	
		// ...	
	
		return prototypeBean;
	}
}
```

- JSR-330 Provider 사용
	- JSR-330 자바 표준을 사용하는 방법이다.
	- gradle에 `javax.inject:javax.inject:1` 추가
```java
public class SingletonBean {
	@Autowired
	private Provider<PrototypeBean> provider;
	
	public PrototypeBean testMethod() {
		PrototypeBean prototypeBean = provider.get();
	
		// ...	
	
		return prototypeBean;
	}
}
```



### 웹 스코프
웹 스코프는 웹 환경에서만 동작하고 종료시점까지 관리한다. 웹 스코프의 종류에는 `request`, `session`, `application`, `websocket`이 있다.
- `request` : HTTP 요청 하나가 들어오고 나갈 때 까지 유지된다. HTTP 요청마다 별도의 빈 인스턴스가 생성, 관리된다.
- `session` : HTTP Session과 동일한 생명주기를 가진다.
- `application` : 서블릿 컨텍스트와 동일한 생명주기를 가진다.
- `websocket` : 웹 소켓과 동일한 생명주기를 가진다.

웹 요청 등의 시점에 해당 스코프 빈이 생성 및 동작되기 때문에 스프링 애플리케이션 실행 시점에 빈의 생성 및 주입이 안된다. 생성 및 주입 시점을 미뤄야 한다. 가장 간단한 방법은 Provider를 이용하는 것이다.
다른 방법은 프록시를 이용하는 것이다. CGLIB 이라는 라이브러리를 통하여 해당 클래스를 상속받은 가짜 프록시 객체를 만들어 주입한다. 다형성을 이용한 프록시 객체는 클라이언트 입장에서 원본과 동일하게 사용한다. 프록시 객체는 요청이 오면 그 때 내부에서 진짜 빈을 요청하는 위임 로직이 들어있다. 이를 통하여 객체의 조회를 필요한 시점까지 지연처리 할 수 있다.

#### 프록시 사용
```java
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class WebScopeBean {}
```









#스프링 기초/스프링 빈#
#스프링 기초/컴포넌트 스캔#
#스프링 기초/의존관계 자동 주입#
#스프링 기초/빈 생명주기#
#스프링 기초/빈 스코프#

---
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.