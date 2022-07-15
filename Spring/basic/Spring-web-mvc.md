# 스프링 Web MVC
## 웹 시스템 구성
웹 시스템은 보통 웹 서버, 웹 애플리케이션 서버, DB로 구성된다.

- Web Server
	- HTTP 기반으로 동작한다.
	- 정적 리소스(HTML, CSS, JS, IMG, 영상 등)를 제공하고 기타 부가 기능이 있다.
	- NGINX, APACHE 등이 웹 서버의 예이다.

- Web Application Server - WAS
	- HTTP 기반으로 동작한다
	- 웹 서버의 기능을 포함하고 프로그램 코드를 실행하여 애플리케이션 로직을 수행한다.
		- 동적 HTML, HTTP API
		- 서블릿, JSP, 스프링 MVC 등
	- Tomcat, Jetty, Undertow 등이 WAS의 예이다.

WAS와 DB 만으로도 웹 시스템을 구성할 수 있지만 그렇게되면 WAS가 너무 많은 역할을 담당하여 서버 과부화 우려가 있기 때문에, 또한 WAS 장애시 오류 화면도 노출되지 않기 때문에 정적 리소스는 웹 서버가 처리하도록 하고 애플리케이션 로직같은 동적인 처리가 필요하면 WAS에 요청을 위임하는 WebServer -> WAS -> DB의 구조를 일반적으로 사용한다.



## 서블릿
웹 애플리케이션 서버에서 HTTP 요청에 대한 응답을 처리하기 위해 다음과 같은 일들을 해야한다.

1. 서버 TCP/IP 연결 대기, 소켓 연결
2. HTTP 요청 메시지를 파싱해서 읽기
3. HTTP 요청 방식(GET, POST, …)과 URL 읽기
4. Content-Type 확인
5. HTTP 메시지 바디 내용 파싱(요청시 전송된 데이터를 사용할 수 있도록 파싱)
6. 저장 프로세스 실행
7. 비즈니스 로직 실행
	- DB에 저장 요청
8. HTTP 응답 메시지 생성
	- HTTP 시작 라인
	- Header
	- 메시지 바디에 HTML 생성 및 입력
9. TCP/IP에 응답 전달, 소켓 종료

이를 모두 직접 구현하게 되면 개발자가 할 일이 너무 많다. 서블릿은 개발자가 비즈니스 로직에 집중하여 웹 애플리케이션을 개발할 수 있도록 공통 과정을 모두 처리해 준다. 서블릿을 지원하는 WAS를 사용하게 되면 개발자는 **7. 비즈니스 로직**에만 집중하여 개발하면 된다.

서블릿은 HTTP 요청 정보와 응답 정보를 편리하게 사용할 수 있도록 `HttpServletRequest`, `HttpServletResponse`를 제공한다.

- 서블릿은 개발자 대신 HTTP 요청 메시지를 파싱하여 `HttpServletRequest`객체에 담아서 제공한다.
	- HTTP 메소드, URL, 쿼리 스트링, 스키마, 프로토콜, 헤더, 바디 등 조회 가능
	- 해당 HTTP 요청이 시작부터 끝날 때 까지 유지되는 임시 저장소 기능
	- 세션 관리 기능 등
- `HttpServletResponse` 객체에 담겨진 데이터를 HTTP 응답 메시지로 변환하여 전송한다.
	- HTTP 응답코드 지정
	- 헤더 생성
	- 바디 생성
	- 편의기능(Content-Type, 쿠키, Redirect) 제공

자세한 내용은 찾아보자.

### 서블릿 흐름
HTTP 요청이 오면 WAS는 Request, Response 객체를 새로 만들어서 서블릿 객체를 호출한다. 
개발자는 Request 객체에서 HTTP 요청 정보를 편리하게 꺼내서 사용하고  Response 객체에 HTTP 응답 정보를 편리하게 입력할 수 있다. 
WAS는 Response 객체에 담겨있는 내용으로 HTTP 응답 정보를 생성한다.


### 서블릿 컨테이너
톰캣처럼 서블릿을 지원하는 **WAS**를 **서블릿 컨테이너**라고 한다. 서블릿 컨테이너는 서블릿 객체를 생성하고 초기화, 호출, 종료하는 생명주기를 관리한다. 서블릿 객체는 싱글톤으로 관리된다. 고객의 요청마다 계속 서블릿 객체를 생성하는 것은 비효율적이다. 따라서 최초 로딩 시점에 서블릿 객체를 미리 만들어두고 재활용한다. 서블릿 객체는 서블릿 컨테이너 종료시 함께 종료된다. 또한 WAS의 가장 큰 특징은 동시 요청을 위한 멀티 쓰레드 처리를 지원한다는 점이다. 개발자는 이에 대해 크게 신경쓰지 않아도 WAS가 이를 처리 해준다.

#### 멀티 쓰레드
WAS는 멀티 쓰레드에 대한 부분을 처리해준다.

쓰레드란 애플리케이션 코드를 하나하나 순차적으로 실행하는 것이다. 쓰레드가 없다면 자바 애플리케이션 실행이 불가능하다. 쓰레드는 한번에 하나의 코드 라인만 수행하기 때문에 동시 처리가 필요하면 쓰레드를 추가로 생성해야 한다.

HTTP 요청 마다 쓰레드가 할당되어 요청을 처리한다. 여러 사용자가 쓰레드 하나를 사용하게 되면 나중에 요청한 사용자는 대기 시간이 길어지고 앞서 요청한 사용자의 쓰레드의 처리가 지연되면 이후에 요청한 사용자들의 HTTP 요청까지 Time Out이 발생하여 쓰레드가 요청을 처리하지 못할 수 있다. 따라서 여러 사용자의 요청을 동시에 처리하기 위해서 쓰레드를 여러개 사용해야 한다.

가장 쉬운 방법은 요청마다 쓰레드를 생성하는 것이다. 이렇게 하면 동시 요청을 처리할 수 있고 리소스가 허용할 때 까지 처리가 가능하다. 또 하나의 쓰레드가 지연되어도 나머지 쓰레드는 정상적으로 동작한다.
하지만 쓰레드는 생성 비용이 매우 비싸다. 고객의 요청이 올 때마다 쓰레드를 생성하면 응답 속도가 늦어지게 된다. 또한 쓰레드는 컨텍스트 스위칭(코어에서 실행 쓰레드를 전환하는 것) 비용이 발생한다. 그리고 쓰레드 생성에 제한이 없기 때문에 고객 요청이 너무 많이오면 CPU, 메모리 임계점을 넘어서 서버가 죽을 수 있다.

이를 보완하기 위해 쓰레드를 미리 만들어두고 이를 담아두는 쓰레드 풀을 사용한다. 쓰레드 풀 방식은 필요한 쓰레드를 보관하고 관리하며 쓰레드 풀에 생성 가능한 쓰레드의 최대치를 관리한다. 톰캣의 기본 설정은 최대 200개이고 변경 가능하다. 쓰레드가 필요하면 쓰레드 풀에서 생성되어 있는 쓰레드를 꺼내서 사용하고 사용을 종료하면 쓰레드 풀에 반납한다. 최대 쓰레드가 모두 사용중이어서 쓰레드 풀에 쓰레드가 없다면 기다리는 요청은 거절하거나 특정 수만큼 대기하도록 설정할 수 있다.
쓰레드 풀을 사용하면 쓰레드를 생성하고 종료하는 비용(CPU)이 절약되고, 응답 시간이 빠르다. 또한 생성 가능한 쓰레드의 최대치가 있으므로 너무 많은 요청이 들어와도 기존 요청은 안전하게 처리 가능하다.

WAS의 주요 튜닝 포인트는 최대 쓰레드의 수이다. 이를 너무 낮게 설정하면 동시요청이 많을 때, 클라이언트는 금방 응답이 지연되고, 너무 높게 설정하면 CPU, 메모리 리소스의 임계점 초과로 서버가 다운될 수 있다. 따라서 적절한 값을 찾아야 한다. 꼭 최대한 실제 서비스와 유사하게 성능 테스트를 시도하여 적정 숫자를 찾아야 한다. 이 때 사용하는 툴로는 아파치 ab, 제이미터, nGrinder 등이 있다.


---
## MVC 패턴
과거에는 서블릿으로 뷰 화면을 위한 HTML을 만드는 작업을 했다. 이는 자바 코드에 HTML을 만드는 작업이 섞여있어 지저분하고 복잡했다.
이후 이를 해결하기 위해 JSP를 사용하여 뷰를 생성했다. 중간에 동적으로 변경이 필요한 부분이 있으면 해당 부분에만 자바 코드를 적용했다. 하지만 이는 JSP에 뷰, 비즈니스 로직 등 많은 코드들이 JSP에 노출 되어있고 JSP가 너무 많은 역할을 한다. 유지보수가 너무 힘들다.
비즈니스 로직은 서블릿처럼 다른 곳에서 처리하고, JSP는 목적에 맞게 HTML로 화면을 그리는 일에 집중할 수 있도록  MVC 패턴이 등장했다.

MVC 패턴은 **Model - View - Controller**로 역할을 나눈 것을 말한다. 
**컨트롤러**는 HTTP 요청을 받아서 파라미터를 검증하고, 비즈니스 로직을 실행한다. 이후 뷰에 전달할 결과 데이터를 조회하여 모델에 담는다. **모델**은 뷰에 출력할 데이터를 담아둔다. **뷰**는 모델에 담겨있는 데이터를 사용하여 화면을 그린다. 뷰가 필요한 데이터를 모두 모델에 담아서 전달해주기 때문에 뷰는 비즈니스 로직이나 데이터 접근을 몰라도 되고, 화면을 그리는 일에만 집중할 수 있다.


---
## 스프링 웹 MVC
과거 MVC 패턴에서 MVC 컨트롤러는 한계점을 가진다. 
- 뷰로 이동하는 코드가 항상 중복 호출된다.
```java
String viewPath = "/WEB-INF/views/new-form.jsp"; // 경로도 중복되는게 있다. 다른 뷰로 변경하면 전체 코드 다 변경해야 한다.
RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
dispatcher.forward(request, response);
```
- `HttpServletRequest`, `HttpServletResponse`를 사용하지 않을 때도 있다.
	- 테스트 코드 작성도 힘들다.
- 기능이 복잡해질수록 컨트롤러에서 공통으로 처리해야 하는 부분이 많아진다.

이를 해결하기 위하여 수문장 역할을 하는 프론트 컨트롤러 패턴을 도입하였고 **스프링 MVC의 핵심도 프론트 컨트롤러이다.** -> `DispatcherServlet`이 스프링 웹 MVC의 프론트 컨트롤러 역할을 한다.

프론트 컨트롤러 패턴의 특징은 다음과 같다.
- 프론트 컨트롤러 서블릿 하나로 클라이언트의 요청을 받는다.
- 프론트 컨트롤러가 요청에 맞는 컨트롤러를 찾아서 호출한다.
- 공통 처리가 가능하다.
- 프론트 컨트롤러를 제외한 나머지 컨트롤러는 서블릿을 사용하지 않아도 된다.



### 스프링 웹 MVC의 구조
[image:3E735A48-721E-46DC-8690-DC71229C68F4-5030-000004689A5B35B9/스크린샷 2022-05-28 오후 6.49.14.png]
- `DispatcherServlet`도 부모 클래스에서  HttpServlet을 상속받아서 사용하고 서블릿으로 동작한다.
	- DispatcherServlet -> FrameworkServlet -> HttpServletBean -> HttpServlet
- 스프링 부트는 `DistpatcherServlet`을 서블릿으로 자동 등록하면서 모든 경로에 대해서 매핑한다.

#### 동작 순서
1. 핸들러 조회 : 핸들러 매핑을 통해 요청 URL에 매핑된 핸들러(컨트롤러)를 조회한다.
2. 핸들러 어댑터 조회 : 핸들러를 실행할 수 있는 핸들러 어댑터를 조회한다.
3. 핸들러 어댑터 실행
4. 핸들러 실행 : 핸들러 어댑터가 실제 핸들러를 실행한다.
5. ModelAndView 반환 : 핸들러 어댑터는 핸들러가 반환하는 정보를 ModelAndView로 변환하여 반환한다.
6. viewResolver 호출 : 뷰 리졸버를 찾고 실행한다.
7. View 반환 : 뷰 리졸버는 뷰의 논리 이름을 물리 이름으로 변경하고, 렌더링 역할을 담당하는 뷰 객체를 반환한다.
8. 뷰 렌더링 : 뷰를 통하여 뷰를 렌더링한다.

`DispatcherServlet.doDispatch()`는 위와 같은 순서로 스프링 웹 MVC의 동작을 제어한다.
```java
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {

	HttpServletRequest processedRequest = request;
	HandlerExecutionChain mappedHandler = null;
	ModelAndView mv = null;

	// 1. 핸들러 조회	mappedHandler = getHandler(processedRequest); 
	if (mappedHandler == null) { 
		noHandlerFound(processedRequest, response);
		return; 
	} 

	//2.핸들러 어댑터 조회-핸들러를 처리할 수 있는 어댑터	HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler()); 

	// 3. 핸들러 어댑터 실행 -> 4. 핸들러 어댑터를 통해 핸들러 실행 -> 5. ModelAndView 반환 
	mv = ha.handle(processedRequest, response, mappedHandler.getHandler()); 

	processDispatchResult(processedRequest, response, mappedHandler, mv, dispatchException);

} 

private void processDispatchResult(HttpServletRequest request, HttpServletResponse response, HandlerExecutionChain mappedHandler, ModelAndView mv, Exception exception) throws Exception {
	// 뷰 렌더링 호출	
    render(mv, request, response); 
}

protected void render(ModelAndView mv, HttpServletRequest request, HttpServletResponse response) throws Exception {
	
	View view;
	String viewName = mv.getViewName(); 
	
	//6. 뷰 리졸버를 통해서 뷰 찾기,7.View 반환 
	view = resolveViewName(viewName, mv.getModelInternal(), locale, request);
	
	// 8. 뷰 렌더링 
	view.render(mv.getModelInternal(), request, response);
}

```

 








#스프링 기초/스프링 MVC/서블릿#
#스프링 기초/스프링 MVC/구조#

---
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.