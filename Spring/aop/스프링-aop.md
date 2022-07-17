# 스프링 AOP
[스프링 AOP - AOP 설명](#aop-설명)

[스프링 AOP - 스프링 AOP 핵심 원리](#스프링-aop-핵심-원리)

  - [스프링 AOP - 빈 후처리기](#빈-후처리기)

  - [스프링 AOP - 프록시](#프록시)

  - [스프링 AOP - 동적 프록시](#동적-프록시)

  - [스프링 AOP - 프록시 팩토리](#프록시-팩토리)
    
  - [스프링 AOP - Advisor](#advisor)



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



## 스프링 AOP 핵심 원리
스프링 AOP를 통해 핵심 로직에 부가 기능 로직을 추가하는 과정은 다음과 같다.

1. 빈 후처리기가 스프링 빈으로 등록할 객체를 전달받아 프록시 팩토리에게 해당 객체를 프록시 객체로 변환을 요청한다.
2. 프록시 팩토리는 전달받은 객체가 프록시를 적용해도 되는지, 어떤 기능의 프록시를 적용할 지 `advisor`를 통해 판단하여 원본 객체를 대상으로 한 프록시를 반환한다.
3. 빈 후처리기는 반환받은 프록시 객체를 원본 객체 대신에 스프링 빈으로 등록한다.

### 빈 후처리기
빈 후처리기(`BeanPostProcessor`)는 빈을 조작하고 변경할 수 있다. 빈을 생성하고 생성된 빈을 등록하기 직전에 어떤 작업을 처리하여 빈을 조작하거나 변경할 수 있다. 빈 후처리기를 사용하려면 `BeanPostProcessor` 인터페이스를 구현하고, 이를 스프링 빈으로 등록하면 된다.

스프링 AOP는 빈 후처리기를 통해 부가 기능 로직 추가를 원하는 빈을 프록시 객체로 바꿔치기하여 이를 스프링 빈에 등록한다. 스프링 AOP는 `AnnotationAwareAspectJAutoProxyCreator`라는 빈 후처리기를 제공하고 스프링부트는 이를 자동으로 스프링 빈으로 등록한다.

`AnnotationAwareAspectJAutoProxyCreator`는 자동으로 프록시를 생성해주는 빈 후처리기이다. 이는 스프링 빈으로 등록된 `Advisor`들을 자동으로 찾아서 프록시가 필요한 곳에 자동으로 프록시를 적용해준다. 자동 프록시 생성기의 작동 과정은 다음과 같다.

1. 스프링이 스프링 빈 대상이 되는 객체를 생성하여 빈 후처리기(`AnnotationAwareAspectJAutoProxyCreator`)에 전달한다.
2. 빈 후처리기(자동 프록시 생성기)는 스프링 컨테이너에서 `Advisor`들을 조회하여 `Advisor` 내부에 포함된 `Pointcut`을 통해 프록시를 적용할 대상인지 판단한다.
3. 프록시 적용 대상이라면 프록시를 생성하고 이를 반환하고 적용 대상이 아니면 원본 객체를 반환한다.
4. 반환받은 객체(프록시 또는 원본 객체)를 스프링 빈으로 등록한다.

### 프록시
프록시(Proxy)는 대리자라는 뜻으로 클라이언트가 사용하려고 하는 실제 대상을 대신하는 대리자가 클라이언트의 요청을 받아주는 역할을 한다. 이때, 클라이언트는 실제 대상에게 요청을 했는지, 프록시에게 요청을 했는지 몰라도 된다. 구체 클래스를 몰라도 된다는 뜻이다.

프록시가 되려면 클라이언트가 요청한 실제 대상과 프록시가 같은 인터페이스를 사용해야 한다. 같은 인터페이스를 사용해야 요청을 보낸 클라이언트의 코드 변경 없이 DI를 통해 실제 대상 객체를 프록시 객체로 변경할 수 있다.

프록시를 사용하면 권한에 따른 접근을 제어를 할 수 있고, 캐싱과 지연로딩이 가능하다. 또한 기존 대상이 제공하는 기능과 더불어 로깅이나 트랜잭션을 지원하는 등의 부가 기능을 수행하게 할 수도 있다. 접근 제어와 부가 기능 추가가 가능한 것이다.

프록시를 적용하게 되면 프록시의 사용 목적에 따라 프록시 패턴과 데코레이터 패턴으로 구분할 수 있다. 접근 제어를 목적으로 프록시를 사용하면 프록시 패턴, 부가 기능 추가가 목적이면 데코레이터 패턴이다. 프록시 패턴과 데코레이터 패턴에 대한 자세한 내용은 디자인 패턴을 공부해보자.

스프링 AOP는 AOP 적용을 원하는 객체를 편리하게 프록시로 변환하기 위해 프록시 팩토리를 사용하여 동적으로 프록시를 생성해준다.

### 동적 프록시
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

이처럼 JDK 동적 프록시 기술과 CGLIB을 통해 인터페이스와 구체 클래스 기반으로 부가 기능을 가진 프록시를 생성할 수 있다. 스프링은 동적 프록시를 통합하여 편리하게 만들어주는 프록시 팩토리라는 기능을 제공한다.

### 프록시 팩토리
스프링은 동적 프록시를 통합하여 편리하게 만들어주는 프록시 팩토리라는 기능을 제공한다. 프록시 팩토리는 인터페이스가 있으면 JDK 동적 프록시를 사용하여 프록시를 만들어주고, 구체 클래스만 있다면 CGLIB를 사용하여 프록시를 만들어준다. 

스프링은 프록시에 부가 기능을 적용하기 위해 JDK 동적 프록시와 CGLIB에서 제공하는 `InvocationHandler`와 `MethodInterceptor` 대신에 `Advice`라는 새로운 개념을 도입했다. 또한 스프링은 특정 조건에 맞을 때만 프록시 부가 기능이 적용되도록 `Pointcut`이라는 개념을 도입하였다. 1개의 `Advice`와 1개의 `Pointcut`을 묶어서 `Advisor`라고 한다. 어디에 어떤 로직을 적용할 지 알고 있는 것이 `Advisor`이다. [스프링 AOP - Advisor](bear://x-callback-url/open-note?id=C015789D-DCFA-4F35-8E12-8055C2C5A06B-91801-000007A00A20BE7B&header=Advisor)

프록시 팩토리를 사용하면 `Advisor`를 필수로 지정해야 한다. `org.aopalliance.intercept.MethodInterceptor` 인터페이스를 구현하여 `Advice`를 만들 수 있다. `org.springframework.aop.Pointcut` 인터페이스를 구현하여 `Pointcut`을 만들 수 있다. 
프록시를 생성하는 쪽에서 프록시 팩토리에 프록시를 적용할 대상 클래스를 넘겨주고, `Advice`와 `Pointcut`을 통해 `Advisor`를 만들고 `addAdvisor()`를 통해 이를 적용하면 `Pointcut`으로 필터링되고, `Advice`가 적용된 프록시를 반환받을 수 있다. `addAdvisor()`를 통해 여러 `Advisor`를 등록할 수도 있다. 이때, 여러 프록시가 생성되는 것이 아니라 하나의 프록시에 여러 어드바이저가 적용된다.
프록시 팩토리에 `setProxyTargetClass(true)`를 통해 `ProxyTargetClass` 옵션을 사용하게 할 수 있다. 이는 인터페이스가 있어도 JDK 동적 프록시 기술을 사용하지 않고 CGLIB를 사용하여 구체 클래스 기반 프록시를 사용하게 하는 옵션이다. 스프링 부트는 AOP를 적용할 때 기본적으로 이 방법을 사용한다.

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



### Advisor
`Advice`는 프록시가 호출하는 부가 기능을 말한다. 프록시의 로직을 뜻하는 것이다.
`Pointcut`은 `Advice`를 어디에 적용할 지, 어디에 `Advice`를 적용하지 않을지 판단하는 필터링 로직이다. 주로 클래스와 메서드 이름으로 필터링을 한다.
1개의 `Advice`와 1개의 `Pointcut`을 묶어서 `Advisor`라고 한다. 어디에 어떤 로직을 적용할 지 알고 있는 것이 `Advisor`이다.

스프링은 필요한 포인트컷을 대부분 제공한다. 메서드 이름을 기반으로 매칭하는 `NameMatchMethodPointcut`, 애노테이션으로 매칭하는 `AnnotationMatchingPointcut`, aspectJ 표현식으로 매칭하는 `AspectJExpressionPointcut` 등을 제공하고 기타 여러 포인트컷을 제공한다. 대부분 사용하기 편리하고 기능도 가장 많은 `AspectJExpressionPointcut`를 사용한다.
