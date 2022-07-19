# 스프링 AOP
[1. AOP 설명](#aop-설명)

[2. 스프링 AOP 핵심 원리](#스프링-aop-핵심-원리)

  - [2.1. 빈 후처리기](#빈-후처리기)

  - [2.2. Advisor](#advisor)

  - [2.3. 프록시](#프록시)

[3. 스프링 AOP 적용](#스프링-aop-적용)

  - [3.1. 어드바이스 종류](#어드바이스-종류)
  
  - [3.2. JoinPoint](#joinpoint)

  - [3.3. 포인트컷 적용](#포인트컷-적용)
  
  - [3.4. `Advice` 적용 순서 지정](#advice-적용-순서-지정)

[4. Pointcut 표현식](#pointcut-표현식)


## AOP 설명
AOP는 `Aspect Oriented Programming`의 약자로 관점 지향 프로그래밍을 말한다. 관점 지향이란 애플리케이션의 기능을 핵심 기능과 공통 부가 기능의 관점으로 바라보는 것을 말한다. AOP에서는 애플리케이션 전반에 흩어져 존재하는 트랜잭션이나, 로깅, 보안 등과 같은 공통된 부가 기능들을 각각 하나의 공통 관심사로 보고, 이러한 공통 관심사들이 핵심 비즈니스 로직에서 반복적으로 나타나는 것을 분리하여 관심사별로 모듈화한다. 이렇게 모듈화된 하나의 공통 관심사를 `Aspect`라고 한다. 그리고 이 `Aspect`를 어느 곳에 적용할 지 선택하도록 한다.

AOP는 OOP를 대체하기 위한 것이 아니라 애플리케이션 전반에 걸친 공통 관심사인 횡단 관심사(`cross-cutting concerns`)를 깔끔하게 처리하기 어려운 OOP의 부족한 부분을 보조하는 목적으로 개발되었다.
OOP에서는 공통된 기능을 재사용하는 방법으로 상속 또는 위임을 사용한다. SW 개발에서 변경 지점은 하나가 될 수 있도록 모듈화가 필요하다. 하지만 애플리케이션 전반에 걸친 부가기능들은 OOP의 상속과 위임만으로는 깔끔한 모듈화가 어렵다. 이를 해결하기 위해 AOP가 등장한 것이다.


### 스프링 AOP
AOP를 구현한 구현체로는 대표적으로 **AspectJ 프레임워크**와 **스프링 AOP**가 있다. 스프링 AOP는 AspectJ의 문법을 차용하고 AspectJ가 제공하는 기능의 일부만 제공한다.

AOP는 핵심 비즈니스 로직에서 공통 부가 기능을 분리하고, 코드 수정 없이 공통 부가기능을 핵심 로직에 적용할 수 있다. 원본 로직에 부가 기능 로직이 추가되는 것을 위빙(Weaving)이라 한다. 위빙 방법은 크게 3가지가 있다.

- 컴파일 타임 위빙 : `.java` 파일을 `.class`로 만드는 컴파일 타임에 부가 기능 로직을 추가한다. AspectJ가 제공하는 특별한 컴파일러를 사용해야 한다.
- 로드 타임 위빙 : 자바를 실행하면 `.class` 파일을 JVM 내부의 클래스 로더에 보관하는데 이때 클래스 로더 조작기를 통해 `.class` 파일을 조작하여 부가 기능 로직을 추가하고 JVM에 올린다.
- 런타임 위빙 : 자바의 `main` 메서드가 이미 실행되고 난 다음에 자바 언어가 제공하는 범위 안에서 부가 기능을 적용한다. 프록시 패턴을 이용한다.

컴파일 타임 위빙과 로드 타임 위빙은 실제 대상 코드에 부가 기능 코드가 포함되지만 AspectJ를 직접 사용해야 한다. 하지만 런타임 위빙은 실제 대상 코드는 그대로 유지되고 프록시를 통해 부가 기능이 적용된다. AspectJ를 사용하지 않아도 AOP를 적용할 수 있다. 스프링 AOP는 런타임 위빙 방식과 스프링 컨테이너를 통해 AOP를 적용한다.


### AOP 용어
AOP에서 사용하는 용어는 다음과 같다.

- `Aspect` : `Aspect`는 부가 기능을 핵심 기능에서 분리하고 한 곳에서 관리하는 기능과 부가 기능을 어디에 적용할지 선택할 수 있도록 하는 기능을 합하여 하나의 모듈로 만든 것이다. `Advice`와 `Pointcut`을 모듈화 한 것이다. 여러 `Advice`와 `Pointcut`이 함께 존재한다.
- `Join point` : `Advice`를 적용할 위치로 메서드 실행, 생성자 호출, 필드값 접근, static 메서드 접근 등 프로그램 실행 중 지점을 말한다. 이는 추상적인 개념으로 AOP를 적용할 수 있는 모든 지점을 말한다. 스프링 AOP는 프록시 방식을 사용하기 때문에 `Join point`는 항상 메소드 실행 지점으로 제한된다.
- `Pointcut` : `Advice`가 적용될 위치를 선별한다. 주로 `AspectJ` 표현식을 통해 지정한다. 스프링 AOP는 메서드 실행 지점만 `Pointcut`으로 선별 가능하다.
- `Target` : `Advice`를 받는 객체를 말하며 `Pointcut`으로 결정한다.
- `Advice` : `Advice`는 부가 기능을 말한다. 
- `Advisor` : 스프링 AOP에서만 사용되는 용어로 하나의 `Advice`와 하나의 `Pointcut`으로 구성된다.


[처음으로](#스프링-aop)


## 스프링 AOP 핵심 원리
스프링 AOP를 통해 핵심 로직에 부가 기능 로직을 추가하는 과정은 다음과 같다.

1. 스프링 컨테이너 시작
2. 스프링 빈으로 등록할 객체를 생성하고 빈 후처리기에 전달한다.
3. 빈 후처리기는 컨테이너에서 `Advisor` 빈을 모두 조회한다.
4. 빈 후처리기는 `@Aspect` 애노테이션이 붙은 빈을 모두 조회하여 `@Aspect Advisor` 빌더에게 전달한다.
	- `@Aspect Advisor` 빌더는 `@Aspect` 애노테이션 정보를 기반으로 `Advisor`를 생성한다.
	- 이후 생성한 `Advisor`를  `@Aspect Advisor` 빌더 내부에 저장해둔다.
5. 빈 후처리기는 `@Aspect Advisor` 빌더에서 내부에 저장된 `Advisor`를 모두 조회한다.
6. 빈 후처리기는 조회한 `Advisor` 내부의 `Pointcut`을 사용하여 스프링 빈으로 등록할 객체가 프록시 적용 대상인지 판단한다. 프록시 적용 대상이라면 `Advisor` 내부의 `Advice`를 적용한 프록시를 생성하고 이를 반환한다. 프록시 적용 대상이 아니면 기존 객체를 반환한다.
7. 스프링 컨테이너는 반환받은 객체를 스프링 빈으로 등록한다.


### 빈 후처리기
빈 후처리기(`BeanPostProcessor`)는 빈을 조작하고 변경할 수 있다. 빈을 생성하고 생성된 빈을 등록하기 직전에 어떤 작업을 처리하여 빈을 조작하거나 변경할 수 있다. 빈 후처리기를 사용하려면 `BeanPostProcessor` 인터페이스를 구현하고, 이를 스프링 빈으로 등록하면 된다.

스프링 AOP는 빈 후처리기를 통해 부가 기능 로직 추가를 원하는 빈을 프록시 객체로 바꿔치기하여 이를 스프링 빈에 등록한다. 스프링 AOP는 `AnnotationAwareAspectJAutoProxyCreator`라는 빈 후처리기를 제공하고 스프링부트는 이를 자동으로 스프링 빈으로 등록한다.

`AnnotationAwareAspectJAutoProxyCreator`는 자동으로 프록시를 생성해주는 빈 후처리기이다. 이는 스프링 빈으로 등록된 `Advisor`들을 자동으로 찾아서 프록시가 필요한 곳에 자동으로 프록시를 적용해준다. 
또한 자동 프록시 생성기는 스프링 컨테이너에서 `@Aspect` 애노테이션이 붙은 빈을 찾아서 `@Aspect Advisor` 빌더를 통해 `@Aspect` 애노테이션 정보를 기반으로 `Advisor`를 만들고 이를 빌더 내부에 저장한다. 이렇게 생성된 `Advisor`들도 자동 프록시 생성기에서 조회하여 프록시 적용에 사용한다.

자동 프록시 생성기의 작동 과정은 다음과 같다.

1. 스프링이 스프링 빈 대상이 되는 객체를 생성하여 빈 후처리기(`AnnotationAwareAspectJAutoProxyCreator`)에 전달한다.
2. 빈 후처리기(자동 프록시 생성기)는 스프링 컨테이너에 등록된 `@Aspect` 애노테이션이 붙은 빈을 모두 조회하여 `@Aspect Advisor` 빌더를 통해 `Advisor`를 생성하고 빌더 내부에 생성된 `Advisor`를 저장한다.
3. 자동 프록시 생성기는 `@Aspect Advisor` 빌더 내부에 저장된 `Advisor`를 모두 조회한다.
4. 자동 프록시 생성기는 스프링 컨테이너에 등록된 `Advisor` 빈을 모두 조회한다.
5. 조회한 `Advisor` 내부에 포함된 `Pointcut`을 통해 스프링 빈으로 등록할 객체가 프록시를 적용할 대상인지 판단한다.
6. 프록시 적용 대상이라면 프록시를 생성하고 이를 반환하고 적용 대상이 아니면 원본 객체를 반환한다.
7. 반환받은 객체(프록시 또는 원본 객체)를 스프링 빈으로 등록한다.


### Advisor
`Advisor`는 1개의 `Advice`와 1개의 `Pointcut`을 묶어둔 것을 말한다.
`Advice`는 프록시에 적용할 부가 기능 로직을 말한다.
`Pointcut`은 어떤 객체에 프록시를 적용할지 적용하지 않을지 판단하는 필터링 로직이다. 주로 클래스 이름과 메서드 이름으로 필터링한다.
따라서 `Advisor`는 어디에 어떤 로직을 적용해야 할 지 알고있는 객체로 볼 수 있다.

> 만약 하나의 객체에 여러 `Advisor`가 필터링 될 수 있다. 이때, 여러 프록시가 생성되는 것이 아니라 여러 `Advisor`가 적용된 하나의 프록시 객체만을 생성한다.

개발자는 프록시에 어떤 로직을 적용하고, 프록시를 적용할 대상을 필터링하기 위해서 `Advice`와 `Pointcut`을 구현하고 이를 기반으로 `Advisor`를 생성하여 빈으로 등록만 하면 된다.
스프링 AOP는 `Advisor`를 편리하게 구현할 수 있도록 `@Aspect` 애노테이션을 제공한다. `@Aspect` 애노테이션이 붙은 클래스에 다음과 같이 작성하면 `@Aspect Advisor` 빌더를 통해 `Advisor`를 생성할 수 있다.

- `@Aspect`를 이용하여 `Advisor`를 작성하는 예시
```java
@Aspect
public class CustomAspect {
	// @Around는 Pointcut이 된다. Aspectj 표현식을 사용한다.
	// 포인트컷을 위한 다른 애노테이션이 더 있다.
	@Around("execution(* com.exam.hello..*(..))")
	public Object execute(ProceedingJoinPoint joinPoint) throws Throwable {
		// 메서드는 Advice가 된다.
		// Advice 로직

		// 기존 로직 호출
		Object result = joinPoint.proceed();
		// 기존 로직 호출 결과 반환.
		return result;
	}
}
```


`Advisor`를 직접 생성하고 빈으로 등록하려면 `org.aopalliance.intercept.MethodInterceptor` 인터페이스를 구현하여 `Advice`를 만들고, `org.springframework.aop.Pointcut` 인터페이스를 구현하여 `Pointcut`을 만들어 `Advisor`를 만들 수 있다. 이렇게 생성한 `Advisor`를 스프링 빈으로 등록하면 된다.

- `Advice`와 `Pontcut`을 직접 구현하고 `Advisor`를 생성하여 스프링 빈으로 등록하는 예시.
```java
// Advice를 정의한다.
public class CustomAdvice implements MethodInterceptor {

    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        // 추가 기능 로직

        // 실제 대상 target의 메서드 호출
        Object result = invocation.proceed();

        // 추가 기능 로직

        return result;
    }
}

// Advice를 적용할 대상을 필터링하는 Pointcut을 정의한다.
public class CustomPointcut implements Pointcut {
    @Override
    public ClassFilter getClassFilter() {
        // 클래스 정보를 필터링 한다.
        // 로직 구현
        return null;
    }

    @Override
    public MethodMatcher getMethodMatcher() {
        // CustomMethodMatcher 를 통해 메서드를 필터링 한다.
        return new CustomMethodMatcher();
    }
    
    static class CustomMethodMatcher implements MethodMatcher {

        @Override
        public boolean matches(Method method, Class<?> targetClass) {
            // 메서드 정보를 통해 프록시를 적용할 메서드를 필터링한다.
            // 매칭 로직 구현
            return false;
        }

        @Override
        public boolean isRuntime() {
            // 반환값이 참이면 matches(... args) 메서드가 대신 호출된다. 
            // 동적으로 넘어오는 매개변수를 판단 로직으로 사용할 수 있다.
            // false를 반환하면 클래스의 정적 정보만을 사용하여 스프링이 내부에서 캐싱을 통해 성능 향상이 가능하다.
            // true를 반환할 경우 매개변수가 동적으로 변경된다고 가정하기 때문에 캐싱하지 않는다.
            return false;
        }

        @Override
        public boolean matches(Method method, Class<?> targetClass, Object... args) {
            // 매칭 로직 구현
            return false;
        }
    }
}

public class CustomAdvisorConfig {
	// CustomPointcut과 CustomAdvice를 통해 Advisor를 생성하고 이를 빈으로 등록한다.
	@Bean
	public Advisor customAdvisor() {
		return new DefaultPointcutAdvisor(new CustomPointcut(), new CustomAdvice());
	}
}
```

> 스프링은 필요한 포인트컷을 대부분 제공한다. 따라서 위와 같이 직접 포인트컷을 만들지 않고 스프링이 제공하는 포인트컷을 사용해도 된다. 메서드 이름을 기반으로 매칭하는 `NameMatchMethodPointcut`, 애노테이션으로 매칭하는 `AnnotationMatchingPointcut`, aspectJ 표현식으로 매칭하는 `AspectJExpressionPointcut` 등과 기타 여러 포인트컷을 제공한다. 대부분 사용하기 편리하고 기능도 가장 많은 `AspectJExpressionPointcut`을 사용한다. `@Aspect`를 이용하여 `Advisor`를 작성하는 예시에서 `@Around("execution(.....)")` 애노테이션 부분에 `AspectJExpressionPointcut`을 사용했다.

위 예시들과 같이 `Advisor`를 등록하면 빈 후처리기(자동 프록시 생성기)는 `Advisor`의 `Pointcut`을 통해 빈으로 등록할 대상을 필터링하여 `Advice`를 적용한 프록시 객체를 생성하여 반환하거나 기존 객체를 반환하고, 반환된 객체는 스프링 빈에 등록된다.


### 프록시
프록시(Proxy)는 대리자라는 뜻으로 클라이언트가 사용하려고 하는 실제 대상을 대신하는 대리자가 클라이언트의 요청을 받아주는 역할을 한다. 이때, 클라이언트는 실제 대상에게 요청을 했는지, 프록시에게 요청을 했는지 몰라도 된다. 구체 클래스를 몰라도 된다는 뜻이다.

프록시가 되려면 클라이언트가 요청한 실제 대상과 프록시가 같은 인터페이스를 사용해야 한다. 같은 인터페이스를 사용해야 요청을 보낸 클라이언트의 코드 변경 없이 DI를 통해 실제 대상 객체를 프록시 객체로 변경할 수 있다.
자바에서는 다형성을 지원하기 때문에 상속이나 인터페이스 구현을 통해 프록시를 사용할 수 있다.

프록시를 사용하면 권한에 따른 접근을 제어를 할 수 있고, 캐싱과 지연로딩이 가능하다. 또한 기존 대상이 제공하는 기능과 더불어 로깅이나 트랜잭션을 지원하는 등의 부가 기능을 수행하게 할 수도 있다. 접근 제어와 부가 기능 추가가 가능한 것이다.

프록시를 적용하게 되면 프록시의 사용 목적에 따라 프록시 패턴과 데코레이터 패턴으로 구분할 수 있다. 접근 제어를 목적으로 프록시를 사용하면 프록시 패턴, 부가 기능 추가가 목적이면 데코레이터 패턴을 사용할 수 있다. 

프록시 패턴 사용의 예를 들자면 JPA의 지연 로딩이 있다. JPA는 엔티티를 지연로딩 하면 내부에 캐시를 두어 접근 제어를 한다. 지연로딩으로 엔티티를 조회한 시점에는 프록시의 캐시에 아무런 데이터가 없다. 이후 해당 엔티티를 사용하면 그 때 조회 쿼리를 전송하고 엔티티의 캐시에 데이터를 보관해둔다. 엔티티 캐시에 데이터가 존재하는 시점부터는 더 이상 DB에 조회 쿼리를 전송하지 않는다.

데코레이터 패턴 사용은 메서드 수행 시간을 측정하는 기능을 도입하는 것을 예로 들 수 있다. 기존 객체를 변경하지 않고 부가 기능을 추가하고 싶다면 기존 객체를 상속받거나 대상 객체의 인터페이스를 구현하고, 대상 객체를 주입받아 내부에서 기존 객체의 메서드를 호출하면 된다. 대상 객체의 메서드를 호출하는 곳에서 어떠한 부가 기능이라도 수행이 가능하다. 이제 이렇게 만든 프록시를 기존 객체 대신 사용하면 기존 객체의 코드는 변경 없이 부가 기능을 추가할 수 있다.

> 프록시 패턴과 데코레이터 패턴에 대한 자세한 내용은 디자인 패턴을 공부해보도록 한다.

#### 동적 프록시
프록시 패턴과 데코레이터 패턴을 사용하여 프록시를 적용하면 기존 코드를 변경하지 않고도 부가 기능을 추가할 수 있다. 하지만 직접 프록시를 직접적으로 적용하려면 프록시 적용을 원하는 대상 수 만큼 프록시 클래스를 만들어야 한다는 문제가 있다. 이를 해결하기 위해 자바에서 제공하는 **JDK 동적 프록시 기술**이나 **CGLIB와 같은 프록시 생성 오픈소스 기술**을 활용할 수 있다. 이러한 동적 프록시 기술을 사용하면 프록시를 적용할 코드를 하나만 만들어 두고, 런타임에 프록시 객체를 동적으로 생성해준다.

#### JDK 동적 프록시
JDK 동적 프록시는 리플렉션을 통해 프록시를 동적으로 생성한다. 리플렉션은 클래스나 메서드의 메타정보를 사용하여 동적으로 호출하는 메서드를 변경할 수 있는 기술이다. JDK 동적 프록시는 **인터페이스를 기반**으로 프록시를 동적으로 만들어준다. **인터페이스가 없으면 JDK 동적 프록시 기술을 사용할 수 없다.**

JDK 동적 프록시를 통해 프록시를 동적으로 생성하려면 `InvocationHandler` 인터페이스를 구현하여 프록시의 틀을 정의하고, 프록시를 생성하는 곳에서 `java.lang.reflect.Proxy`의 `newProxyInstance()` 메서드를 통해 프록시를 만들 수 있다.

- JDK 동적 프록시를 사용하여 프록시를 만드는 예
```java
// JDK 동적 프록시를 적용할 틀을 정의.
public class CustomInvocationHandler implements InvocationHandler {
    // 동적 프록시가 호출할 대상 객체이다.
    private final Object target;

    public CustomInvocationHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 추가 로직
        
        // 실제 대상 target의 메서드 호출
        Object result = method.invoke(target, args);
        
        // 추가 로직
        return result;
    }
}

// Proxy를 생성한다.
public class CreateProxy {
    public void do() {
        // CustomInterface 인터페이스 타입의 객체를 생성한다.
        CustomInterface target = new CustomInterfaceImpl();
        // 프록시를 적용할 틀에 대상 객체를 넣는다.
        CustomInvocationHandler handler = new CustomInvocationHandler(target);
        // Proxy.newProxyInstance 메서드를 통해 프록시를 적용한 객체를 생성하고 원본 대상과 같은 인터페이스로 사용하도록 한다.
        CustomInterface proxy = (CustomInterface) Proxy.newProxyInstance(CustomInterface.class.getClassLoader(), new Class[] {CustomInterface.class}, handler);
        // 생성된 프록시는 원본 객체처럼 사용할 수 있다. CustomInterface 타입의 save 메서드를 호출하는 예이다.
        proxy.save();
    }
}
```

#### CGLIB 프록시
CGLIB은 바이트코드를 조작하여 동적으로 클래스를 생성하는 기술을 제공하는 라이브러리이다. CGLIB을 사용하면 인터페이스가 없어도 구체 클래스만 가지고 동적 프록시를 만들어낼 수 있다.

CGLIB을 통해 프록시를 동적으로 생성하려면 `MethodInterceptor` 인터페이스를 구현하여 프록시의 틀을 정의하고, 프록시를 생성하는 곳에서 `org.springframework.cglib.proxy.Enhancer`에 `setSuperclass()`를 통해 어떤 구체 클래스를 상속받을지 지정하고, `setCallback()`을 통해 프록시에 적용할 실행 로직을 할당한 후, `create()`를 통해 프록시를 만들 수 있다.

```java
// CGLIB 프록시를 적용할 틀을 정의.
public class CustomMethodInterceptor implements MethodInterceptor {

    private final Object target;

    public CustomMethodInterceptor(Object target) {
        this.target = target;
    }

    @Override
    public Object intercept(Object o, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
        // 추가 로직

        // 실제 대상 target의 메서드 호출
        Object result = methodProxy.invoke(target, args);

        // 추가 로직
        return result;
    }
}

// Proxy를 생성한다.
public class CreateProxy {
    public void do() {
        // CustomClass 인터페이스 타입의 객체를 생성한다.
        CustomClass target = new CustomClass();
        // enhancer를 통해 어떤 구체클래스를 상속받을지, 어떤 로직의 프록시를 적용할지 지정한다.
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(CustomClass.class);
        enhancer.setCallback(new CustomMethodInterceptor(target));
        // enhancer.create()를 통해 프록시를 생성받는다.
        CustomClass proxy = (CustomClass) enhancer.create();

        // 생성된 프록시는 원본 객체처럼 사용할 수 있다. CustomClass 타입의 save 메서드를 호출하는 예이다.
        proxy.save();
    }
}
```

이처럼 JDK 동적 프록시 기술과 CGLIB을 통해 인터페이스와 구체 클래스 기반으로 부가 기능을 가진 프록시를 생성할 수 있다. 하지만 인터페이스와 구체 클래스에 대한 프록시의 틀을 분리하여 작성해야 한다. 이를 해결하기 위해 스프링은 동적 프록시를 통합하여 편리하게 만들어주는 프록시 팩토리라는 기능을 제공한다.

#### 프록시 팩토리
스프링은 동적 프록시를 통합하여 편리하게 만들어주는 프록시 팩토리라는 기능을 제공한다. 프록시 팩토리는 인터페이스가 있으면 JDK 동적 프록시를 사용하여 프록시를 만들어주고, 구체 클래스만 있다면 CGLIB를 사용하여 프록시를 만들어준다.

프록시 팩토리에 `setProxyTargetClass(true)`를 통해 `ProxyTargetClass` 옵션을 사용하게 할 수 있다. 이는 인터페이스가 있어도 JDK 동적 프록시 기술을 사용하지 않고 CGLIB를 사용하여 구체 클래스 기반 프록시를 사용하게 하는 옵션이다.

스프링은 프록시에 부가 기능을 적용하기 위해 JDK 동적 프록시와 CGLIB에서 제공하는 `InvocationHandler`와 `MethodInterceptor` 대신에 `Advice`라는 새로운 개념을 도입했다. 또한 스프링은 특정 조건에 맞을 때만 프록시 부가 기능이 적용되도록 `Pointcut`이라는 개념을 도입하였다. 1개의 `Advice`와 1개의 `Pointcut`을 묶어서 `Advisor`라고 한다. 어디에 어떤 로직을 적용할 지 알고 있는 것이 `Advisor`이다. 프록시 팩토리를 사용하면 `Advisor`를 필수로 지정해야 한다. [Advisor 설명](#advisor)

> 프록시 팩토리가 등장한 시점에는 프록시 자동 생성기가 없었다. 프록시 팩토리를 위해 `Advisor`가 등장하고, 이를 더욱 편리하게 이용할 수 있도록 프록시 자동 생성기가 등장하였다. 
> 현시점에서 스프링 부트는 스프링 AOP에서 제공하는 빈 후처리기(자동 프록시 생성기)인 `AnnotationAwareAspectJAutoProxyCreator`를 사용하여 프록시를 생성한다. 프록시 팩토리를 사용하는 것은 아니지만, 프록시 팩토리와 비슷한 방법으로 프록시를 생성한다.

- `ProxyFactory`와 `Advisor`를 통해 프록시를 생성하는 예
```java
// Proxy를 생성한다.
public class CreateProxy {
    public void do() {
        // CustomClass 인터페이스 타입의 객체를 생성한다.
        CustomClass target = new CustomClass();
        ProxyFactory proxyFactory = new ProxyFactory(target);
        // 인터페이스 여부에 관계없이 CGLIB를 사용하여 구체 클래스 기반 프록시를 만든다.
        proxyFactory.setProxyTargetClass(true);
        // CustomPointcut과 CustomAdvice를 기반으로 Advisor를 생성한다.
        DefaultPointcutAdvisor advisor = new DefaultPointcutAdvisor(new CustomPointcut(), new CustomAdvice());
        // Advisor를 등록한다.
        // 프록시 팩토리는 advisor의 pointcut을 보고 tartget을 필터링하여 advice를 적용할지 판단한다.
        proxyFactory.addAdvisor(advisor);

        // Advice 기능이 적용된 프록시를 반환받는다.
        // Pointcut을 통해 필터링 되기 때문에 프록시가 적용되지 않았을 수도 있다.
        CustomClass proxy = (CustomClass) proxyFactory.getProxy();

        // 생성된 프록시는 원본 객체처럼 사용할 수 있다. CustomClass 타입의 save 메서드를 호출하는 예이다.
        proxy.save();
    }
}
```


[처음으로](#스프링-aop)



## 스프링 AOP 적용
[스프링 AOP - 어드바이스 종류](#어드바이스-종류)

[스프링 AOP - JoinPoint](#joinpoint)

[스프링 AOP - 포인트컷 적용](#포인트컷-적용)

[스프링 AOP - `Advice` 적용 순서 지정](#advice-적용-순서-지정)


`@Asepct` 애노테이션을 사용하여 스프링 AOP를 구현할 수 있다.
스프링 AOP로 사용하기를 원하는 클래스에 `@Aspect` 애노테이션을 붙이면 스프링 AOP는 이를 인식하여 내부의 `@Pointcut`, `@Around` 등의 애노테이션을 보고 `Advisor`를 생성, 이를 기반으로 스프링 AOP가 적용된 프록시를 생성할 수 있게끔 한다.

`Advisor`를 구현하려면 `Advice` 종류 선택, `Pointcut` 적용, `Advice` 기능 구현의 과정이 모두 이루어져야 한다.

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
포인트컷 표현식은 포인트컷 지시자(Pointcut Designator : PCD)로 시작한다. 포인트컷 지시자의 종류는 다음과 같은 것들이 있다.

- `execution` : 메서드 실행 조인 포인트를 매칭한다.
- `within` : 특정 타입 내의 조인 포인트를 매칭한다.
- `args` : 조인 포인트의 파라미터가 주어진 타입의 인스턴스일 때 매칭된다. 단독으로 사용하면 안된다.
- `this` : 스프링 빈 객체(스프링 AOP 프록시)를 대상으로 하는 조인 포인트
- `target` : Target 객체(스프링 AOP 프록시가 가르키는 실제 대상)를 대상으로 하는 조인 포인트 
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

> `args`는 실제 객체 인스턴스가 생성되고 실행될 때 어드바이스 적용 여부를 확인할 수 있다. 이를 단독으로 사용하게 되면 스프링은 모든 빈에 AOP를 적용하려고 시도하기 때문에 오류가 발생할 수 있다. 따라서 최대한 프록시 적용 대상을 축소하는 표현식과 함께 사용해야 한다.


#### `this`
`this` 지시자는 스프링 빈으로 등록된 `Proxy` 객체를 대상으로 하는 조인 포인트가 매칭된다. 적용 타입 하나를 정확하게 지정해야 한다.
- `"execution(* com.exam.hello..*.*(..)) && this(com.exam.hello.CustomService)"`
	- `com.exam.hello` 패키지와 그 하위의 모든 타입의 모든 메서드 중에서 `com.exam.hello.CustomService` 타입으로 스프링 빈에 등록되어 있는 프록시 객체를 보고 판단한다.

> JDK 동적 프록시를 통해 프록시를 생성할 경우, `this`에 구체 클래스를 지정하면 AOP를 적용할 수 없다. JDK 동적 프록시는 인터페이스를 기반으로 프록시를 생성한다. 인터페이스는 구현체를 전혀 알지 못하기 때문에 AOP를 적용할 수 없다. 


#### `target`
`target` 지시자는 실제 `Target` 객체를 대상으로 하는 조인 포인트가 매칭된다. 적용 타입 하나를 정확하게 지정해야 한다.
- `"execution(* com.exam.hello..*.*(..)) && target(com.exam.hello.CustomService)"`
	- `com.exam.hello` 패키지와 그 하위의 모든 타입의 모든 메서드 중에서 `com.exam.hello.CustomService` 타입인 실제 대상 객체를 보고 판단한다.


#### `@target`
`@target`은 인스턴스를 기준으로 인스턴스의 모든 메서드를 조인 포인트로 적용한다. 부모 클래스의 메서드까지 어드바이스를 적용한다.
- `"execution(* com.exam..*(..)) && @target(com.exam.hello.annotation.CustomAnnotation)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 인스턴스 중에서, `@CustomAnnotation` 애노테이션이 붙은 타입의 인스턴스의 모든 메서드를 조인 포인트로 지정한다. 부모 클래스의 메서드에도 적용된다.
	- `child(@CustomAnnotation 있음)`와 `parent(@CustomAnnotation 없음)`가 있을 때, `@target`을 사용하면 `child`와 `parent` 모두 적용된다.

> `@target`은 실제 객체 인스턴스가 생성되고 실행될 때 어드바이스 적용 여부를 확인할 수 있다. 이를 단독으로 사용하게 되면 스프링은 모든 빈에 AOP를 적용하려고 시도하기 때문에 오류가 발생할 수 있다. 따라서 최대한 프록시 적용 대상을 축소하는 표현식과 함께 사용해야 한다.


#### `@within`
`@within`은 해당 타입 내에 있는 메서드만 조인 포인트로 적용한다. 자기 자신의 클래스에 정의된 메서드에만 어드바이스를 적용한다.
- `"execution(* com.exam..*(..)) && @within(com.exam.hello.annotation.CustomAnnotation)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 인스턴스 중에서, `@CustomAnnotation` 애노테이션이 붙은 타입의 내부에 있는 메서드만을 조인 포인트로 지정한다. 부모 클래스의 메서드에는 적용되지 않는다.
	- `child(@CustomAnnotation 있음)`와 `parent(@CustomAnnotation 없음)`가 있을 때, `@within`을 사용하면 `@CustomAnnotation` 애노테이션이 붙은 `child`만 적용된다.


#### `@annotation`
`@annotation`은 조인 포인트에 주어진 애노테이션이 있으면 매칭된다.
- `"@annotation(com.exam.hello.annotation.MethodAnnotation)"`
	- `@MethodAnnotation` 애노테이션이 붙은 메서드만을 조인 포인트로 지정한다.


#### `@args`
`@args`는 전달된 인수의 런타임 타입에 지정한 타입의 애노테이션이 있는 경우에 매칭된다.
- `"execution(* com.exam..*(..)) && @args(com.exam.hello.annotation.CustomAnnotation)"`
	- `com.exam` 패키지와 그 하위 패키지의 모든 타입의 인스턴스의 메서드 중에서, 메서드의 파라미터로 넘어온 객체의 런타임 타입에 `@CustomAnnotation` 애노테이션이 붙어있다면 매칭된다.

> `@args`는 실제 객체 인스턴스가 생성되고 실행될 때 어드바이스 적용 여부를 확인할 수 있다. 이를 단독으로 사용하게 되면 스프링은 모든 빈에 AOP를 적용하려고 시도하기 때문에 오류가 발생할 수 있다. 따라서 최대한 프록시 적용 대상을 축소하는 표현식과 함께 사용해야 한다.


#### `bean`
`bean`은 스프링 빈의 이름으로 `Pointcut`을 지정한다. 스프링에서만 사용할 수 있는 특별한 지시자다.
- `"bean(customService) || bean(*Repository)"`
	- `customService`의 이름을 갖는 빈의 메서드와 이름이 `-Repository`로 끝나는 빈의 메서드가 매칭된다.


```java
```

