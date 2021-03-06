# 스프링 핵심
## 스프링
- 스프링은 자바 언어 기반의 프레임워크다. -> 자바 언어의 가장 큰 특징은 **객체 지향 언어**라는 점이다.
- 스프링은 객체 지향 언어가 가진 강력한 특징을 살려내는 프레임워크
- 좋은 객체 지향 애플리케이션을 개발할 수 있게끔 도와주는 프레임워크
- 핵심 기술 : 스프링 DI 컨테이너, AOP, 이벤트, etc..

### 객체 지향 프로그래밍
객체지향 프로그래밍은 컴퓨터 프로그램을 명령어의 목록이 아닌 여러개의 독립된 단위인 객체들의 모임으로 파악하고자 하는 것이다. 각각의 객체는 메시지를 주고받고, 데이터를 처리할 수 있다. 협력 관계를 가진다.
객체 지향 프로그래밍은 프로그램을 유연하고 변경이 용이하기 만들기 때문에 대규모 SW 개발에 많이 사용된다.
객체 지향 설계의 특징은 추상화, 캡슐화, 상속, 다형성이 있다. 

### 다형성
객체 지향 설계에서 가장 중요한 특징은 다형성이라고 생각한다. 
다형성을 이용하여 역할(인터페이스)과 구현(인터페이스를 구현한 클래스)으로 분리하면 프로그램을 단순하고 유연하며, 변경이 편리하게 작성할 수 있다. 클라이언트는 대상의 역할만 알고 구현 대상의 내부 구조를 몰라도 된다. 또한 클라이언트는 구현 대상의 내부 구조가 변경되어도 사용에 영향을 받지 않고, 구현 대상 자체를 변경하여도 사용에는 영향을 받지 않는다.




## 스프링의 특징
### IoC(Inversion of Control : 제어의 역전)
프로그램의 제어 흐름을 직접 제어하는 것이 아니라, 외부에서 관리하는 것을 제어의 역전(IoC)이라고 한다. 스프링은 IoC를 지원한다.

### DI(Dependency Injection : 의존관계 주입)
애플리케이션의 런타임에 외부에서 실제 구현 객체를 생성하고 클라이언트에 이를 전달하여 클라이언트와 서버의 실제 의존관계가 연결되는 것을 의존관계 주입이라고 한다. 의존관계 주입을 사용하면 클라이언트 코드를 변경하지 않고, 클라이언트가 호출하는 대상의 타입 인스턴스를 변경할 수 있다. 스프링은 DI를 지원하는 특징을 가진다.

### 컨테이너
객체를 생성하고 관리하면서 의존관계를 연결해 주는 것을 IoC 컨테이너, DI 컨테이너라고 한다. 스프링은 이러한 컨테이너의 특징을 가진다.




## 스프링과 객체 지향
- 스프링은 다형성을 극대화해서 이용할 수 있게 도와준다.
- 스프링에서 이야기하는 제어의 역전(IoC), 의존관계 주입(DI)은 다형성을 활용해서 역할과 구현을 편리하게 다룰 수 있도록 지원한다.
- 스프링을 사용하면 구현을 편리하게 변경할 수 있다.


### 좋은 객체지향 설계의 5가지 원칙(SOLID)
- SRP : 단일 책임 원칙
	- 한 클래스는 하나의 책임만 가져야 한다.
	- 변경이 있을 때 파급 효과가 적으면 단일 책임 원칙을 잘 지킨 것이다.
	- 실행하는 책임, 생성 및 연결 책임 등 관심사를 분리하도록 한다.
- OCP : 개방-폐쇄 원칙
	- 확장에는 열려있으나 변경에는 닫혀있어야 한다.
	- 다형성 활용
	- 객체를 생성하고 연관관계를 맺어주는 별도의 조립, 설정자가 필요 -> 스프링.
- LSP : 리스코프 치환 원칙
	- 프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야 한다.
	- 다형성에서 하위 클래스는 인터페이스 규약을 다 지켜야 한다는 것. 다형성을 지원하기 위한 원칙.
- ISP : 인터페이스 분리 원칙
	- 특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫다.
	- 인터페이스가 명확해지고, 대체 가능성이 높아진다.
- DIP : 의존관계 역전 원칙
	- 추상화에 의존하고, 구체화에 의존하면 안된다.
	- 구현 클래스가 아닌, 인터페이스에 의존하라는 뜻.
	- 클라이언트 코드에서 특정 구체 클래스를 사용하면 DIP를 지킬 수 없다. -> 별도의 조립 설정자 필요.

-> 다형성 만으로는 OCP, DIP를 지킬 수 없다.
-> 스프링은 DI(Dependency Injection : 의존관계, 의존성 주입) 컨테이너를 제공하여 OCP, DIP를 가능하게 지원한다.




## 스프링 컨테이너
`ApplicationContext`를 스프링 컨테이너라 한다. 스프링 컨테이너는 `@Configuration`이 붙은 클래스를 설정 정보로 사용한다. 여기에서 `@Bean` 애노테이션이 붙은 메서드를 모두 호출한 후, 반환된 객체를 스프링 컨테이너에 등록한다. 이런 과정을 거쳐 스프링 컨테이너에 등록된 객체를 **스프링 빈**이라 한다.

스프링 빈은 `@Bean` 애노테이션이 붙은 메서드의 이름을 스프링 빈의 이름으로 사용한다. 스프링 컨테이너에서 `applicationContext.getBean()` 메서드를 사용하여 필요한 스프링 빈을 찾아 꺼내어 사용하면 된다.


### 생성 과정
```java
ApplicationContext applicationContext = 
	new AnnotationConfigApplicationContext(AppConfig.class);
```
1. 구성정보(AppConfig.class)를 지정하여 스프링 컨테이너를 생성한다.
2. 파라미터로 넘어온 설정 클래스 정보를 사용하여 스프링 빈을 등록한다. 설정 클래스 내부에 `@Bean` 애노테이션이 붙은 메서드를 호출하여 반환값을 등록한다. 스프링 빈 이름은 메서드 이름을 사용하고 빈 객체는 메서드의 반환값이다.
3. 스프링 컨테이너는 설정 정보를 참고하여 의존관계를 주입한다.


### BeanFactory & ApplicationContext
`ApplicationContext`를 스프링 컨테이너라 한다 했는데 정확히는 `BeanFactory`와 `ApplicationContext`를 구분한다. `BeanFactory`는 스프링 컨테이너의 최상위 인터페이스로 스프링 빈을 관리하고 조회하는 역할을 담당한다. `BeanFactory`를 직접 사용할 일은 거의 없기 때문에 일반적으로 `ApplicationContext`를 스프링 컨테이너라 하는 것이다. `ApplicationContext`는 `BeanFactory`의 기능을 모두 상속받고 부가기능을 제공한다. 제공하는 부가기능은 다음과 대표적으로 다음과 같다.

- 메시지 소스를 활용한 국제화 기능
- 환경 변수
	- 로컬, 개발, 운영 등을 구분하여 처리
- 애플리케이션 이벤트
	- 이벤트를 발행하고 구독하는 모델을 편리하게 지원한다.
- 편리한 리소스 조회
	- 파일, 클래스패스, 외부 등에서 리소스를 편리하게 조회할 수 있게끔 지원한다.



## 싱글톤 패턴
싱글톤 패턴은 클래스의 인스턴스가 딱 1개만 생성되는 것을 보장하는 디자인 패턴이다. 싱글톤 패턴을 적용하면 요청이 올 때마다 객체를 생성하지 않고, 이미 만들어진 객체를 공유해서 효율적으로 사용할 수 있게끔 한다. 하지만 싱글톤 패턴은 구현하는 코드 자체가 많이 들어가고 의존관계상 클라이언트가 구체 클래스에 의존하여 DIP를 위반한다. 또한 클라이언트가 구체 클래스에 의존하기 때문에 OCP를 위반할 가능성이 높다. 이외에도 테스트하기 어렵고, 내부 속성을 변경하거나 초기화 하기 어려움, private 생성자로 자식 클래스를 만들기 어려움, 유연성이 떨어지는 등 많은 문제를 가진다.

### 싱글톤 컨테이너
하지만 스프링 컨테이너는 싱글톤 패턴의 문제점을 해결하면서 객체 인스턴스를 싱글톤으로 관리한다. 스프링 컨테이너는 싱글톤 패턴을 적용하지 않아도 객체를 하나만 생성해서 관리한다. -> 싱글톤으로 관리.

주의할 점은 싱글톤 방식은 객체 인스턴스를 하나만 생성해서 관리하기 때문에 상태를 유지하면 안되고 무상태로 설계해야 한다는 점이다.


### @Configuration
`@Configuration` 애노테이션을 붙이면 바이트코드를 조작하는 CGLIB 기술을 사용하여 @Bean이 붙은 메서드마다 이미 스프링 빈이 존재하면 존재하는 빈을 반환하고, 빈이 없으면 생성하여 스프링 빈으로 등록하고 반환하도록 한다. 이를 통해 싱글톤을 보장해준다.





## 정리
- 스프링은 객체 지향 언어가 가진 강력한 특징을 잘 살려낼 수 있는 프레임워크이다.
- 다형성을 통해 DI와 IoC를 지원한다.
- 스프링은 DI 컨테이너의 특징을 가진다.
- 다형성 만으로는 OCP, DIP 원칙을 지킬 수 없지만, 스프링은 DI 컨테이너를 제공하여 이를 가능하게끔 한다.
- 스프링 컨테이너는 싱글톤 컨테이너이다. 싱글톤 패턴의 문제점을 해결하면서 객체 인스턴스를 싱글톤으로 관리한다.
	- 싱글톤 방식은 무상태로 설계해야 한다.




#스프링 기초#
#스프링 기초/스프링 핵심#
#스프링 기초/스프링 특징#

---
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.
