# 스프링 공부 내용 요약
## 세션 & 쿠키
클라이언트에서 로그인 요청을 하면 서버는 전송받은 데이터를 검증한다. 검증에 성공하면 로그인 성공 처리를 해주고 클라이언트가 로그인 상태를 유지할 수 있게끔 해줘야 한다. 이때 사용하는 방법이 쿠키를 이용하는 방법이 있다. 로그인에 성공하면 서버에서 쿠키를 생성하고 쿠키를 응답 결과에 담아서 전송하면 클라이언트는 쿠키를 저장해두고 요청마다 해당 쿠키를 전송하면 된다.

쿠키는 값을 임의로 변경할 수 있고 탈취당하기 쉽다. 이를 해결하기 위해 쿠키에 중요한 값을 노출하지 않고 사용자별로 예측이 불가능한 임의의 토큰을 노출하고 사용자 ID를 매핑하여 인식하도록 하고 서버에서 토큰을 관리한다.

이렇게 서버에서 중요한 정보를 보관하고 연결을 유지하는 방법을 **세션**이라고 한다.
서블릿은 세션을 편리하게 사용할 수 있도록 `HttpSession`이라는 기능을 제공한다. 서블릿을 통해 `HttpSession`을 생성하면 서블릿은 `JSESSIONID`라는 이름과 추정 불가능한 랜덤값을 가진 쿠키를 생성한다. 이 값은 `HttpSession`에 저장된 정보와 매핑된다. 서블릿은 이 값을 통해 세션에서 값을 조회한다. 

- 세션을 생성하고 정보를 보관하는 방법.
```java
// request.getSession(false); // 세션이 있으면 세션 반환, 없으면 null 반환
// request.getSession(true : default); // 세션이 없으면 생성
HttpSession session = request.getSession();
session.setAttribute("세션이름", 보관할 정보);
```

- 세션에 저장된 데이터를 조회하는 방법
```java
// JSESSIONID 쿠키를 통해 조회.
Member member = (Member) session.getAttribute("세션이름");
```
또는
```java

@GetMapping
public String sessionAttributeExamp(
	@SessionAttribute(name="세션이름", required=false) Member loginM) {
	// 세션을 찾고, 세션에 들어있는 데이터를 찾는 과정을 스프링이 편리하게 처리해준다.
	// 이는 세션을 생성하지 않는다. 조회용.

	// ...로직
}
```

- 세션에 저장된 데이터를 삭제
```java
HttpSession session = request.getSession(false);
	if (session != null) {
		session.invalidate();
	}
```


- TrackingModes 해제
	- URL에 `JSESSIONID` 노출 해제
	- `server.servlet.session.tracking-modes=cookie`

- 세션 타임아웃 설정
	- `server.servlet.session.timeout=900` -> 900초, 15분
	- `JSESSIONID`를 전달하는 HTTP 요청이 있으면 현재 시간으로 다시 초기화 된다.


## 필터와 인터셉터
매 요청마다 로그인 상태를 확인하기 위해, 또는 특정 작업을 수행하기 위해 필터나 인터셉터를 사용한다. 필터는 서블릿이 제공하는 기술이고 인터셉터는 스프링이 제공하는 기술이다. 필터와 인터셉터의 동작 흐름은 아래와 같다.

	- HTTP 요청 -> WAS -> 필터 -> 서블릿 -> 스프링 인터셉터 -> 컨트롤러

 웹과 관련된 공통 관심사를 처리할 때는 HTTP의 헤더나 URL 정보들이 필요한데, 서블릿 필터나 스프링 인터셉터는 `HttpServletRequest`를 제공한다. 

인터셉터는 스프링 MVC에 특화된 필터 기능을 제공한다. 스프링 MVC를 사용하고, 특별히 필터를 사용해야하는 상황이 아니면 인터셉터를 사용하는 것이 더 편리하다.

인터셉터를 이용하려면 아래의 `HandlerInterceptor`를 구현한 클래스를 만든다.
```java
public interface HandlerInterceptor { 
	// 컨트롤러 호출 전
	// 반환값이 true 이면 다음 인터셉터나 컨트롤러를 호출한다. 
	// false 이면 더 이상 호출하지 않고 response를 반환한다.
	default boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {}

	// 컨트롤러 호출 후
	// 예외 발생시 호출되지 않는다.
	default void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {}
	
	// 요청 완료 이후
	// 예외가 발생해도 무조건 호출된다.
  default void afterCompletion(HttpServletRequest request, HttpServletResponse
response, Object handler, @Nullable Exception ex) throws Exception {} 
```

다음으로 구현한 인터셉터를 등록해준다.
`WebConfig` - 인터셉터 설정
```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

	@Override
	public void addInterceptors(InterceptorRegistry registry) {
  		  registry.addInterceptor(new LogInterceptor()) // 인터셉터 등록.
      	      .order(1) // 인터셉터의 호출 순서 지정.
				  //인터셉터를 적용할 URL 패턴 지정.
          	  .addPathPatterns("/**")
				  // 인터셉터에서 제외할 패턴 지정.
            	  .excludePathPatterns("/css/**", "/*.ico", "/error");
	}
}
```




#Study/Spring MVC 내용 요약#