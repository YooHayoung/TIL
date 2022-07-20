# 스프링 AOP 적용 방법
[1. 스프링 AOP 적용](#스프링-aop-적용)

  - [1.1. 어드바이스 종류](#어드바이스-종류)
  
  - [1.2. JoinPoint](#joinpoint)

  - [1.3. 포인트컷 적용](#포인트컷-적용) 

  - [1.4. `Advice` 적용 순서 지정](#advice-적용-순서-지정)

[2. Pointcut 표현식](#pointcut-표현식)




## 스프링 AOP 적용
`@Asepct` 애노테이션을 사용하여 스프링 AOP를 구현할 수 있다.
스프링 AOP로 사용하기를 원하는 클래스에 `@Aspect` 애노테이션을 붙이면 스프링 AOP는 이를 인식하여 내부의 `@Pointcut`, `@Around` 등의 애노테이션을 보고 `Advisor`를 생성, 이를 기반으로 스프링 AOP가 적용된 프록시를 생성하여 빈으로 등록한다. 이 과정은 스프링 부트를 사용하면 자동으로 등록되는 빈 후처리기(자동 프록시 생성기)인 `AnnotationAwareAspectJAutoProxyCreator`가 해준다.

`Advisor`를 구현하려면 `Advice` 종류 선택, `Pointcut` 적용, `Advice` 기능 구현의 과정이 모두 이루어져야 한다. `Advice` 기능 구현은 `Advice` 관련 애노테이션이 붙은 메서드를 구현하면 된다.


### 어드바이스 종류
사용할 수 있는 `Advice`는 다음과 같은 것들이 있다.

- `@Around` : 메서드 호출 전후에 수행된다. 조인 포인트 실행 여부를 선택할 수 있고, 반환 값 변환, 예외 변환 등이 가능하다. `joinPoint.proceed()`를 통해 조인 포인트 실행 여부를 선택할 수 있고 `joinPoint.proceed(args[])`를 통해 전달값을 변환할 수도 있다. 이 외에 반환값 변환, 예외 변환 등이 가능하다.
- `@Before` : 조인 포인트 실행 이전에 실행되며 메서드 종료시 다음 타겟이 자동으로 호출된다. 예외가 발생하면 다음 코드를 호출하지 않는다.
- `@AfterReturning` : 조인 포인트가 정상 완료된 후에 실행된다. `returning` 속성에 어드바이스 메서드의 매개변수 이름을 입력하면 해당 타입의 값을 반환하는 메서드만 대상으로 실행한다. 이때, 매개변수의 이름과 `returning` 속성에 입력한 값이 일치해야 하며, 부모 타입을 지정한 경우, 모든 자식타입도 인정된다. 반환되는 객체를 변경할 수는 없으나 조작(사용)할 수는 있다.
- `@AfterThrowing` : 메서드가 예외를 던지는 경우에 실행된다. 예외를 매개변수로 받으며 `throwing` 속성에 어드바이스 메서드의 예외 매개변수 이름을 입력하면 해당 타입의 예외를 대상으로 실행된다.
- `@After` : `try-catch-finally`의 `finally`와 같다. 조인 포인트가 종료되면 결과에 관계없이 실행된다. 일반적으로 사용한 리소스를 해제하는데 사용할 수 있다.

동일한 `@Aspect` 안에서 동일한 조인포인트의 어드바이스는 `@Around` -> `@Before` -> `target` 수행 -> `@After` -> `@AfterReturning` or `@AfterThrowing` -> `@Around` 순으로 적용된다.


### JoinPoint
`JoinPoint`는 `Advice`를 적용할 위치를 말한다. 메서드 실행, 생성자 호출, 필드값 접근, static 메서드 접근 등 프로그램 실행 중 지점을 말한다. 이는 추상적인 개념으로 AOP를 적용할 수 있는 모든 지점을 말한다. 스프링 AOP는 프록시 방식을 사용하기 때문에 `Join point`는 항상 메소드 실행 지점으로 제한된다.

`JoinPoint`는 인터페이스이다. 모든 어드바이스는 `org.aspectj.lang.JoinPoint`를 첫번째 파라미터에 사용할 수 있다. 이는 생략이 가능하다. `JoinPoint` 인터페이스의 주요 기능은 다음과 같다.

- `getArgs()` : 메서드 인수를 반환한다.
- `getThis()` : 프록시 객체를 반환한다.
- `getTarget()` : 대상 객체를 반환한다.
- `getSignature()` : 조언되는 메서드에 대한 설명을 반환한다.
- `toString()` : 조언되는 방법에 대한 유용한 설명을 인쇄한다.

`@Around`는 `ProceedingJoinPoint`를 사용해야 한다. 이는 `JoinPoint`의 하위 타입이다. `ProceedingJoinPoin` 인터페이스의 주요 기능으로는 `proceed()`가 있다. `proceed()`는 다음 `Advice`가 있으면 이를 호출하고, 없다면 `target`을 호출한다. 

추가로 호출시 전달한 매개변수를 파라미터를 통해서 전달 받을 수 있다.


### 포인트컷 적용
구현한 `Advice`에 `Pointcut`을 적용하려면 다음과 같은 방법들을 이용할 수 있다. `Pointcut`을 정의할 때에는 `Pointcut`을 편리하게 표현하기 위한 특별한 표현식인 AspectJ 포인트컷 표현식을 사용할 수 있다.

#### `Advice` 애노테이션의 `value` 속성에 포인트컷 표현식을 입력한다.
`Advice` 애노테이션의 `value` 속성에 AspectJ 포인트컷 표현식을 사용하여 `Pointcut`으로 사용할 수 있다.

```java
@Aspect
public class CustomAspect {
	// com.exam.hello 패키지와 그 하위의 모든 메서드들을 대상으로 하는 Pointcut을 정의하고 사용한다.
	// @AfterReturning(value="execution(* com.exam.hello..*(..))") // <- 이와 같이 사용 가능.
	@Around("execution(* com.exam.hello..*(..))")
	public Object customAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
		// 추가 기능 로직 작성
		return joinPoint.proceed(); // 다음 Advice나 메서드 호출
	}
}
```

#### `@Pointcut` 애노테이션을 사용하여 `Pointcut`을 별도로 분리하고 `Advice` 애노테이션에 이를 지정하여 사용한다.
`@Pointcut` 애노테이션을 사용하여 `Pointcut`을 분리할 수 있다. 분리한 `Pointcut`을 조합하여 재사용할 수도 있다. 이렇게 별도로 분리한 `Pointcut`은 `Pointcut`이 위치한 같은 클래스 안에서 사용하면 `Pointcut`의 시그니처 이름만을 입력해도 되지만, 다른 클래스에서 사용하면 패키지명을 포함한 클래스 이름과 포인트컷 시그니처를 모두 지정하여 사용해야 한다.

- 같은 클래스에서 `Pointcut`을 분리하여 사용하거나, 분리한 `Pointcut`을 조합하여 사용할 수 있다.
```java
// *** 포인트컷을 분리하여 사용할 수 있다. ***
// *** 같은 클래스에서 사용하면 포인트컷 시그니처만 입력해도 된다. ***
@Aspect
public class CustomAspect1 {
	@Pointcut("execution(* com.exam.hello..*(..))") // 포인트컷 표현식
	private void customPointcut() {} // 포인트컷 시그니처

	// 같은 클래스에서 사용하면 포인트컷 시그니처만 입력해도 된다.
	@Around("customPointcut()")
	public Object customAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
		// 추가 기능 로직 작성
		return joinPoint.proceed();
	}
}

// *** 분리한 포인트컷을 조합하여 재사용 할 수 있다. ***
// 같은 클래스에서 사용하면 포인트컷 시그니처만 입력해도 된다.
@Aspect
public class CustomAspect2 {
	@Pointcut("execution(* com.exam.hello..*(..))") // 포인트컷 표현식
	private void customPointcut1() {} // 포인트컷 시그니처

	@Pointcut("execution(* com.exam.world..*(..))") // 포인트컷 표현식
	private void customPointcut2() {} // 포인트컷 시그니처

	// *** 분리한 포인트컷을 조합하여 재사용할 수 있다. ***
	@Pointcut("customPointcut1() && customPointcut2()")
	private void customPointcut3() {} // 포인트컷 시그니처

	// 분리한 포인트컷을 조합하여 재사용할 수 있다.
	// 같은 클래스에서 사용하면 포인트컷 시그니처만 입력해도 된다.
	@Around("customPointcut3()")
	public Object customAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
		// 추가 기능 로직 작성
		return joinPoint.proceed();
	}
}
```

- 외부 클래스에 `Pointcut`을 모아두고 사용할 수 있다. 외부 클래스의 `Pointcut`을 사용할 때에는 패키지명을 포함한 클래스 이름과 포인트컷 시그니처를 모두 지정하여 사용할 수 있다.
```java
// Pointcut을 별도 외부 클래스에 모아둔다.
public class Pointcuts {
	@Pointcut("execution(* com.exam.hello..*(..))") // 포인트컷 표현식
	public void customPointcut1() {} // 포인트컷 시그니처

	@Pointcut("execution(* com.exam.world..*(..))") // 포인트컷 표현식
	public void customPointcut2() {} // 포인트컷 시그니처

	// *** 분리한 포인트컷을 조합하여 재사용할 수 있다. ***
	@Pointcut("customPointcut1() && customPointcut2()")
	public void customPointcut3() {} // 포인트컷 시그니처
}

// 외부 클래스의 Pointcut을 사용할 수 있다.
// 이를 사용할 때에는 패키지명을 포함한 클래스 이름과 포인트컷 시그니처를 모두 지정하여 사용할 수 있다.
@Aspect
public class CustomAspect {
	// 패키지명을 포함한 클래스 이름과 포인트컷 시그니처를 모두 지정하여 외부 클래스의 포인트컷을 사용한다.
	@Around("com.exam.config.Pointcuts.customPointcut3()")
	public Object customAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
		// 추가 기능 로직 작성
		return joinPoint.proceed();
	}
}
```


### `Advice` 적용 순서 지정
`Advice`는 기본적으로 순서를 보장하지 않는다. 순서를 지정하려면 `@Aspect` 단위로 `org.springframework.core.annotation.@Order` 애노테이션을 통해 순서를 지정할 수 있다. 하나의 `@Aspect`에 여러 `Advice`가 있으면 순서를 보장할 수 없기 때문에 별도의 `@Aspect` 클래스로 분리하여 지정해야 한다. `@Order()`에 지정된 값이 작을수록 먼저 실행된다.

```java
// @Order를 통해 순서를 지정하기 위해 Advice를 @Aspect 클래스 단위로 분리한다.
public class CustomAspectOrder {

	@Aspect
	@Order(1) // 값이 작을수록 먼저 실행된다.
	public static class FirstAspect {
		@Around("com.exam.config.Pointcuts.customPointcut2()")
		public Object customAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
			// 추가 기능 로직 작성
			return joinPoint.proceed();
		}
	}

	@Aspect
	@Order(2) // 값이 작을수록 먼저 실행된다.
	public static class SecondAspect {
		@Around("com.exam.config.Pointcuts.customPointcut3()")
		public Object customAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
			// 추가 기능 로직 작성
			return joinPoint.proceed();
		}
	}
}
```



## Pointcut 표현식
### Pointcut 지시자
포인트컷 표현식은 포인트컷 지시자(Pointcut Designator : PCD)로 시작한다. 다음과 같은 포인트컷 지시자들이 있다.

- `execution` : 메서드 실행 조인 포인트를 매칭한다.
- `within` : 특정 타입 내의 조인 포인트를 매칭한다.
- `args` : 조인 포인트의 파라미터가 주어진 타입의 인스턴스일 때 매칭된다. 단독으로 사용하면 안된다.
- `this` : 스프링 빈 객체(스프링 AOP 프록시)를 대상으로 하는 조인 포인트를 매칭한다.
- `target` : Target 객체(스프링 AOP 프록시가 가르키는 실제 대상)를 대상으로 하는 조인 포인트를 매칭한다.
- `@target` : `@target(패키지명.애노테이션클래스명)`으로 대상 애노테이션을 지정하여 해당 애노테이션이 붙은 인스턴스의 모든 메서드를 조인 포인트로 적용한다. 단독으로 사용하면 안된다.
- `@within` : `@within(패키지명.애노테이션클래스명)`으로 대상 애노테이션을 지정하여 해당 애노테이션이 붙은 해당 타입 내에 있는 메서드만 조인 포인트로 적용한다.
- `@annotation` : `@annotation(패키지명.애노테이션클래스명)`으로 대상 애노테이션을 지정하여 해당 애노테이션이 붙은 메서드만이 매칭된다.
- `@args` : `@args(패키지명.애노테이션명)`으로 대상 애노테이션을 지정하여 전달된 실제 인수의 런타임 타입이 해당 애노테이션을 갖는 조인 포인트를 매칭한다. 단독으로 사용하면 안된다.
- `bean` : 스프링 전용 포인트컷 지시자, 빈의 이름으로 포인트컷을 지정한다.

포인트컷 표현식에서 `*`은 어떠한 값도 상관 없다는 뜻이고, `..`은 파라미터의 타입과 수가 상관없다는 뜻이다. 패키지에서 `..`은 해당 위치의 패키지와 그 하위 패키지도 포함한다는 뜻이다.

#### `execution`
`execution` 지시자는 메서드의 실행 조인 포인트를 매칭한다. `execution` 지시자는 다음과 같은 형태로 입력해야 한다.

- `“execution(접근제어자(생략가능) 반환타입 선언타입(패키지명 포함).메서드이름(파라미터타입) 예외(생략가능))”`

다음과 같이 메서드 명과 파라미터 수, 타입까지 정확하게 일치하게 작성할 수도 있고, 포인트컷 표현식의 패턴을 사용하여 작성할 수도 있다. 이때, 타입을 지정하면 해당 타입의 자식 타입은 모두 매칭된다. 단, 부모 타입에서 선언한 메서드가 자식 타입에 있어야 매칭된다.

- `"execution(String com.exam.hello.CustomService.methodName(String))"`
	- 패키지명, 메서드 이름, 파라미터 수와 타입, 메서드 반환 타입이 모두 일치하는 메서드만 매칭

- 반환 타입
	- `"execution(* com.exam.hello.CustomService.methodName(String))"`
		- 반환 타입에 `*`를 사용하여 어떠한 반환타입도 상관없이 매칭할 수 있다.

- 메서드 이름
	- `"execution(* com.exam.hello.CustomService.methoName(..))"`
		- 메서드 이름이 `methodName`과 일치해야 매칭된다.
	- `"execution(* com.exam.hello.CustomService.*tho*(..))"`
		- 메서드 이름 앞뒤에 `*`을 사용하여 매칭할 수 있다.
		- 메서드 이름 중간에 `tho`가 포함되어 있으면 매칭된다.
	- `"execution(* com.exam.hello.CustomService.*(..))"`
		- 메서드 이름에 `*`를 사용하여 매칭할 수 있다. 
		- 메서드 이름에 상관없이 모든 메서드가 매칭된다.

- 선언 타입
	- `"execution(* com.exam.hello.*.*(..))"`
	- 선언 타입에 `*`를 사용하여 매칭할 수 있다.
	- `com.exam.hello`의 패키지의 모든 타입의 모든 메서드는 모두 매칭된다.

- 패키지명
	- `"execution(* com.exam..*.*(..))"`
		- 패키지에서 `..`을 사용하면 해당 패키지와 그 하위 패키지도 포함한다는 뜻이다.  
		- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 모든 메서드가 매칭된다.
	- `"execution(* com.exam.*.*(..))"`
		- 패키지에서 `.`은 해당 위치의 패키지만을 의미한다. 하위 패키지는 포함하지 않는다.
		- 하위 패키지는 포함하지 않기 때문에 `com.exam.hello` 패키지 등의 그 하위에는 적용되지 않는다. `com.exam` 패키지에 존재하는 타입과 메서드만이 매칭된다. 

- 파라미터
	- `"execution(* com.exam..*.*(String))"`
		- `String` 타입의 파라미터 하나만 가진다면 매칭된다.
	- `"execution(* com.exam..*.*())"`
		- 메서드에 파라미터가 없다면 매칭된다.
	- `"execution(* com.exam..*.*(*))"`
		- 메서드에 어떤 타입이든 파라미터 하나만 가진다면 매칭된다.
	- `"execution(* com.exam..*.*(..))"`
		- 메서드의 파라미터 개수, 타입 등 상관없이 모두 매칭된다.
	- `"execution(* com.exam..*.*(String, ..))"`
		- 메서드의 파라미터가 `String` 타입으로 시작하고, 이후에는 상관없이 매칭된다.


#### `within`
`within` 지시자는 특정 타입 내의 조인 포인트에 대한 매칭을 제한한다. 타입이 매칭되면 해당 타입 내의 조인 포인트들이 자동으로 매칭된다. `execution`에서 타입 부분만 사용하는 것과 동일하지만 부모 타입(인터페이스 등)을 지정하면 안된다. 타입이 정확히 맞아야만 매칭된다.
- `"within(com.exam.hello.CustomService)"`
	- `com.exam.hello` 패키지의 `CustomService` 타입의 모든 메서드가 매칭된다.
- `"within(com.exam.hello.*Serv*)"`
	- `com.exam.hello` 패키지의 타입명 중간에 `Serv`가 포함되어 있으면 해당 타입의 모든 메서드가 매칭된다.
- `"within(com.exam.hello.*)"`
	- `com.exam.hello` 패키지의 모든 타입의 모든 메서드가 매칭된다.
- `"within(com.exam..*)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 모든 메서드가 매칭된다.


#### `args`
`args` 지시자는 조인 포인트의 파라미터가 주어진 타입의 인스턴스일 때 매칭된다. 기본적인 문법은 `execution`의 파라미터 부분과 같다. `execution`과의 차이점으로는 `execution`은 클래스에 선언된 정보를 기반으로 판단하기 때문에 파라미터 타입이 정확하게 일치해야 하지만, `args`는 실제 전달된 파라미터 객체 인스턴스를 보고 동적으로 판단하기 때문에 부모 타입이 허용된다. 
- `"args(String)"`
	- `"execution(* *(String))"`과 같다.
- `"args(..)"`
	- `"execution(* *(..))"`과 같다.
- `"args(Object)"`
	- `args`는 부모 타입을 허용하기 때문에 `Object`를 상속받은 객체가 파라미터로 넘어와도 매칭이 된다.
	- `“execution(* *(Object))”`는 `Object`타입이 아닌, 그 자식이 파라미터로 넘어오면 매칭이 안된다.
- 매개변수를 전달할 수 있다.
	- `@Around("args(arg,..)") public void methodName(String arg)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"args(arg,..)"` -> `"args(String,..)"`

> `args`는 실제 객체 인스턴스가 생성되고 실행될 때 어드바이스 적용 여부를 확인할 수 있다. 이를 단독으로 사용하게 되면 스프링은 모든 빈에 AOP를 적용하려고 시도하기 때문에 오류가 발생할 수 있다. 따라서 최대한 프록시 적용 대상을 축소하는 표현식과 함께 사용해야 한다.  


#### `this`
`this` 지시자는 스프링 빈으로 등록된 `Proxy` 객체를 대상으로 하는 조인 포인트가 매칭된다. 적용 타입 하나를 정확하게 지정해야 한다.
- `"execution(* com.exam.hello..*.*(..)) && this(com.exam.hello.CustomService)"`
	- `com.exam.hello` 패키지와 그 하위의 모든 타입의 모든 메서드 중에서 `com.exam.hello.CustomService` 타입으로 스프링 빈에 등록되어 있는 프록시 객체를 보고 판단한다.
- 매개변수를 전달할 수 있다.
	- `@Around("this(obj)") public void methodName(CustomService obj)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"this(obj)"` -> `"this(com.exam.hello.CustomService)"`

> JDK 동적 프록시를 통해 프록시를 생성할 경우, `this`에 구체 클래스를 지정하면 AOP를 적용할 수 없다. JDK 동적 프록시는 인터페이스를 기반으로 프록시를 생성한다. 인터페이스는 구현체를 전혀 알지 못하기 때문에 AOP를 적용할 수 없다.   


#### `target`
`target` 지시자는 실제 `Target` 객체를 대상으로 하는 조인 포인트가 매칭된다. 적용 타입 하나를 정확하게 지정해야 한다.
- `"execution(* com.exam.hello..*.*(..)) && target(com.exam.hello.CustomService)"`
	- `com.exam.hello` 패키지와 그 하위의 모든 타입의 모든 메서드 중에서 `com.exam.hello.CustomService` 타입인 실제 대상 객체를 보고 판단한다.
- 매개변수를 전달할 수 있다.
	- `@Around("target(obj)") public void methodName(CustomService obj)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"target(obj)"` -> `"target(com.exam.hello.CustomService)"`


#### `@target`
`@target`은 인스턴스를 기준으로 인스턴스의 모든 메서드를 조인 포인트로 적용한다. 부모 클래스의 메서드까지 어드바이스를 적용한다.
- `"execution(* com.exam..*(..)) && @target(com.exam.hello.annotation.CustomAnnotation)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 인스턴스 중에서, `@CustomAnnotation` 애노테이션이 붙은 타입의 인스턴스의 모든 메서드를 조인 포인트로 지정한다. 부모 클래스의 메서드에도 적용된다.
	- `child(@CustomAnnotation 있음)`와 `parent(@CustomAnnotation 없음)`가 있을 때, `@target`을 사용하면 `child`와 `parent` 모두 적용된다.
- 매개변수를 전달할 수 있다.
	- `@Around("@target(annotation)") public void methodName(CustomAnnotation annotation)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"@target(annotation)"` -> `"@target(com.exam.hello.annotation.CustomAnnotation)"`

> `@target`은 실제 객체 인스턴스가 생성되고 실행될 때 어드바이스 적용 여부를 확인할 수 있다. 이를 단독으로 사용하게 되면 스프링은 모든 빈에 AOP를 적용하려고 시도하기 때문에 오류가 발생할 수 있다. 따라서 최대한 프록시 적용 대상을 축소하는 표현식과 함께 사용해야 한다.  


#### `@within`
`@within`은 해당 타입 내에 있는 메서드만 조인 포인트로 적용한다. 자기 자신의 클래스에 정의된 메서드에만 어드바이스를 적용한다.
- `"execution(* com.exam..*(..)) && @within(com.exam.hello.annotation.CustomAnnotation)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 인스턴스 중에서, `@CustomAnnotation` 애노테이션이 붙은 타입의 내부에 있는 메서드만을 조인 포인트로 지정한다. 부모 클래스의 메서드에는 적용되지 않는다.
	- `child(@CustomAnnotation 있음)`와 `parent(@CustomAnnotation 없음)`가 있을 때, `@within`을 사용하면 `@CustomAnnotation` 애노테이션이 붙은 `child`만 적용된다.
- 매개변수를 전달할 수 있다.
	- `@Around("@within(annotation)") public void methodName(CustomAnnotation annotation)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"@within(annotation)"` -> `"@within(com.exam.hello.annotation.CustomAnnotation)"`


#### `@annotation`
`@annotation`은 조인 포인트에 주어진 애노테이션이 있으면 매칭된다.
- `"@annotation(com.exam.hello.annotation.MethodAnnotation)"`
	- `@MethodAnnotation` 애노테이션이 붙은 메서드만을 조인 포인트로 지정한다.
- 매개변수를 전달할 수 있다.
	- `@Around("@annotation(annotation)") public void methodName(MethodAnnotation annotation)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"@annotation(annotation)"` -> `"@annotation(com.exam.hello.annotation.MethodAnnotation)"`



#### `@args`
`@args`는 전달된 인수의 런타임 타입에 지정한 타입의 애노테이션이 있는 경우에 매칭된다.
- `"execution(* com.exam..*(..)) && @args(com.exam.hello.annotation.CustomAnnotation)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 인스턴스의 메서드 중에서, 메서드의 파라미터로 넘어온 객체의 런타임 타입에 `@CustomAnnotation` 애노테이션이 붙어있다면 매칭된다.
- 매개변수를 전달할 수 있다.
	- `@Around("@args(annotation)") public void methodName(CustomAnnotation annotation)`
	- 메서드의 매개변수의 이름과 `Pointcut`에 작성한 매개변수 이름이 동일해야 한다.
	- 타입이 메서드에 지정한 타입으로 제한된다.
	- `"@args(annotation)"` -> `"@args(com.exam.hello.annotation.CustomAnnotation)"`

> `@args`는 실제 객체 인스턴스가 생성되고 실행될 때 어드바이스 적용 여부를 확인할 수 있다. 이를 단독으로 사용하게 되면 스프링은 모든 빈에 AOP를 적용하려고 시도하기 때문에 오류가 발생할 수 있다. 따라서 최대한 프록시 적용 대상을 축소하는 표현식과 함께 사용해야 한다.  


#### `bean`
`bean`은 스프링 빈의 이름으로 `Pointcut`을 지정한다. 스프링에서만 사용할 수 있는 특별한 지시자다.
- `"bean(customService) || bean(*Repository)"`
	- `customService`의 이름을 갖는 빈의 메서드와 이름이 `-Repository`로 끝나는 빈의 메서드가 매칭된다.
